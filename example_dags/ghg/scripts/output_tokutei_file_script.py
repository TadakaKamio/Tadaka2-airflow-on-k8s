import io
import json
import sqlite3
from decimal import Decimal

import ghg.common.settings as Constants
import numpy as np
import pandas as pd
from ghg.common.log import MyAppLog, log_writer
from ghg.common.settings_tokutei_info import (
    ENERGY_INFO,
    FLG_0,
    NETSU_ENERGY_ID_WITHOUT_OTHER,
    TOKUTEI_INTERMEDIATE_OUTPUT_FOLDER,
    TOKUTEI_INTERMEDIATE_OUTPUT_TEMPLATE,
)
from ghg.common.utils import (
    check_install_package,
    get_current_tokyo_timestamp,
    get_joined_path,
    get_relative_path,
    mul,
    put_fileio_to_hadoop,
)
from ghg.sql.tokutei_info import (
    SELECT_SAIBUNRUI_NETSURYO_RESULT,
    SELECT_SHIYORYO_RESULT,
)

if __name__ != "__main__":
    from airflow.models import Variable
    from ghg.common.hive_connector import HiveConnector
    from ghg.common.settings_tokutei_info import (
        ELECTRICITY_LEVELING_TIME_FACTOR,
        JIKOTAKUSO_COEFFICIENT,
        NON_FOSSIL_FUEL_COMPENSATION_FACTOR,
        OIL_CONV_FACTOR,
    )

    # Hive接続
    hive_connector = HiveConnector()

    # value: 360.53
    value_32671_5 = Decimal(32671.5)

else:
    NON_FOSSIL_FUEL_COMPENSATION_FACTOR = 0.8
    OIL_CONV_FACTOR = 0.0258
    ELECTRICITY_LEVELING_TIME_FACTOR = 0.3
    JIKOTAKUSO_COEFFICIENT = 3.6

    # value: 32671.5
    value_32671_5 = 32671.5


pd.options.mode.copy_on_write = True

logger = MyAppLog()


tables = {}


def test_query(query):
    """ローカル試験用"""
    from impala.util import as_pandas

    local_db_path = r"C:\ws\db_ghg.db"
    with sqlite3.connect(local_db_path) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return as_pandas(cursor)
        finally:
            cursor.close()


def get_all_table_data():
    """DBから関連のテーブルを取得する"""
    if __name__ == "__main__":
        year_energy = test_query("select * from energy_used_record_year_detail")
        kubun_mst = test_query("select * from kubun_mst")
        month_energy = test_query("select * from energy_used_record_month_detail")
        ancate_info = test_query("select * from ancate_info")
        optimal_factor = test_query(
            "select * from require_optimization_coefficient_for_month_mst"
        )
        energy_mst = test_query("select * from energy_mst where nendo = 2023")
        shitei_info = test_query("select * from shitei_info")
        company_mst = test_query("select * from company_mst")

        year_energy.columns = year_energy.columns.str.lower()
        kubun_mst.columns = kubun_mst.columns.str.lower()
        month_energy.columns = month_energy.columns.str.lower()
        ancate_info.columns = ancate_info.columns.str.lower()
        optimal_factor.columns = optimal_factor.columns.str.lower()
        energy_mst.columns = energy_mst.columns.str.lower()
        shitei_info.columns = shitei_info.columns.str.lower()
        company_mst.columns = company_mst.columns.str.lower()
    else:
        # Hive接続初期化
        conn = hive_connector.hive_connect()
        with conn.cursor() as cursor:
            year_energy = get_dataframe(cursor, "energy_used_record_year_detail")
            kubun_mst = get_dataframe(cursor, "kubun_mst")
            month_energy = get_dataframe(cursor, "energy_used_record_month_detail")
            ancate_info = get_dataframe(cursor, "ancate_info")
            optimal_factor = get_dataframe(
                cursor, "require_optimization_coefficient_for_month_mst"
            )
            energy_mst = get_dataframe(cursor, "energy_mst", "nendo = 2023")
            shitei_info = get_dataframe(cursor, "shitei_info")
            company_mst = get_dataframe(cursor, "company_mst")

    for df in [
        year_energy,
        kubun_mst,
        month_energy,
        ancate_info,
        optimal_factor,
        energy_mst,
        shitei_info,
        company_mst,
    ]:
        # SQL文に「*」を使って取得したの列名は所属テーブル名を付けっていますので、
        # 下記の処理で、テーブル名を取り除く
        df.columns = df.columns.str.split(".").str[-1]

        # 使わない共通列を削除する
        columns_to_drop = [
            col
            for col in [
                "delete_flg",
                "insert_name",
                "insert_date",
                "update_name",
                "update_date",
            ]
            if col in df.columns
        ]
        if columns_to_drop:
            df.drop(columns=columns_to_drop, inplace=True)

    tables["year_energy"] = year_energy
    tables["kubun_mst"] = kubun_mst
    tables["month_energy"] = month_energy
    tables["ancate_info"] = ancate_info
    tables["optimal_factor"] = optimal_factor
    tables["energy_mst"] = energy_mst
    tables["shitei_info"] = shitei_info
    tables["company_mst"] = company_mst

    # 取得のテーブルデータを調整する
    adjustData()

    return tables


def adjustData():
    """取得のテーブルデータを調整する"""

    # turn '' to 0
    ancate_info = tables["ancate_info"]
    ancate_info.loc[ancate_info["dr_date"] == "", "dr_date"] = 0

    # 単位表示を統一する
    year_energy = tables["year_energy"]
    year_energy["report_unit"] = year_energy["report_unit"].apply(unified_unit_string)
    # 「自己託送（非燃料由来の非化石電気）」の変換係数を変わる8.64⇒3.6
    year_energy.loc[year_energy["energy_id"] == "D09", "new_energy_coefficient"] = (
        JIKOTAKUSO_COEFFICIENT
    )


def sepcial_treatment_for_EP():
    """EP特定表中間ファイル出力時、一部データは修正必要です。
    EPは会社名リストの最後に置いたので、他の会社には影響ないです、
    もし他の会社も特別処理が必要であれば、元テーブルデータのバックアップは顧慮必要です。
    """

    # 銀座三井ビルディング(建物ID：1000413)以外の建物の産業分類は全部3309に変更する
    ancate_info = tables["ancate_info"]
    ancate_info.loc[ancate_info["building_id"] != "1000413", "industrial_class_cd"] = (
        "3309"
    )

    # 技術開発センター（研究所）(建物ID：1000064)の原単位分母と原単位分母の値を変更する
    ancate_info.loc[
        ancate_info["building_id"] == "1000064",
        ["denominator_type", "denominator_value"],
    ] = ["01", value_32671_5]

    # 使用しないエネルギー(灯油,軽油,A重油,液化石油ガス_LPG,輸入一般炭)の使用量を0にする
    year_energy = tables["year_energy"]
    year_energy.loc[
        year_energy["energy_id"].isin(["A06", "A07", "A08", "A12", "A19"]),
        [
            "energy_amount",
            "sale_secondary_energy_amount",
            "external_supply_fuel_amount",
            "unused_heat_amount",
        ],
    ] = [0, 0, 0, 0]


def output_intermediate_file(**kwargs):
    """中間ファイルを出力する"""
    try:
        logger.info("処理開始")

        if __name__ != "__main__":
            # openpyxlをインストール
            check_install_package(Constants.PackageName.PANDAS_ENGINE.value)

            # airflowから変数の値を取得
            company_um = Variable.get("GHG_COMPANY_UM")

            if company_um == "ALL":
                company_um_list = ["HD", "RP", "EP"]
            else:
                company_um_list = [company_um]
        else:
            company_um_list = ["HD", "PG", "RP", "EP"]

        # 関連のすべてテーブルデータを取得する
        get_all_table_data()

        for name in company_um_list:
            if name == "EP":
                sepcial_treatment_for_EP()
            write_excel(name)
    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        if __name__ != "__main__":
            if hive_connector.conn:
                # 接続を閉じる
                hive_connector.close_connection()

        logger.info("処理終了")


