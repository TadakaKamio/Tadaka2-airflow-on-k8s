"""
dags.py

このスクリプトはData FabricからProselfへファイルをアップロードします。

機能:
- Data FabricからProselfへファイルをアップロードします。

使用方法:
- GiteaにコードをPush後、AirflowからDAGを実行してください。
"""

import airflow
from airflow.decorators import dag, task
from airflow.models import Variable
from kubernetes.client import models as k8s

import ghg.proself_upload.utils as hdfs_download_utils
from ghg.common.log import MyAppLog
from ghg.common.utils import set_log_level

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
    dag_id="ghg_upload_files_to_proself",
    default_args=args,
    start_date=airflow.utils.dates.days_ago(2),
    schedule_interval=Variable.get("GHG_SCHEDULE_INTERVAL"),
)
def ghg_hdfs_download_tool():
    cpu_lim = Variable.get("GHG_PROSELF_UPLOAD_CPU_LIMIT")
    cpu_req = cpu_lim
    ram_lim = Variable.get("GHG_PROSELF_UPLOAD_MEMORY_LIMIT")
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
    def upload_files_to_proself(**kwargs):

        def _do():
            try:
                # Hadoop対象フォルダを指定
                base_path = Variable.get("GHG_PROSELF_UPLOAD_GET_BASE_PATH")
                sub_path = Variable.get("GHG_PROSELF_UPLOAD_GET_SUB_PATH")
                conpany_um = Variable.get("GHG_COMPANY_UM")
                # # アップロードするファイルのパス
                proself_upload_base_url = Variable.get("GHG_PROSELF_UPLOAD_BASE_URL")
                proself_upload_sub_path = Variable.get("GHG_PROSELF_UPLOAD_SUB_PATH")
                proself_auth = Variable.get(
                    "GHG_PROSELF_UPLOAD_PROSELF_AUTH", deserialize_json=True
                )

                # Hadoopから対象ファイルを取得
                logger.info("Hadoopからファイル取得開始")
                files_io = hdfs_download_utils.get_file_from_hadoop(
                    base_path, sub_path, conpany_um
                )
                logger.info("Hadoopからファイル取得終了")

                logger.info("proselfへファイルアップロード開始")
                for file_path, file_io in files_io.items():
                    file_names = hdfs_download_utils.basename(file_path)
                    logger.info("file_names is：" + str(file_names))

                    url = hdfs_download_utils.pathjoin(
                        proself_upload_base_url, proself_upload_sub_path
                    )
                    url = url + "/" + file_names
                    logger.info("upload url is " + str(url))
                    logger.info("file_path url is " + str(file_path))
                    logger.info("file_name url is " + str(file_names))

                    # 取得したファイルをproselfへアップロードする
                    response = hdfs_download_utils.put_file_to_proself(
                        url, file_names, file_io, proself_auth
                    )
                    if not response.ok:
                        msg = (
                            f"put_file is failed. file name is {file_names}. "
                            f"put path is {url} "
                        )
                        logger.error(msg)
                        raise Exception(msg)
                    # レスポンスのステータスコードを確認
                    print(f"Status Code: {response.status_code}")
                    # レスポンスの本文を出力（エラーメッセージ等があれば表示される）
                    print(f"Response Body: {response.text}")
                    logger.info("proselfへファイルアップロード終了")

            except Exception as e:
                logger.error(
                    f"「upload_files_to_proself関数を実行時、エラーが発生しました。エラーメッセージ : {e}"
                )
                raise e

        return _do()

    upload_files_to_proself()


ghg_hdfs_download_tool()
