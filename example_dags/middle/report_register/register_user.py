from hashlib import pbkdf2_hmac
import bcrypt
import numpy as np
import pandas as pd
import os, traceback
from pyhive.exc import DatabaseError
from airflow.models import Variable
from middle.common.postgre_connect import Psycopg2Singleton
import middle.common.utils as utils
import middle.common.log as log
import middle.common.constants_colums as constants
from middle.common.hive_connect import ImpalaSingleton
from middle.common.hql_processor import execute_delete, execute_hive_update, execute_insert, execute_update

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
schema_middle = json_config["database_posgre"]["schema_middle"]

hive_corp_user = json_config["database_hive"]["user"]
hive_corp_password = json_config["database_hive"]["password"] 

# rootパス取得
project_root_path = utils.get_project_root_path()

@log.log_writer(logger)
def insert_user(target_file_name=None, *args, **kwargs):
    """ユーザ登録"""

    # 実行モード取得
    run_mode = os.getenv("MIDDLE_RUN_MODE", constants.RunMode.DEV.value) \
        if os.environ.get("MIDDLE_RUN_MODE") is None else os.environ.get("MIDDLE_RUN_MODE")

    # excelファイル処理用ライブラリopenpyxlをインストール
    utils.install_package("openpyxl")

    logger.info("★★★システム利用アカウント登録・変更処理を開始します★★★")
    # hive接続インスタンス
    hive_corp_connect_singleton = corp_conn = None
    postgre_connect_singleton = postgre_conn = None  # postgre接続インスタンス

    if run_mode in ( constants.RunMode.PROD.value, constants.RunMode.S2_PROD.value):
        # postgre connect接続
        # postgre_connect_singleton = Psycopg2Singleton()
        # コネクション取得
        # postgre_conn = postgre_connect_singleton._connection
        # Hive connect接続
        hive_corp_connect_singleton = ImpalaSingleton(hive_corp_user, hive_corp_password)
        # コネクション取得
        corp_conn = hive_corp_connect_singleton._connection

    # 処理する入力シートファイル一覧取得
    excel_files = None
    if run_mode == constants.RunMode.DEV.value:
        # excel_files = utils.get_files("masterfiles")
        excel_files = [r'C:\Users\msduser\cndx_workspace\esg05\dags\middle\files\masterfiles\account_application_form.xlsx']
    else:
        base_path = Variable.get("middle_download_put_base_path")
        sub_path = Variable.get("middle_download_put_masterfiles_path")

        # Hadoopから対象ファイルのBytesIOを取得
        excel_files = utils.get_file_from_hadoop(base_path, sub_path, None)

    file_names = [os.path.basename(path) for path in excel_files]
    # ファイル存在チェック
    if (excel_files is None or len(excel_files) == 0) or target_file_name not in file_names:
        logger.info("登録・更新するファイルがないため、処理を中止します。")
        return
    
    # ファイル数分処理を繰り返す読み込み
    # for excel_file in excel_files: # 🔥🔥🔥🔥テスト用
    for file_path, excel_file in excel_files.items():
        logger.info(f"{file_path}★処理中ファイル名： {excel_file} ★")

        with pd.ExcelFile(excel_file) as file:
            sheet_names = file.sheet_names

        try:
            if run_mode == constants.RunMode.DEV.value:
                # user_df.to_csv("user.csv", index=False)
                pass
            else:
                # シート数分を繰り返す
                for sheet_name in sheet_names:
                    # target_sheetsが指定されている場合、シート名が対象シートに含まれていないとスキップ
                    # if target_sheets and sheet_name not in target_sheets:
                    #     logger.info(f"シート {sheet_name} は指定されていないため、スキップします。")
                    #     continue

                    if constants.EEGSMasterSheetName.MUMST_SHEET_NAME.value == sheet_name:
                        user_df =  get_user_data(excel_file, sheet_name)
                        # 申請区分ごとにデータフレームを分割
                        df_add = user_df[user_df["APPLY_KBN"] == constants.UserApplicationKbn.ADD.value].drop(columns=["APPLY_KBN"])
                        df_update = user_df[user_df["APPLY_KBN"] == constants.UserApplicationKbn.UPDATE.value].drop(columns=["APPLY_KBN"])
                        df_delete = user_df[user_df["APPLY_KBN"] == constants.UserApplicationKbn.DELETE.value].drop(columns=["APPLY_KBN"])
                        df_add.to_csv("df_add.csv", index=False)
                        df_update.to_csv("df_update.csv", index=False)
                        df_delete.to_csv("df_delete.csv", index=False)
                                            
                        # postgre connect接続
                        postgre_connect_singleton = Psycopg2Singleton()
                        # コネクション取得
                        postgre_conn = postgre_connect_singleton._connection
                        if not df_add.empty:
                            # PostgreS登録
                            execute_insert(
                                postgre_conn,
                                df_add,
                                constants.MUMST_COLUMNS,
                                schema_middle + DOT + constants.MasterTable.MUMST.value,
                            )
                            # Hive登録
                            # execute_insert(
                            #     corp_conn,
                            #     user_df,
                            #     constants.MUMST_COLUMNS,
                            #     schema_middle + DOT + constants.MasterTable.MUMST.value,
                            # )
                        if not df_update.empty:
                            # PostgreS登録
                            # update_data = [{col: df_update[col]} for col in df_update.columns]
                            update_data = df_update.to_dict(orient="records")
                            execute_update(
                                postgre_conn,
                                schema_middle + DOT + constants.MasterTable.MUMST.value,
                                update_data,
                                {"USER_MAIL": df_update["USER_MAIL"].iloc[0]}
                            )
                            # Hive登録
                            # execute_hive_update(corp_conn, 
                            #                     schema_middle + DOT + constants.MasterTable.MUMST.value,
                            #                     constants.MUMST_COLUMNS,
                            #                     True,False)
                        if not df_delete.empty:
                            update_data = df_update.to_dict(orient="records")
                            execute_update(
                                postgre_conn,
                                schema_middle + DOT + constants.MasterTable.MUMST.value,
                                [{"DELETE_FLG": True}],
                                {"USER_MAIL": df_update["USER_MAIL"].iloc[0]}
                            )

        except DatabaseError as e:
            error_message = traceback.format_exc()
            error_line = str(e.__traceback__.tb_lineno) 
            logger.error(f" DatabaseError occurred at line {error_line}: {error_message}")
            raise e
        
        except Exception as e:
            error_message = traceback.format_exc()
            error_line = str(e.__traceback__.tb_lineno) 
            logger.error(f" Error occurred at line {error_line}: {error_message}")
            raise e

        finally:
            # リソースのクリーンアップ
            # connectionをクローズする
            if hive_corp_connect_singleton:
                hive_corp_connect_singleton.close_connection()
            if postgre_connect_singleton:
                postgre_connect_singleton.close_connection()

