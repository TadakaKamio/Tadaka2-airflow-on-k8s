# import os
# import warnings

import time

import ghg.common.settings as Constants
import ghg.common.settings_ancate_info as AncateInfoConstants
import pandas as pd
import requests
from airflow.models import Variable
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.utils import (
    check_install_package,
    get_current_timestamp,
    get_file_from_hadoop,
)
from ghg.sql.ancate_info import INSERT_ANCATE_INFO
from ghg.sql.building_mst import SELECT_BUILDING_MST_BY_NAME
from requests.auth import HTTPBasicAuth

# import dicttoxml
# from bs4 import BeautifulSoup

logger = MyAppLog()

# Hive接続初期化
hive_connector = HiveConnector()


# @log_writer(logger)
# def insert_ancate_info(**kwargs):
#     try:
#         logger.debug("処理開始")

#         # 現在日時
#         current_timestamp = get_current_timestamp()

#         # openpyxlをインストール
#         check_install_package(Constants.PackageName.PANDAS_ENGINE)

#         # Hadoop対象フォルダを指定
#         base_path = Variable.get("GHG_HADOOP_BASE_PATH")
#         sub_path = Variable.get("GHG_HADOOP_INPUTFILES_ANCATE_INFO_PATH")
#         company_um = Variable.get("GHG_COMPANY_UM")

#         # Hadoopから対象ファイルのBytesIOを取得
#         files_io = get_file_from_hadoop(base_path, sub_path, company_um)

#         for file_path, file_io in files_io.items():
#             for sheet_name in AncateInfoConstants.SHEET_NAMES_ANCATE_INFO:
#                 logger.info(f"処理対象: ファイル={file_path}, シート={sheet_name}")

#                 # dtype設定を取得
#                 dtype = get_dtype(sheet_name)

#                 # pandasを使用してExcelファイルを読み込む
#                 excel_data = pd.read_excel(
#                     file_io,
#                     sheet_name=sheet_name,
#                     skiprows=1,
#                     dtype=dtype,
#                     engine=Constants.PackageName.PANDAS_ENGINE.value,
#                 )

#                 if excel_data.empty:
#                     logger.warn(f"{sheet_name}シートにデータがありません")
#                     continue

#                 # NaN値を""に変換
#                 pandas_df = excel_data.fillna("")
#                 # 改行コードの置換
#                 pandas_df = pandas_df.replace("\n", "", regex=True)

#                 # シート「基本情報_登録用」の場合
#                 if sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[0]:
#                     execute_insert_ancate_info(pandas_df, current_timestamp)

#         logger.debug("処理終了")

#     except Exception as e:
#         logger.error(f"エラーが発生しました: {e}")
#         raise e
#     finally:
#         # 接続を閉じる
#         hive_connector.close_connection()


# @log_writer(logger)
# def format_record(record):
#     formatted_record = []
#     for r in record:
#         if isinstance(r, str):
#             formatted_record.append(f"'{r}'")
#         else:
#             formatted_record.append(str(r))
#     record_str = "(" + ", ".join(formatted_record) + ")"
#     return record_str


