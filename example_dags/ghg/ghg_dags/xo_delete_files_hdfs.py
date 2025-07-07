import os
import re
import sys
from datetime import datetime

import airflow
import pyarrow.fs as fs
from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from kubernetes.client import models as k8s

from ghg.common.log import MyAppLog

logger = MyAppLog()

# DAGのスペック設定
cpu_req = cpu_lim = Variable.get("XO_cpu_limit")  # 500m
ram_req = ram_lim = Variable.get("XO_memory_limit")  # 3G

pod_config = {
    "pod_override": k8s.V1Pod(
        spec=k8s.V1PodSpec(
            containers=[
                k8s.V1Container(
                    name="I-am-rich",
                    resources=k8s.V1ResourceRequirements(
                        limits={"cpu": cpu_lim, "memory": ram_lim},
                        requests={"cpu": cpu_req, "memory": ram_req},
                    ),
                )
            ]
        )
    )
}


# HDFS上のファイル一覧を取得
def get_hdfs_file_list(dtapfs, src_path):
    try:
        logger.info(f"Trying to get file list from HDFS path: {src_path}")
        files = dtapfs.get_file_info(fs.FileSelector(src_path, recursive=True))
        file_list = []
        for file in files:
            file_list.append(file.base_name)
        return file_list
    except Exception as e:
        logger.error(f"Error: failed to get hdfs file list: {e}")
        return False


# ファイル名から日付を取得、日付でソート
def extract_date_from_filename(file_list):
    # ファイル名のYYYYMMDDから日付を抽出
    file_date_list = []
    pattern = r"(\d{8})"
    for file in file_list:
        match = re.search(pattern, file)
        if match:
            try:
                date = datetime.strptime(match.group(0), "%Y%m%d")
                file_date_list.append((file, date))
            except ValueError:
                logger.warn(f"Failed to parse date from {file}")
        else:
            logger.warn(f"No date pattern found in {file}")
    # 日付でソート
    file_date_list.sort(key=lambda x: x[1])

    return file_date_list


# HDFS上のファイルを削除する
def delete_files(dtapfs, src_path, files_to_delete):
    for file in files_to_delete:
        try:
            dtapfs.delete_file(os.path.join(src_path, file))
            logger.info(f"Deleted file: {file}")
        except Exception as e:
            logger.error(f"Failed to delete file: {file}, reason: {e}")
            raise sys.exit(1)


# main tasks ###################################################################
def delete_files_from_hdfs():
    # Airflow Variables
    dtap_path = Variable.get("XO_dtap_path")
    src_path = Variable.get("XO_hdfs_dir")
    num_dates_to_keep = int(Variable.get("XO_num_dates_to_keep"))

    # HDFSへの接続
    try:
        dtapfs = fs.HadoopFileSystem.from_uri(dtap_path)
        logger.info("Success: success to connect hdfs")
    except Exception as e:
        logger.error(f"Error: falied to connect hdfs. Reason: {e}")
        raise e

    # HDFS上のファイルリストを取得
    file_list = get_hdfs_file_list(dtapfs, src_path)

    if not file_list:
        logger.info("info: file_list is empty or None")
        return

    # ファイルの日付を取得、ソート
    files_with_dates = extract_date_from_filename(file_list)

    # 日付のリストを作成し、ユニークな日付を抽出
    unique_dates = sorted(set(date for _, date in files_with_dates))

    # 最新の14日分の日付を保持する
    dates_to_keep = unique_dates[-num_dates_to_keep:]

    # 削除対象のファイルを決定
    files_to_delete = [f for f, date in files_with_dates if date not in dates_to_keep]

    # ファイルを削除
    if not files_to_delete:
        logger.info("No files to be deleted")
        return

    logger.info("Start deleting files")
    delete_files(dtapfs, src_path, files_to_delete)
    logger.info(f"Files deleted: {files_to_delete}")


# DAG ################################
default_args = {
    "owner": "GHG",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(1),
}

schedule = Variable.get("XO_file_delete_schedule_interval")
dag = DAG(
    dag_id="XO_delete_hdfs_files",
    default_args=default_args,
    description="XO_delete_hdfs_files",
    schedule_interval=schedule if bool(schedule) else None,
    catchup=False,
)

# task #############################
delete_files_task = PythonOperator(
    task_id="delete_files_from_hdfs",
    python_callable=delete_files_from_hdfs,
    dag=dag,
    executor_config=pod_config,
    provide_context=True,
)

####################################

delete_files_task
