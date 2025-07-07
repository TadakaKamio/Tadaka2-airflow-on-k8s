import json
import re
from collections import OrderedDict

import pandas as pd
from airflow.models import Variable

import ghg.common.settings as Constants
import ghg.common.settings_shitei_info as ShiteiInfoConstants
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.utils import (
    check_install_package,
    get_current_timestamp,
    get_file_from_hadoop,
    round_to_str,
    turn_excel_item_to_dict,
)
from ghg.sql.building_mst import SELECT_BUILDING_MST_BY_NAME
from ghg.sql.company_mst import SELECT_COMPANY_MST_BY_NAME
from ghg.sql.shitei_info import INSERT_SHITEI_INFO

logger = MyAppLog()

# Hive接続初期化
hive_connector = HiveConnector()


@log_writer(logger)
def insert_shitei_info(**kwargs):
    """
    関数名：指定表のデータ登録

    指定表情報DBへ登録する処理

    パラメータ:
        なし

    戻り値:
        なし
    """

    try:
        logger.info("処理開始")

        # 現在日時
        current_timestamp = get_current_timestamp()

        # openpyxlをインストール
        check_install_package(Constants.PackageName.PANDAS_ENGINE.value)

        # Hadoop対象フォルダを指定
        base_path = Variable.get("GHG_HADOOP_BASE_PATH")
        sub_path = Variable.get("GHG_HADOOP_INPUTFILES_SHITEI_INFO_PATH")
        company_um = Variable.get("GHG_COMPANY_UM")

        # Hadoopから対象ファイルのBytesIOを取得
        files_io = get_file_from_hadoop(base_path, sub_path, company_um)

        for file_path, file_io in files_io.items():
            json_list = []
            result_dict = {}

            for sheet_name in ShiteiInfoConstants.SHEET_NAMES_SHITEI_INFO:
                logger.info(f"処理対象: ファイル={file_path}, シート={sheet_name}")

                # シート名中の数値を取得して、インデックスを作る
                sheet_index = int(re.findall(r"\d+", sheet_name)[0])

                if (
                    sheet_name == "STEP２（第１、2表）"
                    or sheet_name == "STEP２（第３表～）"
                ):
                    excel_step2_data = pd.read_excel(
                        file_io,
                        sheet_name=sheet_name,
                        header=1,
                        engine=Constants.PackageName.PANDAS_ENGINE.value,
                    )
                    pandas_df_step2 = excel_step2_data.applymap(
                        lambda x: None if pd.isna(x) else x
                    )

                    dict_data_value(
                        sheet_name,
                        pandas_df_step2,
                        result_dict,
                    )

                    continue

                # pandasを使用してExcelファイルを読み込む
                excel_data = pd.read_excel(
                    file_io,
                    sheet_name=sheet_name,
                    header=1,
                    usecols=ShiteiInfoConstants.COL_RANGE_OF_SHITEI_LIST[sheet_index],
                    engine=Constants.PackageName.PANDAS_ENGINE.value,
                )

                # NaN値をNoneに変換
                pandas_df = excel_data.applymap(lambda x: None if pd.isna(x) else x)

                # 指定－第８表選択(専ら事務所） or （工場等）jsonタグ表示、非表示
                itemData = {}
                # 項目名を取得key：Shitei_08_Kbn
                itemCD = pandas_df.iloc[0, 0]
                # 項目名を取得value："1"(専ら事務所） or "2"（工場等）
                itemValue = pandas_df.iloc[1, 0]
                # Shitei_08_Kbn = 2：（工場等）場合、"1"（専ら事務所）を出力なし。
                if sheet_index == 8 and itemValue == 2:
                    # 工場等における判断の基準の遵守状況
                    dict_data, _ = turn_excel_item_to_dict(pandas_df, 0, 1, 106, 272)
                    # 工場等に設置する発電専用設備又はコージェネレーション設備の発電効率等の状況に関し、参考となる情報Array
                    shitei_08_dict_data, _ = turn_excel_item_to_dict(
                        pandas_df, 0, 1, 273, 273
                    )
                    # 項目「指定－第８表選択：（Shitei_08_Kb:2)」を設定
                    itemData[itemCD] = itemValue
                    # 辞書は、プロジェクトの挿入順序を保持
                    itemData.update(dict_data)
                    itemData.update(shitei_08_dict_data)
                    # 指定表第８表のキーの修正
                    shitei8_dict_rename_key(itemData)
                    # 指定表第８表「設備に投入する排熱エネルギーの有無」修正
                    shitei8_dict_tonyu_ene_kbn(itemData)
                    dict_data = itemData

                # Shitei_08_Kbn = 1：（専ら事務所）場合、"2"（工場等）を出力なし。
                elif sheet_index == 8 and itemValue == 1:
                    # 専ら事務所その他これに類する用途に供する工場等における判断の基準の遵守状況
                    dict_data, _ = turn_excel_item_to_dict(pandas_df, 0, 1, 1, 105)
                    # # 工場等に設置する発電専用設備又はコージェネレーション設備の発電効率等の状況に関し、参考となる情報Array
                    shitei_08_dict_data, _ = turn_excel_item_to_dict(
                        pandas_df, 0, 1, 273, 273
                    )
                    # 項目「指定－第８表選択：（Shitei_08_Kb:1)」を設定
                    itemData[itemCD] = itemValue
                    # 辞書は、プロジェクトの挿入順序を保持
                    itemData.update(dict_data)
                    itemData.update(shitei_08_dict_data)
                    # 指定表第８表「設備に投入する排熱エネルギーの有無」修正
                    shitei8_dict_tonyu_ene_kbn(itemData)
                    dict_data = itemData
                else:
                    # 変換後確認
                    dict_data, _ = turn_excel_item_to_dict(
                        pandas_df,
                        0,
                        1,
                        0,
                        ShiteiInfoConstants.LASTCOL_INDEX_OF_SHITEI_LIST[sheet_index],
                    )

                if sheet_index == 2:
                    # 指定表第２表のキーの修正
                    shitei2_dict_rename_key(dict_data)
                    # XML構造設計書の項番(943)の辞書データ修正
                    clean_meisai_data(dict_data)
                    # 指定表第２表の該当年度を修正
                    shitei2_dict_nendo(dict_data)
                    # 指定表第２表の報告月を修正
                    shitei2_dict_houkoku_tuki(dict_data)
                    # 指定表第２表の対前年度比を修正
                    shitei2_dict_zennendo_hi(dict_data, result_dict)

                if sheet_index == 4:
                    # 指定表第4表の対前年度比を修正
                    shitei4_dict_zennendo_hi(dict_data, result_dict)

                if sheet_index == 5:
                    # 指定表第5表の対前年度比を修正
                    shitei5_dict_zennendo_hi(dict_data, result_dict)

                if sheet_index == 6:
                    # 指定表第6表の対前年度比を修正
                    shitei6_dict_zennendo_hi(dict_data, result_dict)

                json_data = json.dumps(dict_data, ensure_ascii=False)
                json_list.append(json_data)

            jsonList1 = json.loads(json_list[1])
            jsonList2 = json.loads(json_list[2])
            # 建物名称
            kojyo_nm = jsonList1.get("Shitei_Kojyo_Name")
            # 報告対象年度
            nendo = jsonList2.get("Nendo")

            params = {}
            params["kojyo_nm"] = kojyo_nm
            params["nendo"] = nendo

            if kojyo_nm is None:
                logger.error(
                    f"入力ファイル：「{file_path}」の建物名を取得できませんでした。"
                )
                continue

            # 建物マスタの検索
            building_results = execute_select_building_mst(params)

            if building_results is None:
                logger.error(
                    f"入力ファイル：「{file_path}」の該当する建物名:「{kojyo_nm}」は建物マスタに関連する建物IDがありません。"
                )
                continue

            params = {}
            company_um = file_path.split("/")[-2]
            params["company_um"] = company_um

            if company_um is None:
                logger.error(
                    f"入力ファイル：「{file_path}」の会社名略称を取得できませんでした。"
                )
                continue

            # 会社マスタを検索
            company_results = execute_select_company_mst(params)

            if company_results is None:
                logger.error(
                    f"入力ファイル：「{file_path}」の該当する会社名:「{company_um}」は会社マスタに関連する会社IDがありません。"
                )
                continue

            params = {}
            params["company_id"] = company_results[0]  # 会社ID
            params["building_id"] = building_results[0]  # 建物ID
            params["kojyo_nm"] = kojyo_nm  # 建物名称
            params["nendo"] = nendo  # 報告対象年度
            params["json_list"] = json_list  # 指定表第０表～第１０表のjsonリスト

            # 指定表情報の登録
            execute_insert_shitei_info(params, current_timestamp)

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        # 接続を閉じる
        hive_connector.close_connection()
        logger.info("処理終了")


