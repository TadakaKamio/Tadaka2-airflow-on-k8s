import base64
import datetime
import os
import tempfile
import time
import traceback
from io import BytesIO


# from airflow.models import Variable
import middle.common.constants_colums as constants_colums
import middle.common.log as log
import middle.common.utils as utils
import middle.report_register.register_inputdata.register_aggregation_Info as rai
import middle.report_register.register_inputdata.register_inputdata_info as rii
from middle.common.hive_connect import ImpalaSingleton
from middle.common.utils import get_json_config
from middle.report_register.common.CommonMasterDataLoader import CommonMasterDataLoader
from middle.report_register.register_inputdata.excel_files_parsing import (
    parse_excel_file,
)

# ▼▼▼▼▼▼▼▼▼符号定数群▼▼▼▼▼▼▼▼▼
DOT = constants_colums.SpecialChars.DOT.value
BLANK = constants_colums.SpecialChars.BLANK.value
HYPHEN = constants_colums.SpecialChars.HYPHEN.value
SLASH = constants_colums.SpecialChars.LINUX_PATH_DELIMITER.value

# ▼▼▼▼▼▼▼▼▼識別用文字列群▼▼▼▼▼▼▼▼▼
# "事業所"
OFFICE_STRING = constants_colums.StringOfExcelFile.OFFICE.value
# "入力シート"
INPUT_SHEET_STRING = constants_colums.StringOfExcelFile.INPUT_SHEET.value
# "設定"
SETTING_STRING = constants_colums.StringOfExcelFile.SETTING.value

# ▼▼▼▼▼▼▼▼▼共通オブジェクト群▼▼▼▼▼▼▼▼▼
# 設定ファイルからDB情報取得する
json_config = utils.get_json_config()
schema_middle = json_config["database_posgre"]["schema_middle"]
# 実行モード
run_mode = constants_colums.RunMode.DEV.value
# log出力用オブジェクト
logger = log.MiddleAppLog()
# システム操作時タイムスタンプ取得
current_timestamp = utils.get_current_timestamp()

# 発行する建物ID格納用リスト
building_id_list = []
# エラーファイル対象格納リスト
error_filenames = {}

input_files = {}


