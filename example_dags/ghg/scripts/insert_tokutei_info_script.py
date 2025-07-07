import json

import pandas as pd
from airflow.models import Variable
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.settings import DBoperation, Number, PackageName
from ghg.common.settings_tokutei_info import (
    COL_RANGE_OF_TOKUTEI_LIST,
    LASTCOL_INDEX_OF_TOKUTEI_LIST,
    SHEET_NAMES_TOKUTEI_INFO,
)
from ghg.common.utils import (
    check_install_package,
    get_current_timestamp,
    get_file_from_hadoop,
    turn_excel_item_to_dict,
)
from ghg.sql.company_mst import SELECT_COMPANY_MST_BY_NAME
from ghg.sql.tokutei_info import INSERT_TOKUTEI_INFO

logger = MyAppLog()
# Hive接続
hive_connector = HiveConnector()


# 特定表のデータ登録
@log_writer(logger)
def insert_tokutei_info(**kwargs):
    """
    関数名：指定表のデータ登録

    指定表情報DBへ登録する処理

    パラメータ:
        companyNM

    戻り値:
        なし
    """

    try:
        logger.info("処理開始")

        # openpyxlのインストールをチェック
        check_install_package(PackageName.PANDAS_ENGINE.value)

        # airflowから変数の値を取得
        company_um = Variable.get("GHG_COMPANY_UM")

        # ファイル情報リストを取得
        excel_file_list = get_all_excel_file(company_um)

        for file_path, file_io in excel_file_list.items():
            # 特定表から各シートのデータを取得する
            tokutei_data = get_data_from_tokutei_file(file_path, file_io)

            # 特定表入力ツール側で処理できない・処理漏れの部分をこちらで修正する
            modify_tokutei_data(tokutei_data)

            # 現在のファイルのフォルダ名を読み取り
            company_um = file_path.split("/")[-2]

            # 取得のデータを「特定表情報」テーブルに登録する
            save_data_to_tokutei_info(tokutei_data, company_um)

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        # 接続を閉じる
        hive_connector.close_connection()
        logger.info("処理終了")


@log_writer(logger)
def get_company_id_by_companyUM(company_um):
    """会社名略称によって、会社IDを取得する

    Args:
        company_um (String): 会社名略称

    Raises:
        Exception: 会社IDが取得できなかった場合、エラーを出す
    """
    select_sql = SELECT_COMPANY_MST_BY_NAME(company_um)
    result = hive_connector.execute_query(select_sql, DBoperation.FETCHONE)

    if result is not None and len(result) > 0:
        return result[0]
    else:
        msg = (
            f"該当する会社名:「{company_um}」は会社マスタに関連する会社IDがありません。"
        )
        logger.error(msg)
        raise Exception(msg)


@log_writer(logger)
def get_all_excel_file(company_um):
    """固定フォルダから、全部Excelファイルを取得する

    Args:
        company_um (String): 会社名略称

    Returns:
        List: ファイル情報リスト
    """
    # Hadoop対象フォルダを指定
    base_path = Variable.get("GHG_HADOOP_BASE_PATH")
    sub_path = Variable.get("GHG_HADOOP_INPUTFILES_TOKUTEI_INFO_PATH")

    # Hadoopから対象ファイルのBytesIOを取得
    return get_file_from_hadoop(base_path, sub_path, company_um)


@log_writer(logger)
def get_data_from_tokutei_file(file_path, file_io):
    """特定表から各シートのデータを取得する

    Args:
        file_path (String): ファイルのパス
        file_io (BytesIO): ファイルIO

    Returns:
        List:特定表各シートのデータ
    """
    dict_list = []
    sheet_index = 0
    for sheet_name in SHEET_NAMES_TOKUTEI_INFO:
        logger.debug(f"処理対象: ファイル={file_path}, シート={sheet_name}")

        # pandasを使用してExcelファイルを読み込む
        excel_data = pd.read_excel(
            file_io,
            sheet_name=sheet_name,
            header=1,
            usecols=COL_RANGE_OF_TOKUTEI_LIST[sheet_index],
            engine=PackageName.PANDAS_ENGINE.value,
        )

        # NaN値をNoneに変換
        pandas_df = excel_data.applymap(lambda x: None if pd.isna(x) else x)

        dict_data, _ = turn_excel_item_to_dict(
            pandas_df, 0, 1, 0, LASTCOL_INDEX_OF_TOKUTEI_LIST[sheet_index]
        )

        if sheet_index == 2:
            tokutei2_dict_name_key(dict_data)

        dict_list.append(dict_data)
        sheet_index += 1

    return dict_list