# @log_writer(logger)
# def get_dtype(sheet_name):
#     dtype = {}
#     # シート「基本情報_登録用」の場合
#     if sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[0]:
#         dtype = {
#             "COMPANY_ID": str,
#             "COMPANY_NM": str,
#             "BUILDING_ID": str,
#             "BUILDING_NM": str,
#             "DEPT_NM": str,
#             "REP_NM": str,
#             "EXTENSION": str,
#             "INDUSTRIAL_CLASS_CD": str,
#             "POWER_AREA_CD": str,
#             "POWER_AREA_NM": str,
#             "POSTAL_CD": str,
#             "PREFECTURE": str,
#             "CITY": str,
#             "CHOME_BEYOND": str,
#             "COMPANY_OWNER_CD": str,
#             "COMPANY_OWNER_NM": str,
#             "POWER_DR_JOKO_CD": str,
#             "GAS_COMPANY_ID": str,
#             "GAS_COMPANY_NM": str,
#             "HEAT_COMPANY_ID": str,
#             "HEAT_COMPANY_NM": str,
#             "DENOMINATOR_TYPE": str,
#             "DAY_NIGHT_POWER_GRASP_FLAG": str,
#             "SUBSTATION_EXIST_FLG": str,
#             "SUBSTATION_ENERGY_GRASP_FLAG": str,
#             "SUBSTATION_WATER_GRASP_FLAG": str,
#             "ANCATE_COMMENT": str,
#             "ENERGY_AMOUNT_DIFF_REASON": str,
#             "WATER_AMOUNT_DIFF_REASON": str,
#             "INFLOW_OUTFLOW_DIFF_REASON": str,
#             "ELECTRICITY_ENTERPRISE1_COMPANY_ID": str,
#             "ELECTRICITY_ENTERPRISE1_COMPANY_NM": str,
#             "ELECTRICITY_ENTERPRISE1_MENU_CD": str,
#             "ELECTRICITY_ENTERPRISE1_MENU_NM": str,
#             "ELECTRICITY_ENTERPRISE1_CO2_CD": str,
#             "ELECTRICITY_ENTERPRISE2_COMPANY_ID": str,
#             "ELECTRICITY_ENTERPRISE2_COMPANY_NM": str,
#             "ELECTRICITY_ENTERPRISE2_MENU_CD": str,
#             "ELECTRICITY_ENTERPRISE2_MENU_NM": str,
#             "ELECTRICITY_ENTERPRISE2_CO2_CD": str,
#             "DELETE_FLG": str,
#             "INSERT_NAME": str,
#             "UPDATE_NAME": str,
#         }
#     # シート「エネルギー使用実績明細(月別)_登録用」の場合
#     elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[1]:
#         dtype = {
#             "ANCATE_ID": str,
#             "BUILDING_NM": str,
#             "ENERGY_ID": str,
#             "ENERGY_NAME": str,
#             "INPUT_UNIT": str,
#             "DELETE_FLG": str,
#             "INSERT_NAME": str,
#             "UPDATE_NAME": str,
#         }
#     # シート「エネルギー使用実績明細(年別)_登録用」の場合
#     elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[2]:
#         dtype = {
#             "ANCATE_ID": str,
#             "BUILDING_NM": str,
#             "ENERGY_ID": str,
#             "ENERGY_NAME": str,
#             "OLD_ENERGY_COEFFICIENT": str,
#             "NEW_ENERGY_COEFFICIENT": str,
#             "REPORT_UNIT": str,
#             "DELETE_FLG": str,
#             "INSERT_NAME": str,
#             "UPDATE_NAME": str,
#         }
#     # シート「個別係数_登録用」の場合
#     elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[3]:
#         dtype = {
#             "ANCATE_ID": str,
#             "ENERGY_ID": str,
#             "ENERGY_NAME": str,
#             "DELETE_FLG": str,
#             "INSERT_NAME": str,
#             "UPDATE_NAME": str,
#         }

#     return dtype


# @log_writer(logger)
# def execute_insert_ancate_info(pandas_df, current_timestamp):
#     """
#     関数名：調査表情報の登録

#     「基本情報_登録用」シートのデータは調査表情報テーブルへ登録する処理

#     パラメータ:
#         cursor:hiive接続
#         pandas_df:pandas DataFrameタイプのデータ
#         current_timestamp:システム日時