@log_writer(logger)
def write_excel(company_um):
    """特定中間ファイルを作成して出力する

    Args:
        tables (list): テーブルデータ
        company_um (String): 会社名略称
        report_nendo (Numbers): 報告年度
    """

    # 特定表中間ファイル出力用テンプレートファイルからデータを取得する
    if __name__ == "__main__":
        template_json = TOKUTEI_INTERMEDIATE_OUTPUT_TEMPLATE
    else:
        template_json = get_relative_path("template/tokutei_output_template.json")
    with open(template_json, "r", encoding="utf-8") as f:
        formatData = json.loads(f.read())

    outputData = []
    # 第二表のデータを読み込む
    tokutei_output_data = make_tokutei02_data(company_um)
    set_output_data(
        formatData["Tokuteihyo"]["Tokutei_02"],
        tokutei_output_data["Tokutei_02"],
        "特定-第２表",
        outputData,
    )

    # 第三表のデータを読み込む
    tokutei_output_data, gentani_count = make_tokutei03_data(company_um)
    set_output_data(
        formatData["Tokuteihyo"]["Tokutei_03"],
        tokutei_output_data["Tokutei_03"],
        "特定-第３表",
        outputData,
    )
    outputData.append(("変数", "L3", gentani_count))

    # 第十表のデータを読み込む
    tokutei_output_data = make_tokutei10_data(company_um)
    set_output_data(
        formatData["Tokuteihyo"]["Tokutei_10"],
        tokutei_output_data["Tokutei_10"],
        "特定-第４表～",
        outputData,
    )

    # そのたのデータを読み込む
    other_output_data = make_other_data(company_um)
    set_output_data(
        formatData["Tokutei_other"],
        other_output_data["Tokutei_other"],
        "その他エネルギー一覧",
        outputData,
    )

    # 熱(その他以外)のデータを読み込む
    netsu_output_data = make_netsu_data(company_um)
    set_output_data(
        formatData["Tokutei_netsu"],
        netsu_output_data["Tokutei_netsu"],
        "熱",
        outputData,
    )

    # 電気のデータを読み込む
    denki_output_data = make_denki_data(company_um)
    set_output_data(
        formatData["Tokutei_denki"],
        denki_output_data["Tokutei_denki"],
        "電気",
        outputData,
    )

    # 燃料・熱のデータを読み込む
    netsuryo_output_data = make_netsuryo_data(company_um)
    set_output_data(
        formatData["Tokutei_netsuryo"],
        netsuryo_output_data["Tokutei_netsuryo"],
        "燃料・熱",
        outputData,
    )

    # 細分類燃料・熱のデータを読込む
    saibunrui_netsuryo_output_data = make_saibunrui_netsuryo_data(company_um)
    set_output_data(
        formatData["Tokutei_saibunrui_netsuryo"],
        saibunrui_netsuryo_output_data["Tokutei_saibunrui_netsuryo"],
        "変数",
        outputData,
    )

    # 都市ガスのデータを読み込む
    toshigas_output_data = make_toshigas_data(company_um)
    set_output_data(
        formatData["Tokutei_toshigas"],
        toshigas_output_data["Tokutei_toshigas"],
        "入力・計算補助",
        outputData,
    )

    # 中間ファイルを作成して、全部のデータを「取込用」シートに出力する
    import openpyxl

    workbook = openpyxl.Workbook()
    sheet_torikomi = workbook.create_sheet("取込用")
    for data in outputData:
        sheet_torikomi.append(data)

    # ディフォルトシートを削除
    if "Sheet" in workbook.sheetnames:
        del workbook["Sheet"]

    if __name__ == "__main__":
        workbook.save(get_tokutei_intermediate_file_path(company_um))
    else:
        stream = io.BytesIO()
        workbook.save(stream)
        stream.seek(0)
        put_fileio_to_hadoop(stream, get_tokutei_intermediate_file_path(company_um))


def get_tokutei_intermediate_file_path(company_um):
    """特定表中間ファイルのパスを戻る

    Args:
        company_um (String): 名社名略称

    Returns:
        String: 特定表中間ファイルのパス
    """
    # 現在日時
    current_timestamp = get_current_tokyo_timestamp()
    file_name = f"tokutei_data_for_{company_um}_{current_timestamp}.xlsx"

    if __name__ == "__main__":
        return TOKUTEI_INTERMEDIATE_OUTPUT_FOLDER + file_name
    else:
        target_path = get_joined_path(
            Variable.get("GHG_HADOOP_BASE_PATH"),
            Variable.get("GHG_HADOOP_OUTPUTFILES_TOKUTEI_INFO_INTERMEDIATE_FILE_PATH"),
            company_um,
        )

        return f"{target_path}/{file_name}"


def set_output_data(formatData, inputData, sheetName, outputData: list):
    """中間ファイル出力用データを作成

    Args:
        formatData (Dict): 特定表入力ツールの各項目の出力セル情報
        inputData (Dict): DB取得データによって作成した出力用データ
        sheetName (String): データ出力先の特定表入力ツールのシート名
        outputData (list): 出力用データ
    """
    for key, value in formatData.items():
        if key not in inputData:
            # データに当該キーがなければ、当該キーは設定不要
            continue
        if isinstance(value, dict):
            set_output_data(value, inputData[key], sheetName, outputData)
        elif isinstance(value, list):
            for v, i in zip(value, inputData[key]):
                set_output_data(v, i, sheetName, outputData)
        else:
            if str(value) and str(value)[0] == "!":
                # set data to xml
                outputData.append((sheetName, value[1:], inputData[key]))


@log_writer(logger)
def make_tokutei02_data(company_um):
    """特定-第２表出力用データを作成

    Args:
        company_um (String): 会社名略称

    Returns:
        Dictionary: 特定-第２表出力用データ
    """
    Tokuteihyo = {}
    Tokutei_02 = Tokuteihyo["Tokutei_02"] = {}  # 特定-第２表

    # 第２表の１－１のデータを作成
    results = get_tokutei02_1_1(company_um)
    if results:
        for energyInfo in ENERGY_INFO:
            set_energy_ryo(results, energyInfo[0], energyInfo[1], Tokutei_02)

    # 第2表1-2データ作成
    results = get_tokutei02_1_2(company_um)
    if results:
        Saitekika_Denkiryo = Tokutei_02["Saitekika_Denkiryo"] = {}
        array_data = Saitekika_Denkiryo["Tsukibetsu_Array"] = []
        for row in results:
            (shiyoryo, shiyoryo_kl) = row

            item = {
                "Shiyoryo": shiyoryo,
                "Shiyoryo_Kl": shiyoryo_kl,
            }

            array_data.append({"Tsukibetsu": item})

    # 第2表1-3データ作成
    max_dr_date = get_tokutei02_1_3(company_um)
    if max_dr_date:
        Tokutei_02["Saitekika_Nissu"] = max_dr_date

    return Tokuteihyo