@log_writer(logger)
def save_data_to_tokutei_info(data, company_um):
    """データを特定表情報テーブルに登録する

    Args:
        data (List): 登録用データ
        company_um (String): 会社名略称
    """

    current_timestamp = get_current_timestamp()

    record = (
        get_company_id_by_companyUM(company_um),  # 会社ID
        data[2]["Nendo"],  # 報告対象年度
        json.dumps(data[Number.NUMBER_0.value], ensure_ascii=False),  # 表紙
        json.dumps(data[Number.NUMBER_1.value], ensure_ascii=False),  # 第1表
        json.dumps(data[Number.NUMBER_2.value], ensure_ascii=False),  # 第2表
        json.dumps(data[Number.NUMBER_3.value], ensure_ascii=False),  # 第3表
        json.dumps(data[Number.NUMBER_4.value], ensure_ascii=False),  # 第4表
        json.dumps(data[Number.NUMBER_5.value], ensure_ascii=False),  # 第5表
        json.dumps(data[Number.NUMBER_6.value], ensure_ascii=False),  # 第6表
        json.dumps(data[Number.NUMBER_7.value], ensure_ascii=False),  # 第7表
        json.dumps(data[Number.NUMBER_8.value], ensure_ascii=False),  # 第8表
        json.dumps(data[Number.NUMBER_9.value], ensure_ascii=False),  # 第9表
        json.dumps(data[Number.NUMBER_10.value], ensure_ascii=False),  # 第10表
        json.dumps(data[Number.NUMBER_11.value], ensure_ascii=False),  # 第11表
        json.dumps(data[Number.NUMBER_12.value], ensure_ascii=False),  # 第12表
        "0",  # 削除フラグ
        "TEPSYS",  # 登録者
        current_timestamp,  # 登録日時
        "TEPSYS",  # 更新者
        current_timestamp,  # 更新日時
    )

    insert_sql = INSERT_TOKUTEI_INFO(record)

    hive_connector.execute_query(insert_sql)


@log_writer(logger)
def tokutei2_dict_name_key(dict_data):
    """
    関数名：特定表第2表辞書のキーの修正

    jsonのキーの修正する処理

    パラメータ:
        dict_data: 辞書データ

    戻り値:
        dict_data:修正後キーの辞書データ
    """

    # 化石燃料・化石燃料の小計・連携分のエネルギー使用量(熱量GJ)旧法の項目を追加すること
    dict_data["Netsuryo"]["Shokei_Nenryo"]["UchiRenkei_Shiyoryo_Gj_2023"] = None

    return dict_data


def modify_tokutei_data(data):
    """特定表から取得したデータを修正する"""
    table2 = data[Number.NUMBER_2.value]

    if "Saitekika_Denkiryo" in table2:
        del_item(table2["Saitekika_Denkiryo"], "Jikantaibetsu_Array")

    table3 = data[Number.NUMBER_3.value]
    # 第3表のエネルギー消費原単位(Gentani_Keisan)に
    # 事業分類明細Array(JigyoBunrui_Array)のソート順番を変わる
    table3["Gentani_Keisan"]["JigyoBunrui_Array"] = sort_jigyo_bunrui_array(
        table3["Gentani_Keisan"]["JigyoBunrui_Array"]
    )

    # 電気需要最適化評価原単位
    table3["Heijyunka_Gentani_Keisan"]["JigyoBunrui_Array"] = sort_jigyo_bunrui_array(
        table3["Heijyunka_Gentani_Keisan"]["JigyoBunrui_Array"]
    )


def sort_jigyo_bunrui_array(jigyo_bunrui_array):
    """Sort the list of dictionaries by the value of the key"""
    sorted_jiyobunrui_array = sorted(
        jigyo_bunrui_array, key=lambda x: x["JigyoBunrui"]["A"], reverse=True
    )

    # 事業分類明細Array(JigyoBunrui_Array)の連番を振
    for index, item in enumerate(sorted_jiyobunrui_array, start=1):
        item["JigyoBunrui"]["Renban"] = index

    return sorted_jiyobunrui_array


def del_item(d, key_to_remove):
    """Delete this element from the dictionary"""
    if key_to_remove in d:
        del d[key_to_remove]