@log_writer(logger)
def execute_select_building_mst(params):
    """
    関数名：建物マスタの検索

    建物マスタの検索処理

    パラメータ:
        params: パラメータ

    戻り値:
        なし
    """
    # 建物IDを取得
    select_sql = SELECT_BUILDING_MST_BY_NAME(params["kojyo_nm"])
    logger.debug(select_sql)

    building_results = hive_connector.execute_query(
        select_sql, Constants.DBoperation.FETCHONE
    )
    return building_results


@log_writer(logger)
def execute_select_company_mst(params):
    """
    関数名：会社マスタの検索

    会社マスタの検索処理

    パラメータ:
        params: パラメータ

    戻り値:
        なし
    """
    # 会社IDを取得
    select_sql = SELECT_COMPANY_MST_BY_NAME(params["company_um"])
    logger.debug(select_sql)

    company_results = hive_connector.execute_query(
        select_sql, Constants.DBoperation.FETCHONE
    )
    return company_results


@log_writer(logger)
def execute_insert_shitei_info(params, current_timestamp):
    """
    関数名：指定表情報の登録

    指定表情報の登録する処理

    パラメータ:
        params: パラメータ
        current_timestamp: 現在日時

    戻り値:
        なし
    """
    # 指定表第０表～第１０表のjsonリスト
    json_list = params["json_list"]

    record = (
        params["company_id"],  # 会社ID
        params["building_id"],  # 建物ID
        params["kojyo_nm"],  # 建物名称
        params["nendo"] + 1,  # 報告対象年度
        json_list[Constants.Number.NUMBER_0.value],  # 第0表
        json_list[Constants.Number.NUMBER_1.value],  # 第1表
        json_list[Constants.Number.NUMBER_2.value],  # 第2表
        json_list[Constants.Number.NUMBER_3.value],  # 第3表
        json_list[Constants.Number.NUMBER_4.value],  # 第4表
        json_list[Constants.Number.NUMBER_5.value],  # 第5表
        json_list[Constants.Number.NUMBER_6.value],  # 第6表
        json_list[Constants.Number.NUMBER_7.value],  # 第7表
        json_list[Constants.Number.NUMBER_8.value],  # 第8表
        json_list[Constants.Number.NUMBER_9.value],  # 第9表
        json_list[Constants.Number.NUMBER_10.value],  # 第10表
        "0",  # 削除フラグ
        "TEPSYS",  # 登録者
        current_timestamp,  # 登録日時
        "TEPSYS",  # 更新者
        current_timestamp,  # 更新日時
    )

    insert_sql = INSERT_SHITEI_INFO(record)
    logger.debug(insert_sql)

    hive_connector.execute_query(insert_sql)


