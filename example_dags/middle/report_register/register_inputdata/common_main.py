import os
import time
import middle.common.constants_colums as constants
import middle.common.log as log
from middle.common.postgre_connect import Psycopg2Singleton
from middle.common.utils import get_process_time
from middle.report_register.register_inputdata.save_inputdata_info import save_input_data
import middle.common.utils as utils

# log出力用instance
logger = log.MiddleAppLog()

# 実行モード
run_mode = constants.RunMode.DEV.value
#グローバル変数マスタデータ
master_data = None

@log.log_writer(logger)
def main(**kwargs):
    input_file_name = None #入力シートファイル
    input_file_content = None
    global master_data 

    # 計算式処理用ライブラリsympyをインストール
    utils.install_package('sympy')
    
    # 受入conf取得
    dag_run_conf = kwargs.get('dag_run').conf or {}
    if dag_run_conf is not None:
        input_file_name = dag_run_conf.get('input_file_name')
        input_file_content = dag_run_conf.get('input_file_content')
        user_id = dag_run_conf.get('user_id')
        print(user_id)
        global master_data 
        master_data = dag_run_conf.get('mst_data')

        logger.info(f"★★{input_file_name}★★")

    run_mode = constants.RunMode.DEV.value \
        if os.environ.get("MIDDLE_RUN_MODE") is None else os.environ.get("MIDDLE_RUN_MODE")
    
    postgre_connect_singleton = postgre_conn = None  # postgre接続インスタンス
    
    if run_mode in ( constants.RunMode.PROD.value, constants.RunMode.S2_PROD.value):
        start_time = time.time()
        # postgre connect接続
        postgre_connect_singleton = Psycopg2Singleton()
        # コネクション取得
        postgre_conn = postgre_connect_singleton._connection
        
        end_time= time.time()
        get_process_time(start_time, end_time, "postgre接続取得")

    try:
        # TDH登録処理実行
        save_input_data(postgre_conn, input_file_name, input_file_content, user_id)

    except Exception as e:
        msg = "データ登録処理が失敗しました、"
        logger.error(f"{msg}:{e.args[0]}")
        raise e 
    finally:
        # リソースなどのクリーンアップ
        postgre_connect_singleton.close_connection()

if __name__ == "__main__":
    main()