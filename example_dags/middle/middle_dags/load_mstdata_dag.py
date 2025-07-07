import airflow, os
from airflow import DAG
from datetime import timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from middle.common.constants_colums import RunMode
from middle.common.kubernetes_config import( 
    get_k8s_config, get_proself_k8s_config
)
import middle.common.utils as utils
import middle.common.utils as utils
import middle.common.log as log
from middle.report_register.register_masterdata_info import register_mst_data_from_csv
from middle.report_register.common.download_proselffile_to_hadoop import get_file_list
from middle.report_register.common.download_proselffile_to_hadoop import download_files

# 実行モードを設定する
run_mode = Variable.get("MIDDLE_RUN_MODE")
os.environ["MIDDLE_RUN_MODE"] = run_mode

if run_mode == RunMode.DEV.value:
    os.environ["LOG_LEVEL"] = "DEBUG"
elif run_mode == RunMode.PROD.value:
    os.environ["LOG_LEVEL"] = "INFO"

# log用instance
logger = log.MiddleAppLog()

owner = utils.get_sysuser()

# dag用引数定義
default_args = {
    'owner': 'middle',
    "depends_on_past": False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email_on_failure': False,
    "email_on_retry": False,
    "retries": 0
}

# dagインスタンス作成 
dag = DAG('load_mstdata_dag', 
            default_args = default_args, 
            description = "CSVマスタデータHiveロード",
            schedule_interval = None , # 午前0時と午前3時
            # dagrun_timeout = timedelta(minutes=60),
            tags=['middle', run_mode])

get_file_list_task = PythonOperator(
    task_id = 'get_file_list',
    python_callable = get_file_list,
    provide_context = True,
    dag = dag,
    executor_config = get_proself_k8s_config()
)

download_files_task = PythonOperator(
    task_id = 'download_files',
    python_callable = download_files,
    provide_context = True,
    dag = dag,
    executor_config = get_proself_k8s_config()
)

# マスタデータ登録タスクの定義
load_mstdata_task = PythonOperator(
    task_id='load_mstdata',
    python_callable = register_mst_data_from_csv,  # TDHへデータ登録用メイン関数を指定
    dag = dag,
    executor_config = get_k8s_config(), # proxy設定やconfigMap設定
)

get_file_list_task >> download_files_task >> load_mstdata_task