@log_writer(logger)
def rename_keys_in_dict(data, key_mapping):
    """
    辞書のキーを再帰的にリネームします。

    パラメータ:
        data: 辞書データ
        key_mapping: キーのマッピング辞書 (古いキーを新しいキーにマッピング)

    戻り値:
        新しいキーで辞書データ
    """
    if isinstance(data, dict):
        return {
            key_mapping.get(k, k): rename_keys_in_dict(v, key_mapping)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        return [rename_keys_in_dict(item, key_mapping) for item in data]
    else:
        return data


@log_writer(logger)
def shitei2_dict_rename_key(dict_data):
    """
    指定表第2表辞書のキーの修正

    パラメータ:
        dict_data: 辞書データ

    戻り値:
        修正後キーの辞書データ
    """
    # 石油コースの辞書キーのマビック(左側は古キー、右側は新キー)
    sekiyuCoke_key_mapping = {
        "SekiyuCoke": "EneShurui",
        "EneShurui": "Tani",
        "Tani": "Shiyoryo",
        "Shiyoryo": "Shiyoryo_Gj",
        "Shiyoryo_Gj": "Shiyoryo_Gj_2023",
        "Shiyoryo_Gj_2023": "Kyokyuryo",
        "Kyokyuryo": "Kyokyuryo_Gj",
        "Kyokyuryo_Gj": "Kyokyuryo_Gj_2023",
        "Kyokyuryo_Gj_2023": "Hanbairyo",
        "Hanbairyo": "Hanbairyo_Gj",
        "Hanbairyo_Gj": "Hanbairyo_Gj_2023",
    }

    # 電気事業者・うち非化石の辞書キーのマビック(左側は古キー、右側は新キー)
    uchihikaseki_key_mapping = {"Dennkijigyosya": "UchiHikaseki"}

    # 上記以外の買電・オフサイト型PPA（重み付けあり）の辞書キーのマビック(左側は古キー、右側は新キー)
    ppa_weight_key_mapping = {
        "PPA_Weight": "EneShurui",
        "EneShurui": "Tani",
        "Tani": "Shiyoryo",
        "Shiyoryo": "Shiyoryo_Gj",
    }

    # 修正後の新しいキー(石油コース)を辞書に追加します
    dict_data["Netsuryo"]["SekiyuCoke"] = rename_keys_in_dict(
        dict_data["Netsuryo"]["SekiyuCoke"], sekiyuCoke_key_mapping
    )

    # 修正後の新しいキー(電気事業者・うち非化石)を辞書に追加します
    dict_data["Denki"]["Baiden"]["DenkiJigyosya"] = rename_keys_in_dict(
        dict_data["Denki"]["Baiden"]["DenkiJigyosya"], uchihikaseki_key_mapping
    )

    # 修正後の新しいキー(上記以外の買電・オフサイト型PPA（重み付けあり）)を辞書に追加します
    ofusaito_data = rename_keys_in_dict(
        dict_data["Denki"]["Baiden_Sonota"]["ofusaito"], ppa_weight_key_mapping
    )

    baiden_sonota_data = dict_data["Denki"]["Baiden_Sonota"]
    # 辞書は、プロジェクトの挿入順序を保持
    ordered_baiden_sonota = OrderedDict()
    ordered_baiden_sonota["PPA_NotWeight"] = baiden_sonota_data["PPA_NotWeight"]
    ordered_baiden_sonota["PPA_Weight"] = ofusaito_data
    ordered_baiden_sonota["Jikotakuso"] = baiden_sonota_data["Jikotakuso"]
    ordered_baiden_sonota["HokaJikotakuso"] = baiden_sonota_data["HokaJikotakuso"]
    ordered_baiden_sonota["SonotaBaiden_Array"] = baiden_sonota_data[
        "SonotaBaiden_Array"
    ]
    ordered_baiden_sonota["Tajigyojo"] = baiden_sonota_data["Tajigyojo"]

    dict_data["Denki"]["Baiden_Sonota"] = ordered_baiden_sonota

    return dict_data


@log_writer(logger)
def clean_meisai_data(dict_data):
    """
    XML構造設計書の項番(943)の辞書データ修正

    パラメータ:
        dict_data: 辞書データ

    戻り値:
        修正後の辞書データ
    """
    for hikaseki_wariai in dict_data["HikasekiWariai_Joho"]["HikasekiWariai_Array"]:
        meisai_array = hikaseki_wariai["HikasekiWariai"]["Meisai_Array"]
        # メニュー名が取得できない場合、このJSONデータでは、明細項目にキーは存在しますが、値が設定されていないことがあります。
        filtered_meisai_array = [
            meisai for meisai in meisai_array if meisai["Meisai"]["Menu"] is not None
        ]
        # 更新 Meisai_Array
        hikaseki_wariai["HikasekiWariai"]["Meisai_Array"] = filtered_meisai_array
    return dict_data


@log_writer(logger)
def shitei2_dict_nendo(dict_data):
    """
    指定表第2表「該当年度」の修正

    パラメータ:
        dict_data: 辞書データ

    戻り値:
        修正後の辞書データ
    """
    dict_data["Nendo"] = 2023
    return dict_data


@log_writer(logger)
def shitei2_dict_houkoku_tuki(dict_data):
    full_to_half = {
        "４月": 4,
        "５月": 5,
        "６月": 6,
        "７月": 7,
        "８月": 8,
        "９月": 9,
        "１０月": 10,
        "１１月": 11,
        "１２月": 12,
        "１月": 1,
        "２月": 2,
        "３月": 3,
    }

    # Tsukibetsu_Array"の項目をループする
    for item in dict_data["Saitekika_Denkiryo"]["Tsukibetsu_Array"]:
        month = item["Tsukibetsu"]["Houkoku_Tuki"]
        if month in full_to_half:
            # 再割り当て
            item["Tsukibetsu"]["Houkoku_Tuki"] = full_to_half[month]

    # Jikantaibetsu_Arrayの項目を修正する
    if "Jikantaibetsu_Array" in dict_data["Saitekika_Denkiryo"]:
        dict_data["Saitekika_Denkiryo"].pop("Jikantaibetsu_Array")

    return dict_data


@log_writer(logger)
def dict_data_value(sheet_name, pandas_df_step2, result_dict):

    if sheet_name == "STEP２（第１、2表）":
        if pandas_df_step2.iloc[299, 29] is not None:
            result_dict["cell_value1"] = round_to_str(pandas_df_step2.iloc[299, 29], 1)
        else:
            result_dict["cell_value1"] = "-"
    else:
        # STEP２（第３表～）
        if pandas_df_step2.iloc[105, 42] != "-":
            result_dict["cell_value2"] = round_to_str(
                pandas_df_step2.iloc[105, 42] * 100, 1
            )
        else:
            result_dict["cell_value2"] = "-"

        if pandas_df_step2.iloc[114, 45] != "-":
            result_dict["cell_value3"] = round_to_str(
                pandas_df_step2.iloc[114, 45] * 100, 1
            )
        else:
            result_dict["cell_value3"] = "-"

        if pandas_df_step2.iloc[121, 45] != "-":
            result_dict["cell_value4"] = round_to_str(
                pandas_df_step2.iloc[121, 45] * 100, 1
            )
        else:
            result_dict["cell_value4"] = "-"

        if pandas_df_step2.iloc[139, 23] != "-":
            result_dict["cell_value5"] = round_to_str(pandas_df_step2.iloc[139, 23], 1)
        else:
            result_dict["cell_value5"] = ""

        if pandas_df_step2.iloc[139, 30] != "-":
            result_dict["cell_value6"] = round_to_str(pandas_df_step2.iloc[139, 30], 1)
        else:
            result_dict["cell_value6"] = ""

        if pandas_df_step2.iloc[139, 38] != "-":
            result_dict["cell_value7"] = round_to_str(pandas_df_step2.iloc[139, 38], 1)
        else:
            result_dict["cell_value7"] = ""

        if pandas_df_step2.iloc[139, 46] != "-":
            result_dict["cell_value8"] = round_to_str(pandas_df_step2.iloc[139, 46], 1)
        else:
            result_dict["cell_value8"] = ""

        if pandas_df_step2.iloc[139, 52] != "-":
            result_dict["cell_value9"] = round_to_str(pandas_df_step2.iloc[139, 52], 1)
        else:
            result_dict["cell_value9"] = ""

        if pandas_df_step2.iloc[147, 23] != "-":
            result_dict["cell_value10"] = round_to_str(pandas_df_step2.iloc[147, 23], 1)
        else:
            result_dict["cell_value10"] = ""

        if pandas_df_step2.iloc[147, 30] != "-":
            result_dict["cell_value11"] = round_to_str(pandas_df_step2.iloc[147, 30], 1)
        else:
            result_dict["cell_value11"] = ""

        if pandas_df_step2.iloc[147, 38] != "-":
            result_dict["cell_value12"] = round_to_str(pandas_df_step2.iloc[147, 38], 1)
        else:
            result_dict["cell_value12"] = ""

        if pandas_df_step2.iloc[147, 46] != "-":
            result_dict["cell_value13"] = round_to_str(pandas_df_step2.iloc[147, 46], 1)
        else:
            result_dict["cell_value13"] = ""

        if pandas_df_step2.iloc[147, 52] != "-":
            result_dict["cell_value14"] = round_to_str(pandas_df_step2.iloc[147, 52], 1)
        else:
            result_dict["cell_value14"] = ""


@log_writer(logger)
def shitei2_dict_zennendo_hi(dict_data, result_dict):
    # 第２表の対前年度比を辞書に修正する
    dict_data["ZennendoHi"] = result_dict["cell_value1"]

    return dict_data


@log_writer(logger)
def shitei4_dict_zennendo_hi(dict_data, result_dict):
    # 第4表の対前年度比を辞書に修正する
    dict_data["Missetsu"]["ZennendoHi"] = result_dict["cell_value2"]

    return dict_data


@log_writer(logger)
def shitei5_dict_zennendo_hi(dict_data, result_dict):
    # 第5表のエネルギー消費原単位の対前年度比を辞書に修正する
    dict_data["Gentani"]["ZennendoHi"] = result_dict["cell_value3"]

    # 第5表の電気需要最適化評価原単位の対前年度比を辞書に修正する
    dict_data["Heijyunka_Gentani"]["ZennendoHi"] = result_dict["cell_value4"]

    return dict_data


@log_writer(logger)
def shitei6_dict_zennendo_hi(dict_data, result_dict):
    # 第6表のエネルギー消費原単位の変化状況・3年度前・対前年度比を辞書に修正する
    dict_data["Gentani"]["Henka_2"]["ZennendoHi"] = result_dict["cell_value5"]

    # 第6表のエネルギー消費原単位の変化状況・2年度前・対前年度比を辞書に修正する
    dict_data["Gentani"]["Henka_3"]["ZennendoHi"] = result_dict["cell_value6"]

    # 第6表のエネルギー消費原単位の変化状況・前年度・対前年度比を辞書に修正する
    dict_data["Gentani"]["Henka_4"]["ZennendoHi"] = result_dict["cell_value7"]

    # 第6表のエネルギー消費原単位の変化状況・該当年度・対前年度比を辞書に修正する
    dict_data["Gentani"]["Henka_5"]["ZennendoHi"] = result_dict["cell_value8"]

    # 第6表のエネルギー消費原単位の変化状況・平均原単位変化比を辞書に修正する
    dict_data["Gentani"]["Henka_Heikin"] = result_dict["cell_value9"]

    # 第6表の電気需要最適化評価原単位の変化状況・3年度前・対前年度比を辞書に修正する
    dict_data["Heijyunka"]["Henka_2"]["ZennendoHi"] = result_dict["cell_value10"]

    # 第6表の電気需要最適化評価原単位の変化状況・2年度前・対前年度比を辞書に修正する
    dict_data["Heijyunka"]["Henka_3"]["ZennendoHi"] = result_dict["cell_value11"]

    # 第6表の電気需要最適化評価原単位の変化状況・前年度・対前年度比を辞書に修正する
    dict_data["Heijyunka"]["Henka_4"]["ZennendoHi"] = result_dict["cell_value12"]

    # 第6表の電気需要最適化評価原単位の変化状況・該当年度・対前年度比を辞書に修正する
    dict_data["Heijyunka"]["Henka_5"]["ZennendoHi"] = result_dict["cell_value13"]

    # 第6表の電気需要最適化評価原単位の変化状況・平均原単位変化比を辞書に修正する
    dict_data["Heijyunka"]["Henka_Heikin"] = result_dict["cell_value14"]

    return dict_data


@log_writer(logger)
def shitei8_dict_rename_key(item_data):
    # 指定表第8表_対象項目４－２の辞書キーのマビック(左側は古キー、右側は新キー)
    kojyo_4_2_key_mapping = {
        "Netsu_Riyo": "NetsuRiyo",
        "BioMath_Suiso_Ammonia_Konsho": "BioMathSuisoAmmoniaKonsho",
        "Fukuseibutsu_Konsho": "FukuseibutsuKonsho",
    }

    # 指定表第8表_対象項目４－３の辞書キーのマビック(左側は古キー、右側は新キー)
    kojyo_4_3_key_mapping = {
        "Netsu_Riyo": "NetsuRiyo",
        "BioMath_Suiso_Ammonia_Konsho": "BioMathSuisoAmmoniaKonsho",
        "Fukuseibutsu_Konsho": "FukuseibutsuKonsho",
    }

    # 修正後の新しいキー(対象項目４－２)を辞書に追加します
    item_data["Kojyo"]["Kojyo_4_2"]["Unten"] = rename_keys_in_dict(
        item_data["Kojyo"]["Kojyo_4_2"]["Unten"], kojyo_4_2_key_mapping
    )

    # 修正後の新しいキー(対象項目４－３)を辞書に追加します
    item_data["Kojyo"]["Kojyo_4_3"]["Unten"] = rename_keys_in_dict(
        item_data["Kojyo"]["Kojyo_4_3"]["Unten"], kojyo_4_3_key_mapping
    )

    # 修正後の新しいキー(対象項目６－２)を辞書に追加します
    shinsetsu_value = item_data["Kojyo"]["Kojyo_6_2"]["Hoshu"].pop("Shinsetsu")
    item_data["Kojyo"]["Kojyo_6_2"]["Shinsetsu"] = shinsetsu_value

    return item_data


@log_writer(logger)
def shitei8_dict_tonyu_ene_kbn(item_data):
    if (
        item_data["Hatsudenkoritsu_Sanko_Array"][0]["Hatsudenkoritsu_Sanko"][
            "Tonyu_Ene_Kbn"
        ]
        == 2
    ):
        item_data["Hatsudenkoritsu_Sanko_Array"][0]["Hatsudenkoritsu_Sanko"][
            "Tonyu_Ene_Kbn"
        ] = 0
    return item_data


@log_writer(logger)
def get_shiyoryo_gj_value(data, *keys):
    """辞書からShiyoryo_Gjの値を取得し、存在しない場合は0を返す"""
    try:
        value = data
        for key in keys:
            value = value[key]
        return value if value is not None else 0
    except KeyError:
        return 0


if __name__ == "__main__":
    insert_shitei_info()
