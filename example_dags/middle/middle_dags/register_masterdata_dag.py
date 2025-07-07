import airflow, os
from airflow import DAG
from datetime import timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from middle.common.constants_colums import RunMode
from middle.common.kubernetes_config import get_k8s_config
from middle.common.utils import get_sysuser
from middle.report_register.register_masterdata_info import insert_masterdata

# 実行モードを設定する
run_mode = Variable.get("MIDDLE_RUN_MODE")
os.environ["MIDDLE_RUN_MODE"] = run_mode

if run_mode == RunMode.DEV.value:
    os.environ["LOG_LEVEL"] = "DEBUG"
elif run_mode == RunMode.PROD.value:
    os.environ["LOG_LEVEL"] = "INFO"
else:
    os.environ["LOG_LEVEL"] = "DEBUG"

owner = get_sysuser()

# dag用引数定義
default_args = {
    'owner': 'middle',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email_on_failure': False,
    "email_on_retry": False,
    'retries': 0
}

# dagインスタンス作成 
dag = DAG('register_masterdata_dag', 
            default_args = default_args, 
            description = "マスタデータ登録",
            schedule_interval = None , # 午前0時と午前3時
            # dagrun_timeout = timedelta(minutes=60),
            tags=['middle', run_mode])

# マスタデータ登録タスクの定義
register_masterdata_task = PythonOperator(
    task_id='register_masterdata_task',
    python_callable = insert_masterdata,  # マスタ登録用の関数を指定
    dag = dag,
    executor_config = get_k8s_config(), # proxy設定やconfigMap設定
)

# タスク実行 
register_masterdata_task
