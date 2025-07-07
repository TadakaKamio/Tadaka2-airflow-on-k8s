import airflow
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator

import ghg.scripts.delete_hadoop_file_script as script
from ghg.common.kubernetes_config import get_k8s_config
from ghg.common.log import MyAppLog
from ghg.common.utils import set_log_level

# AirflowのVariableから実行モードを取得
run_mode = Variable.get("GHG_RUN_MODE")

# ログレベルを設定する
set_log_level(run_mode)

# MyAppLogクラスのインスタンス化
logger = MyAppLog()

# デフォルトパラメータの設定
default_args = {
    "owner": "ghg",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(2),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
}

# DAGの設定
dag = DAG(
    "delete_hadoop_file",  # DAGのID
    default_args=default_args,
    description="Hadoopファイル削除",
    schedule_interval="@once",
    tags=["ghg", run_mode],
)

# タスクの設定
task_delete_hadoop_file = PythonOperator(
    task_id="task_delete_hadoop_file",  # タスクID
    python_callable=script.delete_hadoop_file,  # 呼び出すPython関数
    dag=dag,
    executor_config=get_k8s_config(),
)

# タスクの実行順序の設定
task_delete_hadoop_file