@log.log_writer(logger)
def save_input_data(postgre_conn, input_file_name, input_file_content, user_id):
    print("------------TDH蓄積処理開始------------")
    file_content_bytes = base64.b64decode(input_file_content)  # バイト列にデコード
    file_content_io = BytesIO(file_content_bytes)  # BytesIOオブジェクトに変換
    input_files[input_file_name] = file_content_io

    temp_dir = tempfile.gettempdir()  # 一時ディレクトリを取得
    temp_local_path = os.path.join(temp_dir, input_file_name)
    with open(temp_local_path, "wb") as temp_file:
        temp_file.write(file_content_io.read())

    # # ファイルを保存する関数を呼び出す
    # save_file(temp_local_path, input_file_name)

    # 処理する入力シートファイル一覧取得
    start_time = time.time()

    end_time = time.time()
    utils.get_process_time(start_time, end_time, "入力ファイル取得")

    # Excelファイル解析処理
    register_df_dic = {}
    try:
        # input_files = [r'C:\Users\msduser\Desktop\20250306_テスト\行員向け入力シート_テスト一銀行_テスト一株式会社_2024_1.xlsx']
        register_df_dic = parse_excel_file(postgre_conn, input_files, user_id)

    except Exception as e:
        logger.error("ファイルETL処理失敗しました。")
        logger.error(traceback.format_exc())
        raise e

    # TDH登録処理
    try:
        if register_df_dic is None or len(register_df_dic) <= 0:
            logger.error("処理する対象データは取得されていないため、処理を中止する。")
            return
        print("------------postgre生データTDH蓄積処理開始------------")
        # 生データ登録
        basic_df, corporate_df, building_df, energy_df, file_name = (
            rii.register_input_data(postgre_conn, register_df_dic)
        )
        print("------------postgre生データTDH蓄積処理完了------------")

        print("------------postgre集計データTDH蓄積処理開始------------")
        # 集計データ登録
        (
            corporation_df,
            corporationProfileEntity_df,
            corporationMonthlyEntity_df,
            corporationYearlyEntity_df,
        ) = rai.register_energy_aggregation_info(
            postgre_conn, basic_df, corporate_df, building_df, energy_df, file_name
        )
        print("------------postgre集計データTDH蓄積処理完了------------")
        postgre_conn.commit()
        print("------------postreへの登録完了------------")

    except Exception as e:

        logger.error("Postgresへの登録が失敗し、企業カルテの蓄積処理失敗しました。")
        logger.error(traceback.format_exc())

        postgre_conn.rollback()

        with postgre_conn:
            with postgre_conn.cursor() as cursor:
                cursor.execute(
                    "SELECT MAX(building_id) AS max_building_id FROM db_corp.t_report_storage_info WHERE file_id = 'REG_ERR'"
                )
                result = cursor.fetchone()

                max_err_seq = result[0][-6:] if result[0] is not None else 0
                new_err_seq = int(max_err_seq) + 1
                err_seq_str = str(new_err_seq).zfill(6)

                insert_sql = f"""
                    INSERT INTO db_corp.t_report_storage_info 
                    (
                      bank_code 
                    , bank_name 
                    , branch_code 
                    , branch_name 
                    , corporate_number 
                    , corporation_name 
                    , user_code 
                    , user_name 
                    , building_id 
                    , fiscal_year 
                    , report_type 
                    , registration_seq 
                    , file_id 
                    , creation_datetime 
                    , report_status
                    , delete_flg
                    )
                    VALUES
                    (
                      '-' 
                    , '-' 
                    , '-' 
                    , '-' 
                    , '-' 
                    , '{input_file_name}' 
                    , '-' 
                    , '-' 
                    , 'REG_ERR_{err_seq_str}' 
                    , '-' 
                    , '-' 
                    , 0 
                    , 'REG_ERR' 
                    , '{(datetime.datetime.now() + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M:%S")}'
                    , '8'
                    , FALSE
                    )
                """

                cursor.execute(insert_sql)
            postgre_conn.commit()

        raise e

    # Hiveへの蓄積
    try:

        config = get_json_config()  # 設定値を取得
        # hive connect接続
        hive_connect_singleton = hive_conn = None  # postgre接続インスタンス
        hive_connect_singleton = ImpalaSingleton(
            config["database_hive"]["user"], config["database_hive"]["password"]
        )

        # # コネクション取得
        hive_conn = hive_connect_singleton._connection
        print("------------hive生データTDH蓄積処理開始------------")
        # hiveへ生データ登録
        rii.insert_input_info_hive(hive_conn, basic_df, file_name)
        print("------------hive生データTDH蓄積処理完了------------")

        print("------------hive集計データTDH蓄積処理開始------------")
        # hiveへ生データ登録
        rai.register_to_hive(
            hive_conn,
            corporation_df,
            corporationProfileEntity_df,
            corporationMonthlyEntity_df,
            corporationYearlyEntity_df,
            file_name,
        )
        print("------------hive集計データTDH蓄積処理完了------------")
        hive_conn.commit()
        print("------------hiveへの登録完了------------")

    except Exception as e:

        logger.error("TDH登録が失敗し、企業カルテの蓄積処理失敗しました。")
        logger.error(traceback.format_exc())
        raise e
    finally:
        hive_connect_singleton.close_connection()

    print("------------TDH蓄積処理完了------------")


def get_mst_data(conn):
    """
    マスタデータ取得
    params:
        conn Hive接続し
    return:
        jic_mst  業種マスタ
        ec_mst   電力会社排出係数マスタ
    """
    jic_mst = ec_mst = cal_mst = None

    # masterデータ格納オブジェクト
    master_data = CommonMasterDataLoader(conn)
    # 区分マスタ
    # kbn_mst = master_data.kbnmst_list
    # 業種マスタ
    jic_mst = master_data.jicmst_list
    # 電力会社の排出係数マスタ
    ec_mst = master_data.ecmst_list

    cal_mst = master_data.calmst_list

    return jic_mst, ec_mst, cal_mst


def save_file(local_file_path, filename):
    put_base_path = "dtap://TenantStorage"
    put_dir_path = "/corp/input_sheet_files"

    try:
        put_path = get_put_path(put_base_path, put_dir_path, filename)
        print(f"★{put_path}★★{local_file_path}")
        put_out = put_file(local_file_path, put_path)
        if put_out.returncode != 0:
            msg = f"put_file is failed. file name is {local_file_path}. put path is {put_path}. stdout is {put_out}"
            raise Exception(msg)

    except Exception as e:
        print("put失敗★")
        raise e

    return True


def put_file(_local_path, _put_path):
    import subprocess

    out = subprocess.run(
        ["hadoop", "fs", "-put", _local_path, _put_path], capture_output=True
    )
    return out


def make_folder(_full_path):
    import subprocess

    out = subprocess.run(
        ["hdfs", "dfs", "-mkdir", "-p", _full_path], capture_output=True
    )
    return out


def get_put_path(*_path_list):
    import os

    _path_list = [_path[1:] if _path[0] == "/" else _path for _path in _path_list]
    _path_list = [
        _path[:-1] if ((_path[-1] == "/") and (_path[-3:] != "://")) else _path
        for _path in _path_list
    ]
    return os.path.join(*_path_list)