def set_energy_ryo(resultList, energyId, energyName, tokutei02):
    """第２表の１－１のデータを作成

    Args:
        resultList (List): SQL文の検索結果
        energyId (String): エネルギーID
        energyName (String): エネルギーのタグ名
        tokutei02 (Dictionary): 特定-第２表（データ作成先）
    """

    # リスト項目を命名する
    namedResults = [SELECT_SHIYORYO_RESULT(*row) for row in resultList]
    # 指定エネルギーIDのデータを洗い出し
    filtered_data = [result for result in namedResults if result.ENERGY_ID == energyId]
    if filtered_data:
        energyData = filtered_data[0]
        # 当該エネルギー出力用辞書構造作成
        energyDict = make_dict_by_tags_and_return_last_item(
            tokutei02, energyName.split(".")
        )

        # 使用量
        if energyData.SHIYORYO and energyData.SHIYORYO > 0:
            energyDict["Shiyoryo"] = energyData.SHIYORYO
            energyDict["Shiyoryo_Gj"] = energyData.SHIYORYO_GJ
            energyDict["Shiyoryo_Gj_2023"] = energyData.SHIYORYO_GJ_2023
        # 他者に供給する熱・電気を発生させるために使用した燃料の使用量
        if energyData.KYOKYURYO and energyData.KYOKYURYO > 0:
            energyDict["Kyokyuryo"] = energyData.KYOKYURYO
            energyDict["Kyokyuryo_Gj"] = energyData.KYOKYURYO_GJ
            energyDict["Kyokyuryo_Gj_2023"] = energyData.KYOKYURYO_GJ_2023
        # 販売した副生エネルギーの量
        if energyData.HANBAIRYO and energyData.HANBAIRYO > 0:
            energyDict["Hanbairyo"] = energyData.HANBAIRYO
            energyDict["Hanbairyo_Gj"] = energyData.HANBAIRYO_GJ
            energyDict["Hanbairyo_Gj_2023"] = energyData.HANBAIRYO_GJ_2023
        # 購入した未利用熱の量
        if energyData.MIRIYORYO and energyData.MIRIYORYO > 0:
            energyDict["Miriyoryo"] = energyData.MIRIYORYO
            energyDict["Miriyoryo_Gj"] = energyData.MIRIYORYO_GJ
            energyDict["Miriyoryo_Gj_2023"] = energyData.MIRIYORYO_GJ_2023


def make_dict_by_tags_and_return_last_item(dict, tags):
    """タグ名listによって、dictを作成する。一番中の要素を戻る

    Args:
        dict (Dictionary): 構築対象dict
        tags (List): タグ名list

    Returns:
        Dictionary: タグ名listに一番中の要素
    """
    if dict is None or tags is None:
        logger.error("args cannot be None")
        return

    if len(tags) == 0:
        item = dict
    if len(tags) == 1:
        item = dict[tags[0]] = {}
    else:
        # 当該タグは存在しない場合、空白タグを作成する
        if tags[0] not in dict:
            dict[tags[0]] = {}

        # 次レベルのタグを作成する
        inner_item = dict[tags[0]]
        item = make_dict_by_tags_and_return_last_item(inner_item, tags[1:])

    return item


def make_other_data(company_um):
    """
    その他のデータを処理して辞書形式で返す
    """
    other = {}
    other_results = get_tokutei_others(company_um)
    tokutei_other = {}
    arrays = [
        "SonotaNenryo_Array",  # 化石燃料
        "SonotaHikasekiNenryo_Array",  # 非化石燃料
        "SonotaNetsu_Array",  # 他者から購入した熱
        "SonotaNetu_Array",  # その他使用した熱
        "Jikahatsuden_Array",  # 自家発電
        "Toshigas_Array",  # 都市ガス
    ]
    for array_name in arrays:
        array_data = tokutei_other[array_name] = []
        item_name = array_name[:-6]
        filtered_data = []
        if item_name == "SonotaNetsu":
            filtered_data.extend(
                [rew for rew in other_results if rew[0] in ("C09", "C10")]
            )
        else:
            if item_name == "SonotaNenryo":
                energy_id = "A29"
            elif item_name == "SonotaHikasekiNenryo":
                energy_id = "B17"
            elif item_name == "SonotaNetu":
                energy_id = "C15"
            elif item_name == "Jikahatsuden":
                energy_id = "D24"
            elif item_name == "Toshigas":
                energy_id = "A28"
            # row[0]:エネルギーID(ENERGY_ID)
            filtered_data = [rew for rew in other_results if rew[0] == energy_id]

        for row in filtered_data:
            (
                energy_id,
                eneShurui,
                tani,
                shiyoryo,
                kyokyuryo,
                hanbairyo,
                miriyoryo,
                kansan_Keisu,
                tatemono_Name,
                sangyoBunrui,
                Jigyosya,
            ) = row
            item = {
                "EneShurui": eneShurui,
                "Tani": tani,
                "Shiyoryo": shiyoryo,
                "Kyokyuryo": kyokyuryo,
                "Hanbairyo": hanbairyo,
                "Miriyoryo": miriyoryo,
                "Kansan_Keisu": kansan_Keisu,
                "Tatemono_Name": tatemono_Name,
                "SangyoBunrui": sangyoBunrui,
                "Jigyosya": Jigyosya,
            }
            array_data.append({item_name: item})
    other["Tokutei_other"] = tokutei_other
    return other


def make_netsu_data(company_um):
    """
    熱(その他以外)のデータを処理して辞書形式で返す
    """
    tokutei_netsu = {}
    netsu = {"Tokutei_netsu": tokutei_netsu}

    netsu_results = get_tokutei_netsu(company_um)
    if not netsu_results:
        return netsu

    array_data = tokutei_netsu["Netsu_Array"] = []
    for row in netsu_results:
        (
            Jigyosha_Name,
            Shiyoryo,
            Tatemono_Name,
            SangyoBunrui,
        ) = row
        item = {
            "Jigyosha_Name": Jigyosha_Name,
            "Shiyoryo": Shiyoryo,
            "Tatemono_Name": Tatemono_Name,
            "SangyoBunrui": SangyoBunrui,
        }
        array_data.append({"Netsu": item})
    return netsu


def make_denki_data(company_um):
    """
    電気のデータを処理して辞書形式で返す
    """
    denki = {}
    denki_results = get_tokutei_denki(company_um)
    tokutei_denki = {}
    array_data = tokutei_denki["Denki_Array"] = []
    for row in denki_results:
        (
            jigyosha_name,
            menu_name,
            wariai,
            tatemono_Name,
            sangyoBunrui,
            Hiru,
            Yoru,
        ) = row
        item = {
            "Jigyosha_Name": jigyosha_name,
            "Menu_Name": menu_name,
            "Wariai": wariai,
            "Tatemono_Name": tatemono_Name,
            "SangyoBunrui": sangyoBunrui,
            "Hiru": Hiru,
            "Yoru": Yoru,
        }
        array_data.append({"Denki": item})
    denki["Tokutei_denki"] = tokutei_denki
    return denki


def make_netsuryo_data(company_um):
    """
    燃料・熱のデータを処理して辞書形式で返す
    """
    netsuryo = {}
    netsuryo_results = get_tokutei_netsuryo(company_um)
    netsuryo_array = netsuryo["Netsuryo_Array"] = {}
    id_to_type = {
        "AB": "Netsuryo",
        "C0102": "jyoki",
        "C0304": "jyoki2",
        "C0506": "onsui",
        "C0708": "reisui",
        "C11": "chinetsu",
        "C12": "onsennetsu",
        "C13": "taiyonetsu",
        "C14": "seppyonetsu",
    }
    for row in netsuryo_results:
        (
            id,
            value,
            hanbai_value,
        ) = row
        item = {
            "value": value,
            "hanbai_value": hanbai_value,
        }
        # IDによって対応する燃料・熱を取得
        type_name = id_to_type.get(id, value)
        if type_name:
            netsuryo_array[type_name] = item

    return {"Tokutei_netsuryo": netsuryo}


