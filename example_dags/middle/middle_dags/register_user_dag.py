import airflow, os
from airflow import DAG
from datetime import timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from middle.common.constants_colums import RunMode
from middle.common.kubernetes_config import get_k8s_config
from middle.common.utils import get_sysuser
from middle.report_register.register_user import insert_user

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

# DAG用引数定義
default_args = {
    "owner": "corp",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(2),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

# DAGインスタンス作成
dag = DAG(
    "register_user_dag",
    default_args=default_args,
    description="ユーザ登録",
    schedule_interval=None,  # 手動実行
    tags=["middle", run_mode],
)

# 処理対象のシートを `constants.MasterTable` から動的に取得
# target_sheets = [
#     EEGSMasterSheetName.AMCMST_SHEET_NAME.value,
#     EEGSMasterSheetName.MJSIC_SHEET_NAME.value,
#     EEGSMasterSheetName.MECF_SHEET_NAME.value,
# ]
#　airflowから渡す運用にし、deploy作業減らすため
target_file_name = Variable.get("USER_APPLICATION_FORM")

# マスタデータ登録タスク
register_user_task = PythonOperator(
    task_id="register_user_task",
    python_callable=insert_user,
    op_kwargs={"target_file_name": target_file_name},
    dag=dag,
    executor_config=get_k8s_config(),
)

# タスク実行
register_user_task
