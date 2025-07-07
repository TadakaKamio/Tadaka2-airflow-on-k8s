"""
middle_download.py

このスクリプトはProselfからData Fabricへファイルをダウンロードします。

機能:
- ProselfからData Fabricへファイルをダウンロードします。
- 取得元のPathはVariableの「middle_download_get_path」です。
- 保存先のPathはVariableの「middle_download_ignore_files_dir」です。
- 保存先にすでにあるファイルはダウンロードされません。

使用方法:
- GiteaにコードをPush後、AirflowからDAGを実行してください。
"""

import os

from datetime import timedelta
from kubernetes.client import models as k8s

import airflow

from airflow.decorators import dag, task
from airflow.models import Variable

import middle.common.log as log
from middle.middle_download.utils import *
from middle.middle_download.tests.task_test import task_test

# 実行モード取得
run_mode = Variable.get("middle_download_run_mode")
if run_mode == 'test':
    os.environ["LOG_LEVEL"] = 'DEBUG'

# loggerインスタンス
logger = log.MiddleAppLog()

args = {
    'owner': 'middle',
}

@dag(
    dag_id='middle_download',
    default_args=args,
    description = "proselfからDWHへファイル連携",
    start_date=airflow.utils.dates.days_ago(2),
    # schedule_interval=Variable.get("middle_download_schedule_interval"),
    schedule_interval=None,
    tags = ["middle"]
)
def middle_download():
    cpu_lim = Variable.get("middle_download_cpu_limit")
    cpu_req = cpu_lim
    ram_lim = Variable.get("middle_download_memory_limit")
    ram_req = ram_lim

    pod_config = {
        "pod_override":
        k8s.V1Pod(spec=k8s.V1PodSpec(containers=[
            k8s.V1Container(name="I-am-rich",
                            resources=k8s.V1ResourceRequirements(
                                limits={
                                    "cpu": cpu_lim,
                                    "memory": ram_lim
                                },
                                requests={
                                    "cpu": cpu_req,
                                    "memory": ram_req
                                }))
        ]))
    }

    @task(executor_config=pod_config)
    def get_file_list(**kwargs):

        @task_test('get_file_list')  # Test for Dag Task
        def _do():
            try:
                run_mode = Variable.get("middle_download_run_mode")
                get_path = Variable.get("middle_download_get_path")
                put_base_path = Variable.get(
                    "middle_download_put_base_path")
                put_dir_path = Variable.get("middle_download_put_inputfiles_path")
                proself_base_url = Variable.get(
                    "middle_download_proself_base_url")
                ignore_files_dir = Variable.get(
                    "middle_download_ignore_files_dir")
                proself_auth = Variable.get(
                    "middle_download_proself_auth",
                    deserialize_json=True)

                # # ダウンロード済みファイルを格納しているvolume内の一覧を取得
                ls_path = pathjoin(put_base_path, ignore_files_dir)

                logger.debug(f'ダウンロード済みファイルパス : {ls_path}')

                exist_files = ls_volume(ls_path)

                logger.debug(f'ダウンロード済みファイル : {exist_files}')
                # 取得対象フォルダ内の一覧を取得
                file_list = recursive_get_list(proself_base_url, get_path,
                                               proself_auth)

                # file_list(Full Path)のファイル名とexist_files(ファイル名のみ)を比較してfile_listのみにあるfull pathを取得する
                download_list = [
                    file for file in file_list
                    if file.split('/')[-1] not in exist_files
                ]

                filtered_list = []
                for file_path in download_list:
                    if not filter_target_file(file_path.split('/')[-1]):
                        filtered_list.append(file_path)

                        bank_nm = file_path.split('/')[2]
                        company_nm = file_path.split('/')[3]
                        
                        to_make_dir = pathjoin(put_base_path, put_dir_path, bank_nm, company_nm)
                        # maprfs上で「銀行/企業/」のフォルダを作成する
                        make_folder(to_make_dir)

            except Exception as e:
                logger.error(f'error in get list area. error message : {e}')
                raise e

            if not hasattr(filtered_list, "__iter__"):
                raise ValueError(
                    f'download_list is not iterable. items is : {filtered_list}'
                )

            return filtered_list

        return _do()

    @task(executor_config=pod_config)
    def download_files(**kwargs):

        @task_test('download_files')  # Test for Dag Task
        def _do():
            get_path = Variable.get("middle_download_get_path")
            put_dir_path = Variable.get("middle_download_put_inputfiles_path")
            put_base_path = Variable.get(
                "middle_download_put_base_path")
            proself_base_url = Variable.get(
                "middle_download_proself_base_url")
            proself_auth = Variable.get(
                "middle_download_proself_auth",
                deserialize_json=True)

            ti = kwargs['ti']
            download_list = ti.xcom_pull(task_ids='get_file_list')

            # for文でのエラーをエスケープする
            if not hasattr(download_list, "__iter__"):
                raise ValueError(
                    f'download_list is not iterable. items is : {download_list}'
                )

            error_messages = []
            for files in download_list:
                try:
                    # ファイルをダウンロード
                    url = make_proself_url(proself_base_url, files)
                    parts = files.split('/')
                    # /05311_ESG-POC/山梨中銀/東電介護老人ホーム/行員向け入力シート_企業カルテ_山梨中銀_2022_1.xlsm
                    bank_nm = parts[2]
                    company_nm = parts[3]

                    local_path = basename(files)
                    logger.info('download from proself. url is ' + str(url))
                    local_path = get_file(url, local_path, proself_auth)

                    put_path = pathjoin(put_base_path, put_dir_path, bank_nm, company_nm, local_path)
                    logger.info(f"downloadパス★{put_path}")

                    put_out = put_file(local_path, put_path)
                    if put_out.returncode != 0:
                        msg = f'put_file is failed. file name is {local_path}. put path is {put_path}. stdout is {put_out}'
                        logger.error(msg)
                        raise Exception(msg)

                except Exception as e:
                    err_file_msg = f'error download files : {files}.'
                    logger.error(err_file_msg)
                    err_msg = f'error message : {e}.'
                    logger.error(err_msg)
                    error_messages.append({
                        'error_file': err_file_msg,
                        'error_message': err_msg
                    })

                try:
                    remove_local_file(local_path)
                except Exception as e:
                    msg = f'remove local file is failed. local_path is : {local_path}'
                    logger.error(msg)
                    raise e

            if error_messages:
                raise Exception(str(error_messages))

            return True

        return _do()

    get_file_list() >> download_files()


middle_download()