#     戻り値:
#         なし
#     """
#     record_list = []
#     for index, row in pandas_df.iterrows():
#         record = (
#             row["ANCATE_ID"],
#             row["REPORT_NENDO"],
#             row["COMPANY_ID"],
#             row["COMPANY_NM"],
#             row["BUILDING_ID"],
#             row["BUILDING_NM"],
#             row["DEPT_NM"],
#             row["REP_NM"],
#             row["EXTENSION"],
#             row["INDUSTRIAL_CLASS_CD"],
#             row["POWER_AREA_CD"],
#             row["POWER_AREA_NM"],
#             row["POSTAL_CD"],
#             row["PREFECTURE"],
#             row["CITY"],
#             row["CHOME_BEYOND"],
#             row["COMPANY_OWNER_CD"],
#             row["COMPANY_OWNER_NM"],
#             row["POWER_DR_JOKO_CD"],
#             row["DR_DATE"],
#             row["GAS_COMPANY_ID"],
#             row["GAS_COMPANY_NM"],
#             row["HEAT_COMPANY_ID"],
#             row["HEAT_COMPANY_NM"],
#             row["LEASABLE_AREA_PG"],
#             row["LEASABLE_AREA_HD"],
#             row["LEASABLE_AREA_FP"],
#             row["LEASABLE_AREA_EP"],
#             row["LEASABLE_AREA_RP"],
#             row["ANBUN_RATE_PG"],
#             row["ANBUN_RATE_HD"],
#             row["ANBUN_RATE_FP"],
#             row["ANBUN_RATE_EP"],
#             row["ANBUN_RATE_RP"],
#             row["LAST_YEAR_CRUDE_OIL_EQUIVALENT"],
#             row["LAST_YEAR_WATER_AMOUNT"],
#             row["DENOMINATOR_TYPE"],
#             row["DENOMINATOR_VALUE"],
#             row["DAY_NIGHT_POWER_GRASP_FLAG"],
#             row["SUBSTATION_EXIST_FLG"],
#             row["SUBSTATION_ENERGY_GRASP_FLAG"],
#             row["SUBSTATION_WATER_GRASP_FLAG"],
#             row["SUBSTATION_FLOOR_AREA"],
#             row["BUILDING_FLOOR_AREA"],
#             row["SUBSTATION_FLOOR_RATE"],
#             row["POWER_GENERATION_AMOUNT"],
#             row["POWER_TRANSMISSION_AMOUNT"],
#             row["ANCATE_COMMENT"],
#             row["ENERGY_AMOUNT_DIFF_REASON"],
#             row["WATER_AMOUNT_DIFF_REASON"],
#             row["INFLOW_OUTFLOW_DIFF_REASON"],
#             row["ENERGY_AMOUNT_RATE"],
#             row["WATER_AMOUNT_RATE"],
#             row["ELECTRICITY_ENTERPRISE1_COMPANY_ID"],
#             row["ELECTRICITY_ENTERPRISE1_COMPANY_NM"],
#             row["ELECTRICITY_ENTERPRISE1_MENU_CD"],
#             row["ELECTRICITY_ENTERPRISE1_MENU_NM"],
#             row["ELECTRICITY_ENTERPRISE1_CO2_CD"],
#             row["NON_FOSSIL_RATIO1"],
#             row["ELECTRICITY_ENTERPRISE2_COMPANY_ID"],
#             row["ELECTRICITY_ENTERPRISE2_COMPANY_NM"],
#             row["ELECTRICITY_ENTERPRISE2_MENU_CD"],
#             row["ELECTRICITY_ENTERPRISE2_MENU_NM"],
#             row["ELECTRICITY_ENTERPRISE2_CO2_CD"],
#             row["NON_FOSSIL_RATIO2"],
#             row["DELETE_FLG"],
#             "TEPSYS",
#             current_timestamp,
#             "TEPSYS",
#             current_timestamp,
#         )

#         logger.debug(f"■format前のrecord{index + 1}:{record}")
#         record_str = format_record(record)
#         logger.debug(f"■format後のrecord{index + 1}:{record_str}")
#         record_list.append(record_str)

#     insert_values = ", ".join(record_list)
#     insert_sql = INSERT_ANCATE_INFO(insert_values)
#     logger.debug(insert_sql)

#     hive_connector.execute_query(insert_sql)


# @log_writer(logger)
# def write_data_to_excel(df, file_path, sheet_name, start_row, start_col):
#     from openpyxl import load_workbook
#     from openpyxl.utils.dataframe import dataframe_to_rows
#
#     warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")
#
#     # Excelファイルを読み込む
#     try:
#         wb = load_workbook(file_path, keep_vba=True)
#     except Exception as e:
#         print(f"ファイルを読み込む際にエラーが発生しました: {e}")
#         return
#
#     # ワークシートを取得する
#     if sheet_name not in wb.sheetnames:
#         sheet = wb.create_sheet(sheet_name)
#     else:
#         sheet = wb[sheet_name]
#
#     results = [
#         ["1001", "Building A", "Electricity", "2024-01-01", 1000.5],
#         ["1002", "Building B", "Water", "2024-02-01", 300.0],
#         ["1003", "Building C", "Gas", "2024-03-01", 500.25],
#     ]
#     columns = ["ID", "Building Name", "Utility Type", "Date", "Usage"]
#
#     df = pd.DataFrame(results, columns=columns)
#     logger.debug(df)
#
#     # pandas DataFrameから行リストを生成する
#     rows = dataframe_to_rows(df, index=False, header=True)
#
#     for r_idx, row in enumerate(rows, start=start_row):
#         for c_idx, value in enumerate(row, start=start_col):
#             sheet.cell(row=r_idx, column=c_idx, value=value)
#
#     # 変更を保存してExcelファイルを閉じる
#     try:
#         wb.save(TEST_OUTPUT_FOLDER_PATH)
#     except Exception as e:
#         print(f"ファイルを保存する際にエラーが発生しました: {e}")
#     finally:
#         wb.close()
#
#     # app.quit()
#     print("処理終了")


# Excel出力のTest
# results = [
#     ["1001", "Building A", "Electricity", "2024-01-01", 1000.5],
#     ["1002", "Building B", "Water", "2024-02-01", 300.0],
#     ["1003", "Building C", "Gas", "2024-03-01", 500.25],
# ]
# columns = ["ID", "Building Name", "Utility Type", "Date", "Usage"]

