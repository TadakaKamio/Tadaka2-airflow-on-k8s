import airflow, os
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from middle.common.constants_colums import RunMode
from middle.common.kubernetes_config import( 
    get_k8s_config
)
import middle.common.utils as utils
import middle.common.utils as utils
import middle.common.log as log
from middle.report_register.register_inputdata.common_main import main

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
dag = DAG('save_inputdata_dag', 
            default_args = default_args, 
            description = "step2入力データ登録",
            schedule_interval = None , # 午前0時と午前3時
            # dagrun_timeout = timedelta(minutes=60),
            tags=['corp', run_mode])

# マスタデータ登録タスクの定義
save_inputdata_task = PythonOperator(
    task_id='save_inputdata',
    python_callable = main,  # TDHへデータ登録用メイン関数を指定
    provide_context = True,
    dag = dag,
    executor_config = get_k8s_config(), # proxy設定やconfigMap設定
)

save_inputdata_task


