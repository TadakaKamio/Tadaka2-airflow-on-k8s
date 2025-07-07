"""
dags.py

このスクリプトはProselfからData Fabricへファイルをダウンロードします。

機能:
- ProselfからData Fabricへファイルをダウンロードします。
- 取得元のPathはVariableの「GHG_PROSELF_DOWNLOAD_GET_PATH」です。
- 保存先のPathはVariableの「GHG_PROSELF_DOWNLOAD_IGNORE_FILES_DIR」です。
- 保存先にすでにあるファイルはダウンロードされません。

使用方法:
- GiteaにコードをPush後、AirflowからDAGを実行してください。
"""

import airflow
import ghg.proself_download.utils as Proself_download_utils
from airflow.decorators import dag, task
from airflow.models import Variable
from ghg.common.log import MyAppLog
from ghg.common.utils import set_log_level
from kubernetes.client import models as k8s

# AirflowのVariableから実行モードを取得
run_mode = Variable.get("GHG_RUN_MODE")

# ログレベルを設定する
set_log_level(run_mode)

# MyAppLogクラスのインスタンス化
logger = MyAppLog()

args = {
    "owner": "ghg",
}


@dag(
    dag_id="ghg_proself_download",
    default_args=args,
    start_date=airflow.utils.dates.days_ago(2),
    schedule_interval=Variable.get("GHG_SCHEDULE_INTERVAL"),
)
def ghg_proself_download_tool():
    cpu_lim = Variable.get("GHG_PROSELF_DOWNLOAD_CPU_LIMIT")
    cpu_req = cpu_lim
    ram_lim = Variable.get("GHG_PROSELF_DOWNLOAD_MEMORY_LIMIT")
    ram_req = ram_lim

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

    @task(executor_config=pod_config)
    def get_file_list(**kwargs):
        def _do():
            try:
                proself_base_url = Variable.get("GHG_PROSELF_DOWNLOAD_PROSELF_BASE_URL")
                proself_sub_path = Variable.get("GHG_PROSELF_DOWNLOAD_PROSELF_SUB_PATH")
                put_base_path = Variable.get("GHG_PROSELF_DOWNLOAD_PUT_BASE_PATH")
                ignore_files_dir = Variable.get("GHG_PROSELF_DOWNLOAD_IGNORE_FILES_DIR")
                proself_auth = Variable.get(
                    "GHG_PROSELF_DOWNLOAD_PROSELF_AUTH", deserialize_json=True
                )

                # ダウンロード済みファイルを格納しているvolume内の一覧を取得
                ls_path = Proself_download_utils.pathjoin(
                    put_base_path, ignore_files_dir
                )
                logger.info(f"ダウンロード済みファイルパス : {ls_path}")
                exist_files = Proself_download_utils.ls_volume(ls_path)
                logger.info(f"ダウンロード済みファイル : {exist_files}")

                # Proselfの取得対象フォルダ内のファイル一覧を取得
                file_list = Proself_download_utils.recursive_get_list(
                    proself_base_url, proself_sub_path, proself_auth
                )
                logger.info(f"Proselfの取得対象フォルダ内のファイル一覧 : {file_list}")

                # file_list(Full Path)のファイル名とexist_files(ファイル名のみ)を比較して
                # file_listのみにあるfull pathを取得する
                download_list = [
                    file for file in file_list if file.split("/")[-1] not in exist_files
                ]

                # 対象外ファイルを除く
                filtered_list = []
                for file_path in download_list:
                    if not Proself_download_utils.filter_target_file(
                        file_path.split("/")[-1]
                    ):
                        filtered_list.append(file_path)
            except Exception as e:
                logger.error(
                    f"「get_file_list」関数を実行時、エラーが発生しました。エラーメッセージ : {e}"
                )
                raise e

            # for文でのエラーをエスケープする
            if not hasattr(filtered_list, "__iter__"):
                raise ValueError(
                    f"download_list is not iterable. items is : {filtered_list}"
                )

            logger.info(f"フィルター後のファイル一覧 : {filtered_list}")
            return filtered_list

        return _do()

    @task(executor_config=pod_config)
    def download_files(**kwargs):
        def _do():
            put_base_path = Variable.get("GHG_PROSELF_DOWNLOAD_PUT_BASE_PATH")
            put_sub_path = Variable.get("GHG_PROSELF_DOWNLOAD_PUT_SUB_PATH")
            proself_base_url = Variable.get("GHG_PROSELF_DOWNLOAD_PROSELF_BASE_URL")
            proself_auth = Variable.get(
                "GHG_PROSELF_DOWNLOAD_PROSELF_AUTH", deserialize_json=True
            )

            ti = kwargs["ti"]
            download_list = ti.xcom_pull(task_ids="get_file_list")

            if not download_list:
                logger.warn("ダウンロードリストが空です。何もダウンロードしません。")
                return

            # for文でのエラーをエスケープする
            if not hasattr(download_list, "__iter__"):
                raise ValueError(
                    f"download_list is not iterable. items is : {download_list}"
                )

            error_messages = []
            for files in download_list:
                try:
                    # ファイルをダウンロード
                    url = Proself_download_utils.make_proself_url(
                        proself_base_url, files
                    )
                    local_path = Proself_download_utils.basename(files)
                    logger.info("download from proself. url is " + str(url))
                    local_path = Proself_download_utils.get_file(
                        url, local_path, proself_auth
                    )
                    put_path = Proself_download_utils.pathjoin(
                        put_base_path, put_sub_path, local_path
                    )
                    put_out = Proself_download_utils.put_file(local_path, put_path)

                    if put_out.returncode != 0:
                        msg = (
                            f"put_file is failed. file name is {local_path}. "
                            f"put path is {put_path}. "
                            f"stdout is {put_out.stdout}, stderr is {put_out.stderr}"
                        )
                        logger.error(msg)
                        raise Exception(msg)

                except Exception as e:
                    err_file_msg = f"error download files : {files}."
                    logger.error(err_file_msg)
                    err_msg = f"error message : {e}."
                    logger.error(err_msg)
                    error_messages.append(
                        {"error_file": err_file_msg, "error_message": err_msg}
                    )

                else:
                    try:
                        Proself_download_utils.remove_local_file(local_path)
                    except Exception as e:
                        msg = (
                            f"remove local file is failed. local_path is : {local_path}"
                        )
                        logger.error(msg)
                        raise e

            if error_messages:
                raise Exception(str(error_messages))

            return True

        return _do()

    get_file_list() >> download_files()


ghg_proself_download_tool()