# df = pd.DataFrame(results, columns=columns)
# logger.debug(df)

# write_data_to_excel(df, TEST_OUTPUT_FOLDER_PATH, SHEET_NAMES_ANCATE_INFO[0], 10, 2)

# jsonからXML出力のTest
# json_data = {
#     "book": {
#         "title": "Python Programming",
#         "author": "Example Author",
#         "published": "2021",
#         "price": 29.95,
#     }
# }

# xml_data = dicttoxml.dicttoxml(json_data, custom_root="top", attr_type=False)
# print(xml_data)
# soup = BeautifulSoup(xml_data, "xml")
# print(soup.prettify())


# def test_sqlite():
#     from ghg.common.test_utils import test_query

#     # results = test_query("select count(*) from ancate_info")
#     results = test_query("select count(*) from ancate_info", "fetchall")

#     for result in results or []:
#         logger.debug(result)


@log_writer(logger)
def test_hive_connect():
    select_sql = SELECT_BUILDING_MST_BY_NAME("千代田生命福島ビル")
    logger.debug(select_sql)

    results = hive_connector.execute_query(select_sql, Constants.DBoperation.FETCHALL)
    for result in results:
        logger.debug(result[0])


# @log_writer(logger)
# def test_load_excel_files_from_hadoop():
#     # base_path = "dtap://TenantStorage/ghg"
#     # sub_path = "/input_files/ancate_info"
#     # company_um = "ALL"
#
#     base_path = Variable.get("GHG_HADOOP_BASE_PATH")
#     sub_path = Variable.get("GHG_HADOOP_INPUTFILES_ANCATE_INFO_PATH")
#     company_um = Variable.get("GHG_COMPANY_UM")
#     excel_files = get_target_paths(base_path, sub_path, company_um)
#     logger.debug(excel_files)


# @log_writer(logger)
# def test_sql_1():
#     query_rationalization = """
#     SELECT
#         EUY.ANCATE_ID,
#         EUY.ENERGY_ID,
#         EUY.ENERGY_AMOUNT,
#         EUY.NEW_ENERGY_COEFFICIENT,
#         EUY.OLD_ENERGY_COEFFICIENT,
#         EUY.SALE_SECONDARY_ENERGY_AMOUNT,
#         EUY.UNUSED_HEAT_AMOUNT,
#         KM.KBN_CD,
#         KM.BUNRUI_CD
#     FROM
#         ENERGY_USED_RECORD_YEAR_DETAIL EUY
#         LEFT JOIN KUBUN_MST KM ON KM.KBN_CD = EUY.ENERGY_ID
#     WHERE
#         KM.BUNRUI_CD = '0015' OR EUY.ENERGY_ID IN ('D02', 'D05')
#     """
#     logger.debug(query_rationalization)

#     start_time = time.time()
#     results = hive_connector.execute_query(
#         query_rationalization, Constants.DBoperation.FETCHALL
#     )
#     end_time = time.time()
#     cost_time = end_time - start_time
#     logger.debug(f"■Execution time: {cost_time} seconds")

#     for result in results:
#         logger.debug(result)


# @log_writer(logger)
# def test_sql_2():
#     query_optimization = """
#     SELECT
#         AI.ANCATE_ID,
#         EUM.ENERGY_ID,
#         EUM.ENERGY_USAGE_AMOUNT,
#         RO.REQUIRE_OPTIMIZATION_COEFFICIENT,
#         AI.SUBSTATION_ENERGY_GRASP_FLAG,
#         AI.SUBSTATION_FLOOR_RATE
#     FROM
#         ENERGY_USED_RECORD_MONTH_DETAIL EUM
#         JOIN ANCATE_INFO AI ON AI.ANCATE_ID = EUM.ANCATE_ID
#         JOIN REQUIRE_OPTIMIZATION_COEFFICIENT_FOR_MONTH_MST RO ON RO.POWER_AREA_CD = AI.POWER_AREA_CD AND RO.REPORT_NENDO = AI.REPORT_NENDO AND RO.TARGET_MONTH = EUM.TARGET_MONTH
#     WHERE
#         EUM.ENERGY_ID IN ('D01', 'D03', 'D04', 'D06', 'D07', 'D08')
#     """
#     logger.debug(query_optimization)

#     start_time = time.time()
#     results = hive_connector.execute_query(
#         query_optimization, Constants.DBoperation.FETCHALL
#     )
#     end_time = time.time()
#     cost_time = end_time - start_time
#     logger.debug(f"■Execution time: {cost_time} seconds")

#     for result in results:
#         logger.debug(result)


