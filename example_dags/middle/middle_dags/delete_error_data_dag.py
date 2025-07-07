import airflow, os
from airflow import DAG
from datetime import timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from middle.common.constants_colums import RunMode
from middle.common.kubernetes_config import get_k8s_config
from middle.common.utils import get_sysuser
from middle.report_register.delete_error_data import delete_file

# 実行モードを設定する
run_mode = Variable.get("MIDDLE_RUN_MODE")
os.environ["MIDDLE_RUN_MODE"] = run_mode

if run_mode == RunMode.DEV.value:
    os.environ["LOG_LEVEL"] = "DEBUG"
elif run_mode == RunMode.PROD.value:
    os.environ["LOG_LEVEL"] = "INFO"

owner = get_sysuser()
if owner is None: owner = "middle"

# dag用引数定義
default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email_on_failure': False,
    "email_on_retry": False,
    'retries': 0
}

# dagインスタンス作成 
dag = DAG('delete_errordata_dag', 
            default_args = default_args, 
            description = "エラーデータ削除",
            schedule_interval = "@once", # "0 0,3 * * *" , # 午前0時と午前3時
            dagrun_timeout = timedelta(minutes=60),
            tags=['middle', run_mode])

# マスタデータ登録タスクの定義
delete_errordata_task = PythonOperator(
    task_id='delete_errordata_task',
    python_callable = delete_file,  # マスタ登録用の関数を指定
    dag = dag,
    executor_config = get_k8s_config(), # proxy設定やconfigMap設定
)

# タスク実行 
delete_errordata_task
