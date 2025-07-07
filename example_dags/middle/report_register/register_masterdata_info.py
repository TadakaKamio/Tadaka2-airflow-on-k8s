import pandas as pd
import os, traceback
from pyhive.exc import DatabaseError
from airflow.models import Variable
import middle.common.utils as utils
import middle.common.log as log
import middle.common.constants_colums as constants
from middle.common.hive_connect import ImpalaSingleton
from middle.common.hql_processor import (
    insert_data,
    load_csv_to_mst
)

# loogerオブジェクト取得
logger = log.MiddleAppLog()

# "." "" "-"
DOT = constants.SpecialChars.DOT.value
BLANK = constants.SpecialChars.BLANK.value
HYPHEN = constants.SpecialChars.HYPHEN.value

# システム操作時タイムスタンプ取得
current_timestamp = utils.get_current_timestamp()

# データ登録処理実行者
creator_name = utils.get_sysuser()

# データベース名取得する
json_config = utils.get_json_config()
schema_commom = json_config["database_posgre"]["schema_commom"]
tdh_file_base_path = json_config['tdh_file_base_path']

# rootパス取得
project_root_path = utils.get_project_root_path()

@log.log_writer(logger)
def insert_masterdata(*args, **kwargs):
    """ 法人ミドル側利用するマスタデータをDWHへ登録する"""
    # 実行モード
    run_mode = constants.RunMode.DEV.value \
        if os.environ.get("MIDDLE_RUN_MODE") is None else os.environ.get("MIDDLE_RUN_MODE")

    # excelファイル処理用ライブラリopenpyxlをインストール
    utils.install_package('openpyxl')

    logger.info(f"★★★マスタデータの登録処理を開始します。★★★")    
    hive_connect_singleton = conn = None  # hive接続インスタンス
    if run_mode == constants.RunMode.PROD.value:
        # Hive connect接続
        hive_connect_singleton = ImpalaSingleton()
        # コネクション取得
        conn = hive_connect_singleton._connection

    base_path = Variable.get("middle_download_put_base_path")
    sub_path =  Variable.get("middle_download_put_masterfiles_path")
    
    # Hadoopから対象ファイルのBytesIOを取得
    excel_files = utils.get_file_from_hadoop(base_path, sub_path, None)

    # ファイル存在チェック
    if (excel_files is None or len(excel_files) == 0):
        msg = "登録もしくは更新するマスタデータファイルはないため、処理中止します。"
        logger.info(msg)
        return 
    
    # ファイル数分処理を繰り返す読み込み
    for file_path, excel_file in excel_files.items():
        logger.debug(f"★処理中マスタファイル名： {excel_file}★")
        master_table_name = None
        
        # Excelファイル内の全シート名を取得
        file = pd.ExcelFile(excel_file)
        sheet_names = file.sheet_names

        # データ確認
        try:
            # シート数分を繰り返す
            for sheet_name in sheet_names:
                data_by_sheet = {}
                if constants.MasterTable.JICMST.name == sheet_name: # JIMSTのテーブル名が長すぎるので、ここはenum.nameを利用しています
                    # 業種マスタのカラム情報とテーブル情報
                    master_table_columns = constants.JICMST_COLUMNS
                    master_table_name = 'DB' + DOT + constants.MasterTable.JICMST.value
                
                elif constants.MasterTable.CCMST.value == sheet_name:
                    # 換算係数マスタのカラム情報とテーブル情報
                    master_table_columns = constants.CCMST_COLUMNS
                    master_table_name = 'DB' + DOT + constants.MasterTable.CCMST.value
                
                elif sheet_name.startswith(constants.MasterTable.ECMST.value) :
                    # 排出係数マスタのカラム情報とテーブル情報
                    master_table_columns = constants.ECMST_COLUMNS
                    master_table_name = 'DB' + DOT + constants.MasterTable.ECMST.value
                
                else:
                    # 追加のマスタ登録が発生の場合対応する
                    pass
                
                # シート上マスタデータ取得
                master_data_df = file.parse(sheet_name)

                # nanを空文字に変換 
                master_data_df.fillna(BLANK, inplace=True)
                # '-'を空文字に変換
                master_data_df.replace(HYPHEN, BLANK, inplace=True)

                # excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者)
                table_mainten_columns_data =(None,None,f'{current_timestamp}',f'{creator_name}')

                master_data_array = []
                # シート上マスタデータレコード数分を繰り返して、メンテ用カラム情報追加
                for row in master_data_df.values:
                    row_tuple = tuple(row) + table_mainten_columns_data
                    master_data_array.append(row_tuple)
                
                data_by_sheet[sheet_name] = master_data_array
                partition_dict = None

                # TODO PH!仮対応
                if run_mode == constants.RunMode.DEV.value:
                    #開発環境仮対応

                    # csvファイル出力
                    utils.tocsv(utils.toDf(master_data_array), None, sheet_name)
                else:
                    # 本番環境対応
                    # マスタデータ登録用insert hql呼び出す
                    insert_data(conn,master_data_array, master_table_columns, partition_dict, master_table_name, sheet_name)
                
        except DatabaseError as e:
            error_message = traceback.format_exc()
            error_line = str(e.__traceback__.tb_lineno) 
            logger.error(f"{excel_file} : DatabaseError occurred at line {error_line}: {error_message}")
        
        except Exception as e:
            error_message = traceback.format_exc()
            error_line = str(e.__traceback__.tb_lineno) 
            logger.error(f"{excel_file} : Error occurred at line {error_line}: {error_message}")
        
        finally:
            # リソースのクリーンアップ
            # connectionをクローズする
            if conn:
                hive_connect_singleton.close_connection()
            # 処理対象ファイルクローズする
            file.close()