def make_saibunrui_netsuryo_data(company_um):
    """細分類の燃料・熱データを処理して、辞書形式で返す

    Args:
        company_um (String): 会社名略称
    """
    saibunrui_netsuryo = {}
    # 各エネルギーのタグ名
    TAGS = {
        "AB": "Netsuryo",
        "C0102": "jyoki",
        "C0304": "jyoki2",
        "C0506": "onsui",
        "C0708": "reisui",
        "C11": "chinetsu",
        "C12": "onsennetsu",
        "C13": "taiyonetsu",
        "C14": "seppyonetsu",
    }
    results = get_tokutei_saibunrui_netsuryo(company_um)
    # リスト項目を命名する
    saibunrui_data = [SELECT_SAIBUNRUI_NETSURYO_RESULT(*row) for row in results]

    # 細分類番号3311のデータを洗い出し
    data_3311 = [
        result for result in saibunrui_data if result.INDUSTRIAL_CLASS_CD == "3311"
    ]
    netsuryo_3311 = saibunrui_netsuryo["Netsuryo_3311"] = {}
    for row in data_3311:
        item = {"value": row.USED, "hanbai_value": row.SOLD}
        netsuryo_3311[TAGS[row.ENERGY_ID]] = item

    # 細分類番号3300のデータを洗い出し
    data_3300 = [
        result for result in saibunrui_data if result.INDUSTRIAL_CLASS_CD == "3300"
    ]
    netsuryo_3300 = saibunrui_netsuryo["Netsuryo_3300"] = {}
    for row in data_3300:
        item = {"value": row.USED, "hanbai_value": row.SOLD}
        netsuryo_3300[TAGS[row.ENERGY_ID]] = item

    # 細分類番号3309のデータを洗い出し
    data_3309 = [
        result for result in saibunrui_data if result.INDUSTRIAL_CLASS_CD == "3309"
    ]
    netsuryo_3309 = saibunrui_netsuryo["Netsuryo_3309"] = {}
    for row in data_3309:
        item = {"value": row.USED, "hanbai_value": row.SOLD}
        netsuryo_3309[TAGS[row.ENERGY_ID]] = item

    return {"Tokutei_saibunrui_netsuryo": saibunrui_netsuryo}


def make_tokutei03_data(company_um):
    """
    第三表のデータを処理して辞書形式で返す
    """
    tokutei03 = {}
    gentani = get_tokutei03_data(company_um)
    tokutei_tokutei03 = {}
    gentani_count = 0

    if gentani:
        gentani_count = len(gentani)
        if gentani_count == 1:
            array_key = "Gentani_Keisan2"
        else:
            array_key = "Gentani_Keisan"
        array_data = []

        for row in gentani:
            (
                industrial_class_cd,
                denominator_type,
                value,
                name,
                tani,
                a,
                a_2023,
                a2,
                a2_2023,
                b,
                b_2023,
                b2,
                b2_2023,
                ha2,
                ha2_2023,
            ) = row
            item = {
                "INDUSTRIAL_CLASS_CD[0]": industrial_class_cd[0],
                "INDUSTRIAL_CLASS_CD[1]": industrial_class_cd[1],
                "INDUSTRIAL_CLASS_CD[2]": industrial_class_cd[2],
                "INDUSTRIAL_CLASS_CD[3]": industrial_class_cd[3],
                "DENOMINATOR_TYPE": denominator_type,
                "DENOMINATOR_NM": name,
                "DENOMINATOR_TANI": unit_symbol_conversion(tani),
                "DENOMINATOR_VALUE": value,
                "A": a,
                "A_2023": a_2023,
                "A2": a2,
                "A2_2023": a2_2023,
                "B": b,
                "B_2023": b_2023,
                "B2": b2,
                "B2_2023": b2_2023,
                "HEIJYUNKA_A2": ha2,
                "HEIJYUNKA_A2_2023": ha2_2023,
            }
            array_data.append({"Gentani": item})
        tokutei_tokutei03[array_key] = array_data
    tokutei03["Tokutei_03"] = tokutei_tokutei03
    return tokutei03, gentani_count


def make_tokutei10_data(company_um):
    """
    第十表のデータを処理して辞書形式で返す
    """
    tokutei10 = {}
    kojyo = get_tokutei10(company_um)
    array_data = []
    for row in kojyo:
        (tabl1,) = row
        tabl1_dict = json.loads(tabl1)
        item = {
            "kojyoNo": tabl1_dict.get("Shitei_Kojyo_No"),
            "Name": tabl1_dict.get("Shitei_Kojyo_Name"),
            "Name_Bf": tabl1_dict.get("Shitei_Kojyo_Name_Bf"),
            "Zip": tabl1_dict.get("Shitei_Kojyo_Zip"),
            "Address": tabl1_dict.get("Shitei_Kojyo_Address"),
            "No1": tabl1_dict.get("Shitei_SaibunruiNo")[0],
            "No2": tabl1_dict.get("Shitei_SaibunruiNo")[1],
            "No3": tabl1_dict.get("Shitei_SaibunruiNo")[2],
            "No4": tabl1_dict.get("Shitei_SaibunruiNo")[3],
        }
        array_data.append({"Kojyo_Meisai": item})
    tokutei10["Tokutei_10"] = {"Shitei_Kojyo_Meisai_Array": array_data}
    return tokutei10


def make_toshigas_data(company_um):
    """
    都市ガスのデータを処理して辞書形式で返す
    """
    toshigas = {}
    toshigas_results = get_tokutei_toshigas(company_um)
    array_data = []
    for row in toshigas_results:
        (
            kaisyamei,
            kakarisu,
            Shiyoryo,
            Kyokyuryo,
            Hanbairyo,
        ) = row
        item = {
            "kaisyamei": kaisyamei,
            "kakarisu": kakarisu,
            "Shiyoryo": Shiyoryo,
            "Kyokyuryo": Kyokyuryo,
            "Hanbairyo": Hanbairyo,
        }
        array_data.append({"ToshiGas": item})
    toshigas["Tokutei_toshigas"] = {"ToshiGas_Array": array_data}
    return toshigas


def unit_symbol_conversion(unit_symbol):
    """単位符号変換

    Args:
        unit_symbol (String): 単位符号
    """
    if unit_symbol == "m2":
        return "㎡"
    else:
        return unit_symbol


def get_dataframe(cursor, table_name, where_option=""):
    """DBからデータを取得してDataFrameに変換して戻る

    Args:
        cursor (cursor): 検索用カーソル
        table_name (str): テーブル名
        where_option (str, optional): 検索条件. Defaults to "".

    Returns:
        _type_: _description_
    """
    from impala.util import as_pandas

    query = f"select * from {table_name}"
    if where_option:
        query += f" where {where_option}"
    cursor.execute(query)
    return as_pandas(cursor)


