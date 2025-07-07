import airflow, os
from airflow import DAG
from datetime import timedelta
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from middle.common.constants_colums import RunMode
from middle.common.kubernetes_config import get_k8s_config
from middle.common.utils import (
    get_sysuser,
    delete_mapr_file,
    pathjoin
)

# 実行モードを設定する
run_mode = Variable.get("MIDDLE_RUN_MODE")
os.environ["MIDDLE_RUN_MODE"] = run_mode

if run_mode == RunMode.DEV.value:
    os.environ["LOG_LEVEL"] = "DEBUG"
elif run_mode == RunMode.PROD.value:
    os.environ["LOG_LEVEL"] = "INFO"

owner = get_sysuser()
if owner is None: owner = "esg"

# Hadoop対象フォルダを指定
hadoop_base_path = Variable.get("middle_download_put_base_path")
hadoop_sub_path = Variable.get("middle_download_put_inputfiles_path")
file_paths = Variable.get("middle_delete_mapr_file_path", deserialize_json=True)

# ファイルパースがリストを判断する
if not isinstance(file_paths, list):
    file_paths = [file_paths]

full_path_list = []
for file_path in file_paths:
    full_path_list.append(pathjoin(hadoop_base_path,hadoop_sub_path,file_path))

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
dag = DAG('delete_mapr_file_dag', 
            default_args = default_args, 
            description = "maprFS不要フォルダ削除",
            schedule_interval = None,
            dagrun_timeout = timedelta(minutes=60),
            tags=['middle', run_mode])

# マスタデータ登録タスクの定義
delete_mapr_file_task = PythonOperator(
    task_id='delete_mapr_file_task',
    python_callable = delete_mapr_file,  # マスタ登録用の関数を指定
    op_args=[full_path_list],  # 関数に渡す引数
    dag = dag,
    executor_config = get_k8s_config(), # proxy設定やconfigMap設定
)

# タスク実行 
delete_mapr_file_task
