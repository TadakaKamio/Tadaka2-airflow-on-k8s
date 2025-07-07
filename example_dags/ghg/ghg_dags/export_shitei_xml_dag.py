import airflow
import ghg.scripts.export_shitei_xml_script as script
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
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
    "export_shitei_xml",  # DAGのID
    default_args=default_args,
    description="指定表のXML出力",
    schedule_interval="@once",
    tags=["ghg", run_mode],
)

# タスクの設定
task_export_shitei_xml = PythonOperator(
    task_id="task_export_shitei_xml",  # タスクID
    python_callable=script.export_shitei_xml,  # 呼び出すPython関数
    dag=dag,
    executor_config=get_k8s_config(),
)

# タスクの実行順序の設定
task_export_shitei_xml