def get_tokutei03_data(company_um):
    """テーブル３用データを取得する

    Args:
        tables (list): テーブルデータ
        company_um (str): 会社名略称

    Returns:
        list: テーブル３用データ
    """

    # tablesから今回使用のデータを取得する
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)
    if ancate_info.empty:
        return None
    # 原単位分母の値を集計する
    ancate_info_tani = (
        ancate_info.groupby(["industrial_class_cd", "denominator_type"])
        .apply(lambda x: (x["denominator_value"] * x["anbun_rate"]).sum())
        .reset_index(name="denominator_value")
    )
    year_energy = tables["year_energy"]
    kubun_mst = tables["kubun_mst"]
    kubun_0015 = kubun_mst[kubun_mst["bunrui_cd"] == "0015"]
    kubun_0002 = kubun_mst[kubun_mst["bunrui_cd"] == "0002"]
    # 原単位分母の名称と単位を追加する
    kubun_0002["denominator_nm"] = kubun_0002["kbn_name"].str.extract(r"(^[^\[]+)")
    kubun_0002["denominator_tani"] = kubun_0002["kbn_name"].str.extract(r"\[(.*?)\]")

    month_energy = tables["month_energy"]
    month_energy_power = month_energy[
        month_energy["energy_id"].isin(["D01", "D03", "D04", "D06", "D07", "D08"])
    ]
    optimal_factor = tables["optimal_factor"]
    energy_mst = tables["energy_mst"]

    # 合理化データを作成
    df1 = year_energy.merge(
        kubun_0015,
        how="left",
        left_on="energy_id",
        right_on="kbn_cd",
        suffixes=("", "_0015"),
    )
    df1 = df1.where(df1.notnull(), None)

    # 検索項目を処理する
    df1["data_flg"] = 0
    df1["energy_amount_gj"] = mul(df1["energy_amount"], df1["new_energy_coefficient"])
    df1["energy_amount_gj_2023"] = mul(
        df1["energy_amount"], df1["old_energy_coefficient"]
    )
    df1["sale_secondary_energy_amount_gj"] = mul(
        df1["sale_secondary_energy_amount"], df1["new_energy_coefficient"]
    )
    df1["sale_secondary_energy_amount_gj_2023"] = mul(
        df1["sale_secondary_energy_amount"], df1["old_energy_coefficient"]
    )
    df1["unused_heat_amount_gj"] = mul(
        df1["unused_heat_amount"], df1["new_energy_coefficient"]
    )
    df1["unused_heat_amount_gj_2023"] = mul(
        df1["unused_heat_amount"], df1["old_energy_coefficient"]
    )

    # 検索条件
    df1 = df1[(df1["kbn_cd"].notnull()) | df1["energy_id"].isin(["D02", "D05"])]

    # 最適化電気データを作成
    df2 = month_energy_power.merge(
        ancate_info, on=["ancate_id", "report_nendo"], suffixes=("_month", "")
    ).merge(
        optimal_factor,
        on=["target_month", "power_area_cd", "report_nendo"],
        suffixes=("", "_factor"),
    )

    # 集計処理
    # 変電所以外の按分比率
    df2["use_rate"] = df2.apply(
        lambda row: (
            row["substation_floor_rate"]
            if row["substation_energy_grasp_flag"] == "1"
            else 1
        ),
        axis=1,
    )
    # 最適化電気の使用量GJ
    df2["energy_gj"] = (
        mul(
            df2["energy_usage_amount"],
            df2["require_optimization_coefficient"],
            df2["use_rate"],
        )
        / 1000
    )

    # df2["require_optimization_coefficient"]に値がNULLの場合、
    # df2["energy_gj"]に一部値がfloatになる(hive側)。
    # 原因は不明ですが、一旦下記の処理を追加する。
    if __name__ != "__main__":
        df2["energy_gj"] = df2["energy_gj"].apply(Decimal)
    else:
        df2["energy_gj"] = df2["energy_gj"].apply(float)

    df2 = (
        df2.groupby(["ancate_id", "energy_id"])
        .agg(
            report_nendo=("report_nendo", "max"), energy_amount_gj=("energy_gj", "sum")
        )
        .reset_index()
    )
    # 検索項目を処理する
    df2["data_flg"] = 1
    df2["energy_amount_gj_2023"] = 0
    df2["sale_secondary_energy_amount_gj"] = 0
    df2["sale_secondary_energy_amount_gj_2023"] = 0
    df2["unused_heat_amount_gj"] = 0
    df2["unused_heat_amount_gj_2023"] = 0

    df_union = pd.concat([df1, df2])
    df_merge = (
        df_union.merge(ancate_info, on=["ancate_id"], suffixes=("", "_ai"))
        .merge(
            energy_mst,
            left_on=["energy_id", "report_nendo"],
            right_on=["energy_id", "nendo"],
        )
        .merge(
            kubun_0002,
            left_on=["denominator_type"],
            right_on=["kbn_cd"],
            suffixes=("", "_0002"),
        )
    )

    # 集計時使用の関数
    def genyu_sum(series, condition, rate):
        return mul(series[condition], rate, OIL_CONV_FACTOR).sum()

    df = df_merge
    df_group = (
        df.groupby(["industrial_class_cd", "denominator_type"])
        .agg(
            denominator_nm=("denominator_nm", "max"),
            denominator_tani=("denominator_tani", "max"),
            a=(
                "energy_amount_gj",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            a_2023=(
                "energy_amount_gj_2023",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            a2=(
                "energy_amount_gj",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1)
                        & (~df["energy_id"].isin(["D02", "D05"]))
                        & (df["energy_type_cd"] == "B"),
                        mul(df["anbun_rate"], NON_FOSSIL_FUEL_COMPENSATION_FACTOR),
                    )
                    + genyu_sum(
                        x,
                        (df["data_flg"] != 1)
                        & (~df["energy_id"].isin(["D02", "D05"]))
                        & (df["energy_type_cd"] != "B"),
                        df["anbun_rate"],
                    )
                ),
            ),
            a2_2023=(
                "energy_amount_gj_2023",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            b=(
                "sale_secondary_energy_amount_gj",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            b_2023=(
                "sale_secondary_energy_amount_gj_2023",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            b2=(
                "unused_heat_amount_gj",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["energy_type_cd"] == "C")
                        & (df["data_flg"] != 1)
                        & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            b2_2023=(
                "unused_heat_amount_gj_2023",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["energy_type_cd"] == "C")
                        & (df["data_flg"] != 1)
                        & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
            heijyunka_a2=(
                "energy_amount_gj",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        ~(
                            ((df["data_flg"] == 0))
                            & (
                                df["energy_id"].isin(
                                    ["D01", "D03", "D04", "D06", "D07", "D08"]
                                )
                            )
                        )
                        & (~df["energy_id"].isin(["D02", "D05"]))
                        & (df["energy_type_cd"] == "B"),
                        mul(df["anbun_rate"], NON_FOSSIL_FUEL_COMPENSATION_FACTOR),
                    )
                    + genyu_sum(
                        x,
                        ~(
                            ((df["data_flg"] == 0))
                            & (
                                df["energy_id"].isin(
                                    ["D01", "D03", "D04", "D06", "D07", "D08"]
                                )
                            )
                        )
                        & (~df["energy_id"].isin(["D02", "D05"]))
                        & (df["energy_type_cd"] != "B"),
                        df["anbun_rate"],
                    )
                ),
            ),
            heijyunka_a2_2023=(
                "energy_amount_gj_2023",
                lambda x: general_round(
                    genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (df["energy_id"].isin(["D02", "D05"])),
                        mul(df["anbun_rate"], ELECTRICITY_LEVELING_TIME_FACTOR),
                    )
                    + genyu_sum(
                        x,
                        (df["data_flg"] != 1) & (~df["energy_id"].isin(["D02", "D05"])),
                        df["anbun_rate"],
                    )
                ),
            ),
        )
        .reset_index()
    )
    result = ancate_info_tani.merge(
        df_group, on=["industrial_class_cd", "denominator_type"], suffixes=("", "_2")
    )

    # 使用量が0のデータは削除する
    result = result[result["a"] > 0]

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def get_tokutei02_1_1(company_um):
    """特定第２表の１－１のデータを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 特定第２表の１－１のデータ
    """
    # 調査表情報
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)
    if ancate_info.empty:
        return None

    # エネルギー使用実績明細(年別)
    year_energy = tables["year_energy"][
        [
            "ancate_id",
            "energy_id",
            "energy_amount",
            "new_energy_coefficient",
            "old_energy_coefficient",
            "external_supply_fuel_amount",
            "sale_secondary_energy_amount",
            "unused_heat_amount",
        ]
    ]
    year_energy["energy_id"] = year_energy.apply(
        lambda row: (
            "D01" if row["energy_id"] in ["D03", "D04", "D06"] else row["energy_id"]
        ),
        axis=1,
    )
    year_energy2 = tables["year_energy"][
        [
            "ancate_id",
            "energy_id",
            "energy_amount",
            "new_energy_coefficient",
            "old_energy_coefficient",
            "external_supply_fuel_amount",
            "sale_secondary_energy_amount",
            "unused_heat_amount",
        ]
    ]
    # 化石熱と非化石熱を同じエネルギーIDにする
    energy_id_map = {
        "C01": "C0102",
        "C02": "C0102",
        "C03": "C0304",
        "C04": "C0304",
        "C05": "C0506",
        "C06": "C0506",
        "C07": "C0708",
        "C08": "C0708",
        "D10": "D1011",
        "D11": "D1011",
    }
    # 熱エネルギーIDが対応にする
    year_energy2 = year_energy2[year_energy2["energy_id"].isin(energy_id_map.keys())]
    year_energy2["energy_id"] = (
        year_energy2["energy_id"].map(energy_id_map).fillna(year_energy2["energy_id"])
    )

    year_energy_all = pd.concat([year_energy, year_energy2])

    df = ancate_info.merge(year_energy_all, on="ancate_id", suffixes=("", "_all"))

    grouped = df.groupby(["report_nendo", "energy_id"])

    result = grouped.apply(
        lambda x: pd.Series(
            {
                "report_nendo": x.name[0],
                "energy_id": x.name[1],
                "shiyoryo": mul(x["energy_amount"], x["anbun_rate"]).sum(),
                "shiyoryo_gj": mul(
                    x["energy_amount"], x["anbun_rate"], x["new_energy_coefficient"]
                ).sum(),
                "shiyoryo_gj_2023": mul(
                    x["energy_amount"], x["anbun_rate"], x["old_energy_coefficient"]
                ).sum(),
                "kyokyuryo": mul(
                    x["external_supply_fuel_amount"], x["anbun_rate"]
                ).sum(),
                "kyokyuryo_gj": mul(
                    x["external_supply_fuel_amount"],
                    x["anbun_rate"],
                    x["new_energy_coefficient"],
                ).sum(),
                "kyokyuryo_gj_2023": mul(
                    x["external_supply_fuel_amount"],
                    x["anbun_rate"],
                    x["old_energy_coefficient"],
                ).sum(),
                "hanbairyo": mul(
                    x["sale_secondary_energy_amount"], x["anbun_rate"]
                ).sum(),
                "hanbairyo_gj": mul(
                    x["sale_secondary_energy_amount"],
                    x["anbun_rate"],
                    x["new_energy_coefficient"],
                ).sum(),
                "hanbairyo_gj_2023": mul(
                    x["sale_secondary_energy_amount"],
                    x["anbun_rate"],
                    x["old_energy_coefficient"],
                ).sum(),
                "miriyoryo": mul(x["unused_heat_amount"], x["anbun_rate"]).sum(),
                "miriyoryo_gj": mul(
                    x["unused_heat_amount"],
                    x["anbun_rate"],
                    x["new_energy_coefficient"],
                ).sum(),
                "miriyoryo_gj_2023": mul(
                    x["unused_heat_amount"],
                    x["anbun_rate"],
                    x["old_energy_coefficient"],
                ).sum(),
            }
        )
    )

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def get_tokutei02_1_2(company_um):
    """特定第２表の１－２のデータを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 特定第２表の１－２のデータ
    """
    # 調査表情報
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)
    if ancate_info.empty:
        return None

    # エネルギー使用実績明細(月別)
    month_energy = tables["month_energy"][
        ["ancate_id", "energy_id", "target_month", "energy_usage_amount"]
    ]
    month_energy_power = month_energy[
        month_energy["energy_id"].isin(["D01", "D03", "D04", "D06", "D07", "D08"])
    ]

    # 月別電気需要最適化係数マスタ
    optimal_factor = tables["optimal_factor"][
        [
            "target_month",
            "power_area_cd",
            "report_nendo",
            "require_optimization_coefficient",
        ]
    ]

    # テーブル結合
    df = month_energy_power.merge(
        ancate_info, on="ancate_id", suffixes=("_month", "")
    ).merge(
        optimal_factor,
        on=["power_area_cd", "report_nendo", "target_month"],
        suffixes=("", "_factor"),
    )

    # 変電所以外の按分比率を設定
    df["rate"] = df.apply(
        lambda x: (
            x["substation_floor_rate"]
            if x["substation_energy_grasp_flag"] == "1"
            else 1
        ),
        axis=1,
    )
    df["energy_amount"] = (
        mul(df["energy_usage_amount"], df["anbun_rate"], df["rate"]) / 1000
    )
    df["energy_amount_kl"] = (
        mul(
            df["energy_usage_amount"],
            df["require_optimization_coefficient"],
            df["anbun_rate"],
            df["rate"],
            OIL_CONV_FACTOR,
        )
        / 1000
    )

    # 集計
    df_grouped = (
        df.groupby("target_month")
        .agg({"energy_amount": "sum", "energy_amount_kl": "sum"})
        .reset_index()
    )

    # ソート
    df_grouped["sort_order"] = (df_grouped["target_month"] + 8) % 12
    df_sorted = df_grouped.sort_values("sort_order").drop(columns="sort_order")

    # 検索項目を洗い出し
    result = df_sorted[["energy_amount", "energy_amount_kl"]]

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def get_tokutei02_1_3(company_um):
    """特定第２表の１－３のデータを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 特定第２表の１－３のデータ
    """
    # 調査表情報
    ancate_info_all = tables["ancate_info"][
        [
            "report_nendo",
            "anbun_rate_hd",
            "anbun_rate_pg",
            "anbun_rate_ep",
            "anbun_rate_rp",
            "power_area_cd",
            "dr_date",
        ]
    ]
    ancate_info = filter_ancate_info_by_anbun_rate(ancate_info_all, company_um)

    return ancate_info["dr_date"].max()