def set_system_column(result_df):
    """
    システムカラム情報設定
    """
     # excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)
    result_df["START_DATE"] = '20240401'
    result_df["END_DATE"] = None
    result_df["CREATION_DATETIME"] = f"{current_timestamp}"
    result_df["CREATE_BY"] = f"{creator_name}"
    result_df["UPDATE_DATETIME"] = None
    result_df["UPDATE_BY"] = None
    result_df["DELETE_FLG"] = None

def get_user_data(excel_file, sheet_name):
    """
    活動項目小分類（事業者）マスタデータ取得
    """

    # Excelファイルを読み込む
    df = pd.read_excel(
        excel_file,
        sheet_name= sheet_name,
        skiprows=6,
        usecols="C:K"
    )
    # df = df.drop(df.columns[[0,1]], axis=1)
    # nanを空文字に変換
    df.fillna(np.nan, inplace=True)
    # '-'を空文字に変換
    df.replace(HYPHEN, BLANK, inplace=True)

    # カラム名を設定
    df.columns = [
        "申請区分",
        "会社名",
        "部署",
        "氏名",
        "アドレス",
        "パスワード",
        "権限",
        "適用開始日",
        "備考欄"
    ]
    
    # CSVに出力
    df.to_csv("df.csv", index=False)
    # 余計なスペースを削除
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # appl_kbn = df["申請区分"]
    # if constants.UserApplicationKbn.ADD.value == appl_kbn: 
    # カラム名を英字に変換
    result_df = df.rename(columns={
        "申請区分": "APPLY_KBN",
        "会社名": "COMPANY_NAME",
        "部署": "DEPARTMENT_NAME",
        "氏名": "USER_NAME",
        "アドレス": "USER_MAIL",
        "パスワード": "USER_PASSWORD",
        "権限": "USER_ROLE",
        "適用開始日": "START_DATE",
        "備考欄": "REMARKS"
    })
    # "削除フラグ" 列を削除
    result_df = result_df.drop(columns=[ "REMARKS"])
    result_df["DEPARTMENT_ID"]="12345678"
    
    # パスワードをハッシュ化
    # ソルトを生成
    salt = bcrypt.gensalt()

    # パスワードをハッシュ化
    result_df["USER_PASSWORD"] = result_df["USER_PASSWORD"].astype(str)
    result_df["USER_PASSWORD"] = result_df.apply(
        lambda row: bcrypt.hashpw(row["USER_PASSWORD"].encode("utf-8"), salt).decode('utf-8') ,
        axis = 1
    )
    
    # 出力順番を指定
    result_df = result_df[[
        "APPLY_KBN",
        "USER_MAIL",
        "USER_NAME",
        "COMPANY_NAME",
        "DEPARTMENT_ID",
        "DEPARTMENT_NAME",
        "USER_PASSWORD",
        "USER_ROLE"
    ]]
    result_df["USER_ROLE"]="admin"
    result_df = result_df.dropna(subset=["USER_MAIL"])
    # excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)
    set_system_column(result_df)

    # CSVに出力
    # result_df.to_csv("user.csv", index=False)

    return result_df


