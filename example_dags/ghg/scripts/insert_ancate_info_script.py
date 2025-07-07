import math

import ghg.common.settings as Constants
import ghg.common.settings_ancate_info as AncateInfoConstants
import pandas as pd
from airflow.models import Variable
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.utils import (
    check_install_package,
    get_current_timestamp,
    get_file_from_hadoop,
    print_progress_bar,
)
from ghg.sql.ancate_info import INSERT_ANCATE_INFO
from ghg.sql.energy_used_record_month_detail import (
    INSERT_ENERGY_USED_RECORD_MONTH_DETAIL,
)
from ghg.sql.energy_used_record_year_detail import (
    INSERT_ENERGY_USED_RECORD_YEAR_DETAIL,
)
from ghg.sql.separate_coefficient import INSERT_SEPARATE_COEFFICIENT

logger = MyAppLog()

# Hive接続初期化
hive_connector = HiveConnector()

# 現在日時
current_timestamp = get_current_timestamp()


@log_writer(logger)
def insert_ancate_info(**kwargs):
    """
    関数名：調査表のデータ登録

    調査表情報DBへ登録する処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    try:
        logger.info("処理開始")

        # openpyxlをインストール
        check_install_package(Constants.PackageName.PANDAS_ENGINE.value)

        # Hadoop対象フォルダを指定
        base_path = Variable.get("GHG_HADOOP_BASE_PATH")
        sub_path = Variable.get("GHG_HADOOP_INPUTFILES_ANCATE_INFO_PATH")
        company_um = Variable.get("GHG_COMPANY_UM")

        # Hadoopから対象ファイルのBytesIOを取得
        files_io = get_file_from_hadoop(base_path, sub_path, company_um)

        ancate_info_record_list = []
        energy_used_record_month_detail_record_list = []
        energy_used_record_year_detail_record_list = []
        separate_coefficient_record_list = []
        total_files = len(files_io)
        file_count = 0

        for file_path, file_io in files_io.items():
            logger.info(f"処理対象: ファイル={file_path}")
            file_count += 1
            for sheet_name in AncateInfoConstants.SHEET_NAMES_ANCATE_INFO:
                logger.debug(f"処理対象: シート={sheet_name}")

                # dtype設定を取得
                dtype = get_dtype(sheet_name)

                # pandasを使用してExcelファイルを読み込む
                excel_data = pd.read_excel(
                    file_io,
                    sheet_name=sheet_name,
                    skiprows=1,
                    dtype=dtype,
                    engine=Constants.PackageName.PANDAS_ENGINE.value,
                )

                if excel_data.empty:
                    logger.warn(f"{sheet_name}シートにデータがありません")
                    continue

                # NaN値を""に変換
                pandas_df = excel_data.fillna("")
                # 改行コードの置換
                pandas_df = pandas_df.replace("\n", "", regex=True)

                # シート「基本情報_登録用」の場合
                if sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[0]:
                    # データが0件の場合
                    if pandas_df.empty:
                        logger.info(f"{sheet_name}シートのデータがありません")
                        continue

                    # 調査表情報の登録値作成
                    ancate_info_record_list_by_file = create_insert_ancate_info_values(
                        pandas_df
                    )
                    ancate_info_record_list.extend(ancate_info_record_list_by_file)

                # シート「エネルギー使用実績明細(月別)_登録用」の場合
                elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[1]:
                    # データが0件の場合
                    if pandas_df.empty:
                        logger.info(f"{sheet_name}シートのデータがありません")
                        continue

                    # エネルギー使用実績明細(月別)の登録値作成
                    energy_used_record_month_detail_record_list_by_file = (
                        create_insert_energy_used_record_month_detail_valuse(pandas_df)
                    )
                    energy_used_record_month_detail_record_list.extend(
                        energy_used_record_month_detail_record_list_by_file
                    )

                # シート「エネルギー使用実績明細(年別)_登録用」の場合
                elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[2]:
                    # データが0件の場合
                    if pandas_df.empty:
                        logger.info(f"{sheet_name}シートのデータがありません")
                        continue
                    # エネルギー使用実績明細(年別)の登録値作成
                    energy_used_record_year_detail_record_list_by_file = (
                        create_insert_energy_used_record_year_detail_valuse(pandas_df)
                    )
                    energy_used_record_year_detail_record_list.extend(
                        energy_used_record_year_detail_record_list_by_file
                    )

                # シート「個別係数_登録用」の場合
                elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[3]:
                    # データが0件の場合
                    if pandas_df.empty:
                        logger.info(f"{sheet_name}シートのデータがありません")
                        continue

                    # 個別係数の登録値作成
                    separate_coefficient_record_list_by_file = (
                        create_insert_separate_coefficient_valuse(pandas_df)
                    )
                    separate_coefficient_record_list.extend(
                        separate_coefficient_record_list_by_file
                    )

            print_progress_bar(file_count, total_files)

        if (
            not ancate_info_record_list
            or not energy_used_record_month_detail_record_list
            or not energy_used_record_year_detail_record_list
            or not separate_coefficient_record_list
        ):
            msg = "登録必要なデータがありません。"
            logger.error(msg)
            raise Exception(msg)

        # 調査表情報の登録
        logger.info("■調査表情報を登録開始")
        execute_insert_ancate_info(ancate_info_record_list)
        logger.info("■調査表情報を登録終了")

        # エネルギー使用実績明細(月別)の登録
        logger.info("■エネルギー使用実績明細(月別)を登録開始")
        execute_insert_energy_used_record_month_detail(
            energy_used_record_month_detail_record_list
        )
        logger.info("■エネルギー使用実績明細(月別)を登録終了")

        # エネルギー使用実績明細(年別)の登録
        logger.info("■エネルギー使用実績明細(年別)を登録開始")
        execute_insert_energy_used_record_year_detail(
            energy_used_record_year_detail_record_list
        )
        logger.info("■エネルギー使用実績明細(年別)を登録終了")

        # 個別係数の登録
        logger.info("■個別係数を登録開始")
        execute_insert_separate_coefficient(separate_coefficient_record_list)
        logger.info("■個別係数を登録終了")

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        # 接続を閉じる
        hive_connector.close_connection()
        logger.info("処理終了")


@log_writer(logger)
def format_record(record):
    formatted_record = []
    for r in record:
        if isinstance(r, str):
            formatted_record.append(f"'{r}'")
        else:
            formatted_record.append(str(r))
    record_str = "(" + ", ".join(formatted_record) + ")"
    return record_str


@log_writer(logger)
def create_insert_ancate_info_values(pandas_df):
    """
    関数名：調査表情報の登録値作成

    パラメータ:
        pandas_df:pandas DataFrameタイプのデータ

    戻り値:
        なし
    """
    record_list = []
    for index, row in pandas_df.iterrows():
        record = (
            row["ANCATE_ID"],
            row["REPORT_NENDO"],
            row["COMPANY_ID"],
            row["COMPANY_NM"],
            row["BUILDING_ID"],
            row["BUILDING_NM"],
            row["DEPT_NM"],
            row["REP_NM"],
            row["EXTENSION"],
            row["INDUSTRIAL_CLASS_CD"],
            row["POWER_AREA_CD"],
            row["POWER_AREA_NM"],
            row["POSTAL_CD"],
            row["PREFECTURE"],
            row["CITY"],
            row["CHOME_BEYOND"],
            row["COMPANY_OWNER_CD"],
            row["COMPANY_OWNER_NM"],
            row["POWER_DR_JOKO_CD"],
            row["DR_DATE"],
            row["GAS_COMPANY_ID"],
            row["GAS_COMPANY_NM"],
            row["HEAT_COMPANY_ID"],
            row["HEAT_COMPANY_NM"],
            row["LEASABLE_AREA_PG"],
            row["LEASABLE_AREA_HD"],
            row["LEASABLE_AREA_FP"],
            row["LEASABLE_AREA_EP"],
            row["LEASABLE_AREA_RP"],
            row["ANBUN_RATE_PG"],
            row["ANBUN_RATE_HD"],
            row["ANBUN_RATE_FP"],
            row["ANBUN_RATE_EP"],
            row["ANBUN_RATE_RP"],
            row["LAST_YEAR_CRUDE_OIL_EQUIVALENT"],
            row["LAST_YEAR_WATER_AMOUNT"],
            row["DENOMINATOR_TYPE"],
            row["DENOMINATOR_VALUE"],
            row["DAY_NIGHT_POWER_GRASP_FLAG"],
            row["SUBSTATION_EXIST_FLG"],
            row["SUBSTATION_ENERGY_GRASP_FLAG"],
            row["SUBSTATION_WATER_GRASP_FLAG"],
            row["SUBSTATION_FLOOR_AREA"],
            row["BUILDING_FLOOR_AREA"],
            row["SUBSTATION_FLOOR_RATE"],
            row["POWER_GENERATION_AMOUNT"],
            row["POWER_TRANSMISSION_AMOUNT"],
            row["ANCATE_COMMENT"],
            row["ENERGY_AMOUNT_DIFF_REASON"],
            row["WATER_AMOUNT_DIFF_REASON"],
            row["INFLOW_OUTFLOW_DIFF_REASON"],
            row["ENERGY_AMOUNT_RATE"],
            row["WATER_AMOUNT_RATE"],
            row["ELECTRICITY_ENTERPRISE1_COMPANY_ID"],
            row["ELECTRICITY_ENTERPRISE1_COMPANY_NM"],
            row["ELECTRICITY_ENTERPRISE1_MENU_CD"],
            row["ELECTRICITY_ENTERPRISE1_MENU_NM"],
            row["ELECTRICITY_ENTERPRISE1_CO2_CD"],
            row["NON_FOSSIL_RATIO1"],
            row["ELECTRICITY_ENTERPRISE2_COMPANY_ID"],
            row["ELECTRICITY_ENTERPRISE2_COMPANY_NM"],
            row["ELECTRICITY_ENTERPRISE2_MENU_CD"],
            row["ELECTRICITY_ENTERPRISE2_MENU_NM"],
            row["ELECTRICITY_ENTERPRISE2_CO2_CD"],
            row["NON_FOSSIL_RATIO2"],
            row["DELETE_FLG"],
            "TEPSYS",
            current_timestamp,
            "TEPSYS",
            current_timestamp,
        )

        logger.debug(f"■format前のrecord{index + 1}:{record}")
        record_str = format_record(record)
        logger.debug(f"■format後のrecord{index + 1}:{record_str}")
        record_list.append(record_str)

    return record_list


@log_writer(logger)
def execute_insert_ancate_info(record_list, batch_size=5000):
    """
    関数名：調査表情報の登録

    「基本情報_登録用」シートのデータは調査表情報テーブルへ登録する処理

    パラメータ:
        record_list:調査表情報の登録値リスト
        batch_size: 毎回実施件数

    戻り値:
        なし
    """
    total_records = len(record_list)
    batches = math.ceil(total_records / batch_size)

    for i in range(batches):
        start_index = i * batch_size
        end_index = min(start_index + batch_size, total_records)

        batch_records = record_list[start_index:end_index]

        insert_values = ", ".join(batch_records)
        insert_sql = INSERT_ANCATE_INFO(insert_values)
        logger.debug(insert_sql)

        try:
            hive_connector.execute_query(insert_sql)
            print_progress_bar(i + 1, batches)
        except Exception as e:
            logger.error(f"■Failed to insert batch {i + 1}/{batches}: {str(e)}")
            continue


@log_writer(logger)
def create_insert_energy_used_record_month_detail_valuse(pandas_df):
    """
    関数名：エネルギー使用実績明細(月別)の登録値作成

    パラメータ:
        pandas_df:pandas DataFrameタイプのデータ

    戻り値:
        なし
    """
    record_list = []
    for index, row in pandas_df.iterrows():
        record = (
            row["ANCATE_ID"],
            row["BUILDING_NM"],
            row["ENERGY_ID"],
            row["ENERGY_NAME"],
            row["REPORT_NENDO"],
            row["TARGET_MONTH"],
            row["INPUT_UNIT"],
            row["ENERGY_USAGE_AMOUNT"],
            row["DELETE_FLG"],
            "TEPSYS",
            current_timestamp,
            "TEPSYS",
            current_timestamp,
        )

        logger.debug(f"■format前のrecord{index + 1}:{record}")
        record_str = format_record(record)
        logger.debug(f"■format後のrecord{index + 1}:{record_str}")
        record_list.append(record_str)

    return record_list


@log_writer(logger)
def execute_insert_energy_used_record_month_detail(record_list, batch_size=5000):
    """
    関数名：エネルギー使用実績明細(月別)の登録

    「エネルギー使用実績明細(月別)」シートのデータはエネルギー使用実績明細(月別)テーブルへ登録する処理

    パラメータ:
        record_list:エネルギー使用実績明細(月別)の登録値リスト
        batch_size: 毎回実施件数

    戻り値:
        なし
    """
    total_records = len(record_list)
    batches = math.ceil(total_records / batch_size)

    for i in range(batches):
        start_index = i * batch_size
        end_index = min(start_index + batch_size, total_records)

        batch_records = record_list[start_index:end_index]

        insert_values = ", ".join(batch_records)
        insert_sql = INSERT_ENERGY_USED_RECORD_MONTH_DETAIL(insert_values)
        logger.debug(insert_sql)

        try:
            hive_connector.execute_query(insert_sql)
            print_progress_bar(i + 1, batches)
        except Exception as e:
            logger.error(f"■Failed to insert batch {i + 1}/{batches}: {str(e)}")
            continue


@log_writer(logger)
def create_insert_energy_used_record_year_detail_valuse(pandas_df):
    """
    関数名：エネルギー使用実績明細(年別)の登録値作成

    パラメータ:
        pandas_df:pandas DataFrameタイプのデータ

    戻り値:
        なし
    """
    record_list = []
    for index, row in pandas_df.iterrows():
        record = (
            row["ANCATE_ID"],
            row["BUILDING_NM"],
            row["ENERGY_ID"],
            row["ENERGY_NAME"],
            row["REPORT_NENDO"],
            row["OLD_ENERGY_COEFFICIENT"],
            row["NEW_ENERGY_COEFFICIENT"],
            row["REPORT_UNIT"],
            row["ENERGY_AMOUNT"],
            row["SALE_SECONDARY_ENERGY_AMOUNT"],
            row["EXTERNAL_SUPPLY_FUEL_AMOUNT"],
            row["UNUSED_HEAT_AMOUNT"],
            row["DELETE_FLG"],
            "TEPSYS",
            current_timestamp,
            "TEPSYS",
            current_timestamp,
        )

        logger.debug(f"■format前のrecord{index + 1}:{record}")
        record_str = format_record(record)
        logger.debug(f"■format後のrecord{index + 1}:{record_str}")
        record_list.append(record_str)

    return record_list


@log_writer(logger)
def execute_insert_energy_used_record_year_detail(record_list, batch_size=5000):
    """
    関数名：エネルギー使用実績明細(年別)の登録

    「エネルギー使用実績明細(年別)」シートのデータはエネルギー使用実績明細(年別)テーブルへ登録する処理

    パラメータ:
        record_list:エネルギー使用実績明細(年別)の登録値リスト
        batch_size: 毎回実施件数

    戻り値:
        なし
    """
    total_records = len(record_list)
    batches = math.ceil(total_records / batch_size)

    for i in range(batches):
        start_index = i * batch_size
        end_index = min(start_index + batch_size, total_records)

        batch_records = record_list[start_index:end_index]

        insert_values = ", ".join(batch_records)
        insert_sql = INSERT_ENERGY_USED_RECORD_YEAR_DETAIL(insert_values)
        logger.debug(insert_sql)

        try:
            hive_connector.execute_query(insert_sql)
            print_progress_bar(i + 1, batches)
        except Exception as e:
            logger.error(f"■Failed to insert batch {i + 1}/{batches}: {str(e)}")
            continue


@log_writer(logger)
def create_insert_separate_coefficient_valuse(pandas_df):
    """
    関数名：個別係数の登録値作成

    パラメータ:
        pandas_df:pandas DataFrameタイプのデータ

    戻り値:
        なし
    """
    record_list = []
    for index, row in pandas_df.iterrows():
        record = (
            row["ANCATE_ID"],
            row["ENERGY_ID"],
            row["ENERGY_NAME"],
            row["NENDO"],
            row["CONVERSION_COEFFICIENT"],
            row["DELETE_FLG"],
            "TEPSYS",
            current_timestamp,
            "TEPSYS",
            current_timestamp,
        )

        logger.debug(f"■format前のrecord{index + 1}:{record}")
        record_str = format_record(record)
        logger.debug(f"■format後のrecord{index + 1}:{record_str}")
        record_list.append(record_str)

    return record_list


@log_writer(logger)
def execute_insert_separate_coefficient(record_list, batch_size=5000):
    """
    関数名：個別係数の登録

    「個別係数の登録」シートのデータは個別係数テーブルへ登録する処理

    パラメータ:
        record_list:個別係数の登録値リスト
        batch_size: 毎回実施件数

    戻り値:
        なし
    """
    total_records = len(record_list)
    batches = math.ceil(total_records / batch_size)

    for i in range(batches):
        start_index = i * batch_size
        end_index = min(start_index + batch_size, total_records)

        batch_records = record_list[start_index:end_index]

        insert_values = ", ".join(batch_records)
        insert_sql = INSERT_SEPARATE_COEFFICIENT(insert_values)
        logger.debug(insert_sql)

        try:
            hive_connector.execute_query(insert_sql)
            print_progress_bar(i + 1, batches)
        except Exception as e:
            logger.error(f"■Failed to insert batch {i + 1}/{batches}: {str(e)}")
            continue


@log_writer(logger)
def get_dtype(sheet_name):
    dtype = {}
    # シート「基本情報_登録用」の場合
    if sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[0]:
        dtype = {
            "COMPANY_ID": str,
            "COMPANY_NM": str,
            "BUILDING_ID": str,
            "BUILDING_NM": str,
            "DEPT_NM": str,
            "REP_NM": str,
            "EXTENSION": str,
            "INDUSTRIAL_CLASS_CD": str,
            "POWER_AREA_CD": str,
            "POWER_AREA_NM": str,
            "POSTAL_CD": str,
            "PREFECTURE": str,
            "CITY": str,
            "CHOME_BEYOND": str,
            "COMPANY_OWNER_CD": str,
            "COMPANY_OWNER_NM": str,
            "POWER_DR_JOKO_CD": str,
            "GAS_COMPANY_ID": str,
            "GAS_COMPANY_NM": str,
            "HEAT_COMPANY_ID": str,
            "HEAT_COMPANY_NM": str,
            "DENOMINATOR_TYPE": str,
            "DAY_NIGHT_POWER_GRASP_FLAG": str,
            "SUBSTATION_EXIST_FLG": str,
            "SUBSTATION_ENERGY_GRASP_FLAG": str,
            "SUBSTATION_WATER_GRASP_FLAG": str,
            "ANCATE_COMMENT": str,
            "ENERGY_AMOUNT_DIFF_REASON": str,
            "WATER_AMOUNT_DIFF_REASON": str,
            "INFLOW_OUTFLOW_DIFF_REASON": str,
            "ELECTRICITY_ENTERPRISE1_COMPANY_ID": str,
            "ELECTRICITY_ENTERPRISE1_COMPANY_NM": str,
            "ELECTRICITY_ENTERPRISE1_MENU_CD": str,
            "ELECTRICITY_ENTERPRISE1_MENU_NM": str,
            "ELECTRICITY_ENTERPRISE1_CO2_CD": str,
            "ELECTRICITY_ENTERPRISE2_COMPANY_ID": str,
            "ELECTRICITY_ENTERPRISE2_COMPANY_NM": str,
            "ELECTRICITY_ENTERPRISE2_MENU_CD": str,
            "ELECTRICITY_ENTERPRISE2_MENU_NM": str,
            "ELECTRICITY_ENTERPRISE2_CO2_CD": str,
            "DELETE_FLG": str,
            "INSERT_NAME": str,
            "UPDATE_NAME": str,
        }
    # シート「エネルギー使用実績明細(月別)_登録用」の場合
    elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[1]:
        dtype = {
            "ANCATE_ID": str,
            "BUILDING_NM": str,
            "ENERGY_ID": str,
            "ENERGY_NAME": str,
            "INPUT_UNIT": str,
            "DELETE_FLG": str,
            "INSERT_NAME": str,
            "UPDATE_NAME": str,
        }
    # シート「エネルギー使用実績明細(年別)_登録用」の場合
    elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[2]:
        dtype = {
            "ANCATE_ID": str,
            "BUILDING_NM": str,
            "ENERGY_ID": str,
            "ENERGY_NAME": str,
            "OLD_ENERGY_COEFFICIENT": str,
            "NEW_ENERGY_COEFFICIENT": str,
            "REPORT_UNIT": str,
            "DELETE_FLG": str,
            "INSERT_NAME": str,
            "UPDATE_NAME": str,
        }
    # シート「個別係数_登録用」の場合
    elif sheet_name == AncateInfoConstants.SHEET_NAMES_ANCATE_INFO[3]:
        dtype = {
            "ANCATE_ID": str,
            "ENERGY_ID": str,
            "ENERGY_NAME": str,
            "DELETE_FLG": str,
            "INSERT_NAME": str,
            "UPDATE_NAME": str,
        }

    return dtype