def get_tokutei10(company_um):
    """特定第１０表のデータを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 特定第１０表のデータ
    """
    # 指定表情報
    shitei_info = tables["shitei_info"]
    company_mst = tables["company_mst"]

    df = shitei_info.merge(company_mst, on="company_id", suffixes=("", "_cm"))

    df_filter = df[df["company_um"] == company_um]

    result = df_filter[["table_1"]]

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def filter_ancate_info_by_anbun_rate(df, company_um):
    """会社名略称によって、按分比率を設定する。
       按分比率が0以下のデータを除く

    Args:
        df (DataFrame): ancate_infoテーブルデータ
        company_um (str): 会社名略称
    """
    if company_um == "HD":
        df["anbun_rate"] = df["anbun_rate_hd"]
    elif company_um == "PG":
        df["anbun_rate"] = df["anbun_rate_pg"]
    elif company_um == "EP":
        df["anbun_rate"] = df["anbun_rate_ep"]
    elif company_um == "RP":
        df["anbun_rate"] = df["anbun_rate_rp"]
    else:
        df["anbun_rate"] = 0

    # turn '' to 0
    df.loc[df["anbun_rate"] == "", "anbun_rate"] = 0

    return df[df["anbun_rate"] > 0]


def get_tokutei_toshigas(company_um):
    """都市ガス情報を取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 都市ガス情報
    """
    # 調査表情報
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)

    year_energy_all = tables["year_energy"]
    year_energy = year_energy_all[year_energy_all["energy_id"] == "A28"]
    year_energy = year_energy[year_energy["energy_amount"] > 0]

    df = ancate_info.merge(year_energy, on="ancate_id", suffixes=("", "_year"))

    grouped = df.groupby(
        ["gas_company_id", "new_energy_coefficient"], as_index=True
    ).agg(
        gas_company_nm=("gas_company_nm", "max"),
        new_energy_coefficient=("new_energy_coefficient", "max"),
        total_energy_amount=(
            "energy_amount",
            lambda x: mul(x, df.loc[x.index, "anbun_rate"]).sum(),
        ),
        total_external_supply_fuel_amount=(
            "external_supply_fuel_amount",
            lambda x: mul(x, df.loc[x.index, "anbun_rate"]).sum(),
        ),
        total_sale_secondary_energy_amount=(
            "sale_secondary_energy_amount",
            lambda x: mul(x, df.loc[x.index, "anbun_rate"]).sum(),
        ),
    )

    # turn DataFrame data to table
    table_data = list(grouped.to_records(index=False))

    return table_data


