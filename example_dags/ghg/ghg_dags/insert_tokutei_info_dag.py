import airflow
import ghg.scripts.insert_tokutei_info_script as script
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
    "owner": "ghg",  # DAGのオーナー
    "depends_on_past": False,  # 過去のタスク実行結果に依存しない
    "start_date": airflow.utils.dates.days_ago(2),  # DAGの開始日
    "email_on_failure": False,  # 失敗時にメール通知しない
    "email_on_retry": False,  # リトライ時にメール通知しない
    "retries": 0,  # リトライ回数
}

# DAGの設定
dag = DAG(
    "insert_tokutei_info",  # DAGのID
    default_args=default_args,  # 上記で設定したデフォルトパラメータ
    description="特定表のデータ登録",  # DAGの説明
    schedule_interval="@once",  # 実行スケジュール
    tags=["ghg", run_mode],  # DAGの分類
)

# タスクの設定
task_insert_tokutei_info = PythonOperator(
    task_id="task_insert_tokutei_info",  # タスクのID
    # python_callable=script.insert_tokutei_info,  # 実行するPython関数
    python_callable=script.insert_tokutei_info,  # 実行するPython関数
    dag=dag,  # 所属するDAG
    executor_config=get_k8s_config(),  # タスク実行のためのKubernetes設定を取得
)

# タスクの実行順序の設定
task_insert_tokutei_info