# @log_writer(logger)
# def test_sql_3():
#     query_rationalization = """
#     SELECT
#         EUY.ANCATE_ID,
#         EUY.ENERGY_ID,
#         EUY.ENERGY_AMOUNT,
#         EUY.NEW_ENERGY_COEFFICIENT,
#         EUY.OLD_ENERGY_COEFFICIENT,
#         EUY.SALE_SECONDARY_ENERGY_AMOUNT,
#         EUY.UNUSED_HEAT_AMOUNT,
#         KM.KBN_CD,
#         KM.BUNRUI_CD
#     FROM
#         ENERGY_USED_RECORD_YEAR_DETAIL_PARQUET EUY
#         LEFT JOIN KUBUN_MST_PARQUET KM ON KM.KBN_CD = EUY.ENERGY_ID
#     WHERE
#         KM.BUNRUI_CD = '0015' OR EUY.ENERGY_ID IN ('D02', 'D05')
#     """
#     logger.debug(query_rationalization)

#     start_time = time.time()
#     results = hive_connector.execute_query(
#         query_rationalization, Constants.DBoperation.FETCHALL
#     )
#     end_time = time.time()
#     cost_time = end_time - start_time
#     logger.debug(f"■Execution time: {cost_time} seconds")

#     for result in results:
#         logger.debug(result)


# @log_writer(logger)
# def test_sql_4():
#     query_optimization = """
#     SELECT
#         AI.ANCATE_ID,
#         EUM.ENERGY_ID,
#         EUM.ENERGY_USAGE_AMOUNT,
#         RO.REQUIRE_OPTIMIZATION_COEFFICIENT,
#         AI.SUBSTATION_ENERGY_GRASP_FLAG,
#         AI.SUBSTATION_FLOOR_RATE
#     FROM
#         ENERGY_USED_RECORD_MONTH_DETAIL_PARQUET EUM
#         JOIN ANCATE_INFO_PARQUET AI ON AI.ANCATE_ID = EUM.ANCATE_ID
#         JOIN REQUIRE_OPTIMIZATION_COEFFICIENT_FOR_MONTH_MST_PARQUET RO ON RO.POWER_AREA_CD = AI.POWER_AREA_CD AND RO.REPORT_NENDO = AI.REPORT_NENDO AND RO.TARGET_MONTH = EUM.TARGET_MONTH
#     WHERE
#         EUM.ENERGY_ID IN ('D01', 'D03', 'D04', 'D06', 'D07', 'D08')
#     """
#     logger.debug(query_optimization)

#     start_time = time.time()
#     results = hive_connector.execute_query(
#         query_optimization, Constants.DBoperation.FETCHALL
#     )
#     end_time = time.time()
#     cost_time = end_time - start_time
#     logger.debug(f"■Execution time: {cost_time} seconds")

#     for result in results:
#         logger.debug(result)


# @log_writer(logger)
# def test_proself_upload():
#     # アップロードするファイルのパス
#     file_path = r"/usr/local/airflow/dags/gitdags/dags/ghg/files/input_files/ancate_info/HD/【HD】【建物毎に作成】エネルギー使用状況調査表.xlsm"
#     # file_path = r"C:\myWork\ESG情報開示システム\workspace\esg02\dags\ghg\files\input_files\ancate_info\HD\【HD】【建物毎に作成】エネルギー使用状況調査表.xlsm"

#     # アップロード先のURL
#     # url = "https://192.168.8.19:8080/05307_ESG-HD/調査表"
#     url = "https://fileshare.tepcube.jp//proself/weblink.go?/05307_ESG-HD/%E8%AA%BF%E6%9F%BB%E8%A1%A8"

#     # ファイルをバイナリモードで開く
#     with open(file_path, "rb") as file:
#         # PUTリクエストを送信
#         response = requests.put(
#             url,
#             auth=HTTPBasicAuth(
#                 "hongou-takuto@tepsys.co.jp", "@Online555"
#             ),  # ベーシック認証
#             data=file,
#             verify=False,
#         )

#     # レスポンスのステータスコードを確認
#     print(f"Status Code: {response.status_code}")
#     # レスポンスの本文を出力（エラーメッセージ等があれば表示される）
#     print(f"Response Body: {response.text}")

#     # response = requests.get(
#     #     _url, auth=HTTPBasicAuth(_auth["user"], _auth["password"]), verify=False
#     # )


@log_writer(logger)
def main(**kwargs):
    test_hive_connect()


if __name__ == "__main__":
    # select_building_mst()
    # test_sqlite()
    test_hive_connect()
    # test_proself_upload()
    # pass