def get_tokutei_others(company_um):
    """「その他エネルギー一覧」のデータを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 「その他エネルギー一覧」のデータ
    """
    # 調査表情報
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)
    # エネルギー使用実績明細(年別)
    year_energy_all = tables["year_energy"]
    year_energy_A29 = year_energy_all[year_energy_all["energy_id"] == "A29"]
    year_energy_A28 = year_energy_all[year_energy_all["energy_id"] == "A28"]
    year_energy_B17 = year_energy_all[year_energy_all["energy_id"] == "B17"]
    year_energy_C0910 = year_energy_all[
        year_energy_all["energy_id"].isin(["C09", "C10"])
    ]
    year_energy_C15 = year_energy_all[year_energy_all["energy_id"] == "C15"]
    year_energy_D2426 = year_energy_all[
        year_energy_all["energy_id"].isin(["D24", "D26"])
    ]

    logger.debug(f"litest1 type: {year_energy_all['energy_id'].dtype}")
    logger.debug(year_energy_all["energy_id"])
    # 設備容量
    year_energy_capacity = year_energy_all[
        year_energy_all["energy_id"].isin(["D25", "D27"])
    ]
    # 設備容量のエネルギーIDを使用量のIDと統一する
    if not year_energy_capacity.empty:
        year_energy_capacity["energy_id"] = year_energy_capacity.apply(
            lambda row: ("D24" if row["energy_id"] == "D25" else "D26"),
            axis=1,
        )

    # 化石燃料その他
    df_A29 = year_energy_A29.merge(ancate_info, on="ancate_id", suffixes=("_A29", ""))
    df_A29["unused_heat_amount"] = 0
    df_A29["heat_company_nm"] = ""

    # 都市ガス
    df_A28 = year_energy_A28.merge(ancate_info, on="ancate_id", suffixes=("_A28", ""))
    df_A28["unused_heat_amount"] = 0
    df_A28["heat_company_nm"] = ""
    df_A28["energy_name"] = df_A28["gas_company_nm"]

    # 非化石燃料その他
    df_B17 = year_energy_B17.merge(ancate_info, on="ancate_id", suffixes=("_B17", ""))
    df_B17["unused_heat_amount"] = 0
    df_B17["heat_company_nm"] = ""

    # 他者から購入した熱　その他
    df_C0910 = year_energy_C0910.merge(
        ancate_info, on="ancate_id", suffixes=("_C0910", "")
    )
    if not df_C0910.empty:
        df_C0910["energy_name"] = df_C0910.apply(
            lambda row: (
                row["energy_name"][:-3]
                if row["energy_id"] == "C09"
                else (
                    row["energy_name"][:-4]
                    if row["energy_id"] == "C10"
                    else row["energy_name"]
                )
            ),
            axis=1,
        )
    df_C0910["external_supply_fuel_amount"] = 0

    # その他使用した熱　その他
    df_C15 = year_energy_C15.merge(ancate_info, on="ancate_id", suffixes=("_C15", ""))
    df_C15["external_supply_fuel_amount"] = 0
    df_C15["heat_company_nm"] = ""

    # 自家発電　その他(非燃料由来の非化石)
    df_D = year_energy_D2426.merge(
        ancate_info, on="ancate_id", suffixes=("_D2426", "")
    ).merge(
        year_energy_capacity,
        on=["ancate_id", "energy_id"],
        how="left",
        suffixes=("", "_capacity"),
    )
    df_D.loc[df_D["energy_id"] == "D26", "energy_id"] = "D24"
    df_D["heat_company_nm"] = df_D["energy_amount_capacity"].astype(str)

    df = pd.concat([df_A29, df_A28, df_B17, df_C0910, df_C15, df_D])

    # 会社按分比率で計算する
    df["energy_amount"] = mul(df["energy_amount"], df["anbun_rate"])
    df["external_supply_fuel_amount"] = mul(
        df["external_supply_fuel_amount"], df["anbun_rate"]
    )
    df["sale_secondary_energy_amount"] = mul(
        df["sale_secondary_energy_amount"], df["anbun_rate"]
    )
    df["unused_heat_amount"] = mul(df["unused_heat_amount"], df["anbun_rate"])

    # 使用量が0のデータを除く
    df = df[df["energy_amount"] > 0]

    df = df[
        [
            "energy_id",
            "energy_name",
            "report_unit",
            "energy_amount",
            "external_supply_fuel_amount",
            "sale_secondary_energy_amount",
            "unused_heat_amount",
            "new_energy_coefficient",
            "building_nm",
            "industrial_class_cd",
            "heat_company_nm",
        ]
    ]
    result = df.sort_values(by=["building_nm", "energy_name"])

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def get_tokutei_netsu(company_um):
    """「熱」シートのデータを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 「熱」シートのデータ
    """
    # 調査表情報
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)
    # エネルギー使用実績明細(年別)
    year_energy_all = tables["year_energy"]
    year_energy_netsu = year_energy_all[
        year_energy_all["energy_id"].isin(NETSU_ENERGY_ID_WITHOUT_OTHER)
    ]

    df_merge = ancate_info.merge(
        year_energy_netsu, on="ancate_id", how="left", suffixes=("", "_1")
    )

    df_merge["energy_amount"] = mul(df_merge["energy_amount"], df_merge["anbun_rate"])

    grouped_df = df_merge.groupby("ancate_id").agg(
        {
            "heat_company_nm": "first",
            "energy_amount": "sum",
            "building_nm": "first",
            "industrial_class_cd": "first",
        }
    )

    filtered_df = grouped_df[grouped_df["energy_amount"] > 0]

    # turn DataFrame data to table
    table_data = list(filtered_df.to_records(index=False))

    return table_data