def register_mst_data_from_csv():
    # 実行モード
    run_mode = constants.RunMode.DEV.value \
        if os.environ.get("MIDDLE_RUN_MODE") is None else os.environ.get("MIDDLE_RUN_MODE")

    logger.info(f"★★★マスタデータの登録処理を開始します。★★★")    
    hive_connect_singleton = conn = None  # hive接続インスタンス
    if run_mode == constants.RunMode.PROD.value:
        # Hive connect接続
        hive_connect_singleton = ImpalaSingleton()
        # コネクション取得
        conn = hive_connect_singleton._connection

    base_path = Variable.get("middle_download_put_base_path")
    sub_path =  Variable.get("middle_download_put_masterfiles_path")
    
    # Hadoopから対象ファイルのBytesIOを取得
    csv_files = utils.get_file_from_hadoop(base_path, sub_path, None)

    # ファイル存在チェック
    if (csv_files is None or len(csv_files) == 0):
        msg = "登録もしくは更新するマスタデータファイルはないため、処理中止します。"
        logger.info(msg)
        return 
    
    # ファイル数分処理を繰り返す読み込み
    for csv_file_path, csv_file in csv_files.items():
        
        #ファイル名取得（拡張し含む）
        file_name, file_extension = os.path.splitext(os.path.basename(csv_file_path))
        csv_file_name = file_name + file_extension

        if not csv_file_name.endswith(constants.ExcelExtension.CSV.value): continue

        # dtap:TenantStorage/middle/masterfiles
        full_csv_path = utils.pathjoin(tdh_file_base_path, sub_path, csv_file_name)
        fs_prefix = "hdfs:///"
        full_csv_path = fs_prefix + full_csv_path
        # テーブル名とファイル名は一緒
        master_table_name = schema_name + DOT + file_name

        logger.info(f"★処理中マスタファイル名： {csv_file_name}★")

        # データ確認
        try:
            load_csv_to_mst(conn, full_csv_path, master_table_name)
        except DatabaseError as e:
            error_message = traceback.format_exc()
            error_line = str(e.__traceback__.tb_lineno) 
            logger.error(f"{csv_file_name} : DatabaseError occurred at line {error_line}: {error_message}")
            raise e
        
        except Exception as e:
            error_message = traceback.format_exc()
            error_line = str(e.__traceback__.tb_lineno) 
            logger.error(f"{csv_file_name} : Error occurred at line {error_line}: {error_message}")
            raise e
        
        finally:
            # リソースのクリーンアップ
            # connectionをクローズする
            if conn:
                hive_connect_singleton.close_connection()
            # 処理対象ファイルクローズする
            csv_file.close()

