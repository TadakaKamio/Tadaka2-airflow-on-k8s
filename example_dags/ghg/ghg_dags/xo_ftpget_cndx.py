import csv
import ftplib
import os
import sys
import time
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


def _load_json_to_list(_json_file):
    import json

    try:
        target_list = json.loads(_json_file)
    except Exception as e:
        logger.error(f"error in target list area. error message : {e}")
        raise e

    return target_list


# FTPからローカルへダウンロード
def download_files(
    ftp_host,
    ftp_port,
    ftp_user,
    ftp_passwd,
    ftp_file_list,
    current_date,
    max_retries,
    wait_seconds,
):

    try:
        with ftplib.FTP() as ftp:
            # 接続
            print(f"試しているConnect to {ftp_host}:{ftp_port}")
            ftp.connect(ftp_host, ftp_port, timeout=10)

            # ログイン
            ftp.login(ftp_user, ftp_passwd)
            print("Login successful")

            # FTP サーバーのレスポンスを表示
            print("Server response:", ftp.getwelcome())
            ftp.set_pasv(True)

            upload_file_list = []
            error_messages = []

            for uri in ftp_file_list:
                retry_times = max_retries
                last_exception = None
                while retry_times > 0:
                    try:
                        file = os.path.basename(uri)

                        base_name, _ = os.path.splitext(file)
                        new_file_name = f"{base_name}_{current_date}.csv"

                        with open(new_file_name, "wb") as f:
                            ftp.retrbinary("RETR " + uri, f.write)
                        logger.info(
                            f"Success: success to download {file}/{new_file_name} from ftp server {os.path.dirname(uri)}."
                        )

                        upload_file_list.append(new_file_name)
                        break

                    except Exception as e:
                        retry_times -= 1
                        last_exception = e
                        if retry_times > 0:
                            time.sleep(wait_seconds)

                if retry_times == 0:
                    err_file_msg = f"error download files : {file}."
                    logger.error(err_file_msg)
                    err_msg = f"error message : {last_exception}."
                    logger.error(err_msg)
                    error_messages.append(
                        {"error_file": err_file_msg, "error_message": err_msg}
                    )

            if error_messages:
                raise Exception(str(error_messages))

        return upload_file_list

    except Exception as e:
        error_message = (
            f"Error: unable to connect to FTP Server {ftp_host}:{ftp_port}. Reason: {e}"
        )
        logger.error(error_message)
        raise Exception(error_message)


# HDFSにアップロード
def upload_files(dtapfs, upload_dir, upload_files, max_retries, wait_seconds):
    import shutil

    uploaded_file_list = []

    if upload_files:
        for file_name in upload_files:
            retry_times = max_retries
            file_path = "/".join([upload_dir, file_name])
            while retry_times > 0:
                try:
                    with open(file_name, "rb") as local_file_in:
                        with dtapfs.open_output_stream(file_path) as remote_out_file:
                            shutil.copyfileobj(local_file_in, remote_out_file)
                    logger.info(
                        f"Success: Successfully uploaded {file_name} to {file_path}."
                    )

                    uploaded_file_list.append(file_name)

                    break

                except Exception as e:
                    retry_times -= 1
                    logger.error(
                        f"Error: put_file is failed. file name is {file_name}. put path is {file_path}. Fail count is {max_retries - retry_times}. stderr is {e}"
                    )
                    if retry_times > 0:
                        time.sleep(wait_seconds)

            # リトライ回数が0になった場合Exceptionを発生
            if retry_times == 0:
                error_message = f"Error: put_file is failed. file name is {file_name}. put path is {file_path}. stderr is {e}"
                raise Exception(error_message)

    else:
        logger.info(f"There is no file to upload to hdfs.")

    return uploaded_file_list


# main tasks ###################################################################
def download_files_from_ftp():
    # Airflow Variables
    ftp_host = Variable.get("XO_ftp_host")
    ftp_port = int(Variable.get("XO_ftp_port"))
    ftp_file_list_str = Variable.get("XO_ftp_file_list")
    ftp_user = Variable.get("XO_ftp_user")
    ftp_pass = Variable.get("XO_ftp_password")
    dtap_path = Variable.get("XO_dtap_path")
    upload_dir = Variable.get("XO_hdfs_dir")
    max_retries = int(Variable.get("XO_max_retries"))
    wait_seconds = int(Variable.get("XO_wait_seconds"))

    os.environ["TZ"] = "Asia/Tokyo"
    time.tzset()
    process_date = datetime.now().strftime("%Y%m%d")

    ftp_file_list = _load_json_to_list(ftp_file_list_str)

    try:
        dtapfs = fs.HadoopFileSystem.from_uri(dtap_path)
        logger.info("Success: success to connect hdfs")
    except Exception as e:
        logger.error(f"Error: falied to connect hdfs. Reason: {e}")
        raise e

    try:
        logger.info(f"Start download files from ftp.")
        download_file_list = download_files(
            ftp_host,
            ftp_port,
            ftp_user,
            ftp_pass,
            ftp_file_list,
            process_date,
            max_retries,
            wait_seconds,
        )
        logger.info(f"End download files from ftp.")
    except Exception as e:
        logger.error(f"Error: falied to download files from ftp. Reason: {e}")
        raise e

    try:
        logger.info(f"Start upload files to hdfs.")
        upload_files(dtapfs, upload_dir, download_file_list, max_retries, wait_seconds)
        logger.info(f"End upload files to hdfs.")
        return
    except Exception as e:
        logger.error(f"Error: falied to upload files to hdfs. Reason: {e}")
        raise e


# DAG ################################
default_args = {
    "owner": "GHG",
    "depends_on_past": False,
    "start_date": airflow.utils.dates.days_ago(1),
}

schedule = Variable.get("XO_ftp_get_schedule_interval")
dag = DAG(
    dag_id="XO_ftp_get_cndx",
    default_args=default_args,
    description="XO_FTP_GET",
    schedule_interval=schedule if bool(schedule) else None,
    catchup=False,
)

# task #############################
download_task = PythonOperator(
    task_id="download_files_from_ftp",
    python_callable=download_files_from_ftp,
    dag=dag,
    executor_config=pod_config,
    provide_context=True,
)
####################################

download_task