def get_tokutei_denki(company_um):
    """「電気」のデータを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 「電気」のデータ
    """
    # 調査表情報
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)
    # エネルギー使用実績明細(年別)
    year_energy_all = tables["year_energy"]
    year_energy_day1 = year_energy_all[year_energy_all["energy_id"] == "D01"]
    year_energy_night1 = year_energy_all[year_energy_all["energy_id"] == "D03"]
    year_energy_day2 = year_energy_all[year_energy_all["energy_id"] == "D04"]
    year_energy_night2 = year_energy_all[year_energy_all["energy_id"] == "D06"]

    # 電気事業者１
    year_energy1 = ancate_info.merge(
        year_energy_day1, on="ancate_id", how="left", suffixes=("", "_1")
    ).merge(year_energy_night1, on="ancate_id", how="left", suffixes=("", "_2"))
    year_energy1["company_nm"] = year_energy1["electricity_enterprise1_company_nm"]
    year_energy1["menu_nm"] = year_energy1["electricity_enterprise1_menu_nm"]
    year_energy1["ratio"] = year_energy1["non_fossil_ratio1"]
    year_energy1["energy_amount_day"] = mul(
        year_energy1["energy_amount"], year_energy1["anbun_rate"]
    )
    year_energy1["energy_amount_night"] = mul(
        year_energy1["energy_amount_2"], year_energy1["anbun_rate"]
    )

    # 電気事業者２
    year_energy2 = ancate_info.merge(
        year_energy_day2, on="ancate_id", how="left", suffixes=("", "_1")
    ).merge(year_energy_night2, on="ancate_id", how="left", suffixes=("", "_2"))
    year_energy2["company_nm"] = year_energy2["electricity_enterprise2_company_nm"]
    year_energy2["menu_nm"] = year_energy2["electricity_enterprise2_menu_nm"]
    year_energy2["ratio"] = year_energy2["non_fossil_ratio2"]
    year_energy2["energy_amount_day"] = mul(
        year_energy2["energy_amount"], year_energy2["anbun_rate"]
    )
    year_energy2["energy_amount_night"] = mul(
        year_energy2["energy_amount_2"], year_energy2["anbun_rate"]
    )

    df = pd.concat([year_energy1, year_energy2])

    df_filter = df[(df["energy_amount_day"] > 0) | (df["energy_amount_night"] > 0)]
    result = df_filter[
        [
            "company_nm",
            "menu_nm",
            "ratio",
            "building_nm",
            "industrial_class_cd",
            "energy_amount_day",
            "energy_amount_night",
        ]
    ]

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def get_tokutei_netsuryo(company_um):
    """「燃料・熱」のデータを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 「燃料・熱」のデータ
    """
    # 調査表情報
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)
    # エネルギー使用実績明細(年別)
    year_energy_all = tables["year_energy"]
    # エネルギーマスタ
    energy_mst_all = tables["energy_mst"]
    energy_mst_AB = energy_mst_all[
        (energy_mst_all["energy_type_cd"].isin(["A", "B"]))
        & (energy_mst_all["other_flg"] == FLG_0)
    ]
    energy_mst_C = energy_mst_all[
        (energy_mst_all["energy_type_cd"] == "C")
        & (energy_mst_all["other_flg"] == FLG_0)
    ]

    df_fuel = year_energy_all.merge(
        ancate_info, on=["ancate_id", "report_nendo"], suffixes=("_year", "")
    ).merge(
        energy_mst_AB,
        left_on=["energy_id", "report_nendo"],
        right_on=["energy_id", "nendo"],
        suffixes=("", "_AB"),
    )
    df_fuel_ret = pd.DataFrame(
        {
            "id": ["AB"],
            "value": [
                (
                    mul(
                        df_fuel["energy_amount"],
                        df_fuel["new_energy_coefficient"],
                        df_fuel["co2_emission_factor"],
                        df_fuel["anbun_rate"],
                        44,
                    )
                    / 12
                ).sum()
            ],
            "hanbai_value": [
                (
                    mul(
                        df_fuel["sale_secondary_energy_amount"],
                        df_fuel["new_energy_coefficient"],
                        df_fuel["co2_emission_factor"],
                        df_fuel["anbun_rate"],
                        44,
                    )
                    / 12
                ).sum()
            ],
        }
    )

    df_heat = year_energy_all.merge(
        ancate_info, on=["ancate_id", "report_nendo"], suffixes=("_year", "")
    ).merge(
        energy_mst_C,
        left_on=["energy_id", "report_nendo"],
        right_on=["energy_id", "nendo"],
        suffixes=("", "_C"),
    )
    # 化石熱と非化石熱を同じエネルギーIDにする
    energy_id_map = {
        "C01": "C0102",
        "C02": "C0102",
        "C03": "C0304",
        "C04": "C0304",
        "C05": "C0506",
        "C06": "C0506",
        "C07": "C0708",
        "C08": "C0708",
    }
    # 熱エネルギーIDが対応にする
    df_heat["id"] = df_heat["energy_id"].map(energy_id_map).fillna(df_heat["energy_id"])
    df_heat["value"] = mul(
        df_heat["energy_amount"],
        # df_heat["new_energy_coefficient"],
        df_heat["anbun_rate"],
    )
    df_heat["hanbai_value"] = mul(
        df_heat["sale_secondary_energy_amount"],
        # df_heat["new_energy_coefficient"],
        df_heat["anbun_rate"],
    )

    df_heat_ret = (
        df_heat.groupby("id").agg({"value": "sum", "hanbai_value": "sum"}).reset_index()
    )

    result = pd.concat([df_fuel_ret, df_heat_ret])

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def get_tokutei_saibunrui_netsuryo(company_um):
    """燃料・熱の産業細分類データを取得する

    Args:
        company_um (str): 会社名略称

    Returns:
        list: 燃料・熱の産業細分類データ
    """
    # 調査表情報
    ancate_info = filter_ancate_info_by_anbun_rate(tables["ancate_info"], company_um)
    # エネルギー使用実績明細(年別)
    year_energy_all = tables["year_energy"]
    # エネルギーマスタ
    energy_mst_all = tables["energy_mst"]

    # 化石熱と非化石熱を同じエネルギーIDにする
    energy_id_map = {
        "C01": "C0102",
        "C02": "C0102",
        "C03": "C0304",
        "C04": "C0304",
        "C05": "C0506",
        "C06": "C0506",
        "C07": "C0708",
        "C08": "C0708",
    }
    df_sub = ancate_info.merge(
        year_energy_all, on=["ancate_id", "report_nendo"], suffixes=("", "_year")
    ).merge(
        energy_mst_all,
        left_on=["energy_id", "report_nendo"],
        right_on=["energy_id", "nendo"],
        suffixes=("", "_all"),
    )
    # 熱エネルギーIDが対応にする
    df_sub["energy_id"] = (
        df_sub["energy_id"].map(energy_id_map).fillna(df_sub["energy_id"])
    )

    df_AB = df_sub[
        (df_sub["energy_type_cd"].isin(["A", "B"])) & (df_sub["other_flg"] == FLG_0)
    ]
    df_AB["used"] = (
        mul(
            df_AB["energy_amount"],
            df_AB["anbun_rate"],
            df_AB["conversion_coefficient"],
            df_AB["co2_emission_factor"],
            44,
        )
        / 12
    )
    df_AB["sold"] = (
        mul(
            df_AB["sale_secondary_energy_amount"],
            df_AB["anbun_rate"],
            df_AB["conversion_coefficient"],
            df_AB["co2_emission_factor"],
            44,
        )
        / 12
    )
    df_AB_group = (
        df_AB.groupby("industrial_class_cd")
        .agg({"energy_id": lambda x: "AB", "used": "sum", "sold": "sum"})
        .reset_index()
    )

    df_C = df_sub[(df_sub["energy_type_cd"] == "C") & (df_sub["other_flg"] == FLG_0)]
    df_C["used"] = mul(
        df_C["energy_amount"],
        df_C["anbun_rate"],
    )
    df_C["sold"] = mul(
        df_C["sale_secondary_energy_amount"],
        df_C["anbun_rate"],
    )
    df_C_group = (
        df_C.groupby(["industrial_class_cd", "energy_id"])
        .agg({"used": "sum", "sold": "sum"})
        .reset_index()
    )
    result = pd.concat([df_AB_group, df_C_group])

    # turn DataFrame data to table
    table_data = list(result.to_records(index=False))

    return table_data


def unified_unit_string(unit_str):
    """調査表の単位表示とXML構造設計書のを統一する"""
    if unit_str == "kL":
        ret_unit_str = "ｋｌ"
    elif unit_str == "千m3":
        ret_unit_str = "千ｍ３"
    elif unit_str == "GJ":
        ret_unit_str = "ＧＪ"
    elif unit_str == "kw":
        ret_unit_str = "kW"
    else:
        ret_unit_str = unit_str

    return ret_unit_str


def general_round(x, decimals=0):
    """一般的な四捨五入を実現する"""
    if isinstance(x, Decimal):
        return np.floor(x * 10**decimals + Decimal(0.5)) / 10**decimals
    else:
        return np.floor(x * 10**decimals + 0.5) / 10**decimals


if __name__ == "__main__":
    output_intermediate_file()
