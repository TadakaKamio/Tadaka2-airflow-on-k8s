import kubernetes.client.models as k8s
from airflow.models import Variable
import middle.common.log as log
from middle.common.utils import get_json_config


logger = log.MiddleAppLog()

@log.log_writer(logger)
def get_k8s_config():
    # 設定値格納用JSONファイルを読み込む
    config = get_json_config()
    proxyURL = config["k8s"]["proxyURL"]
    return {
        "pod_override": k8s.V1Pod(
            spec = k8s.V1PodSpec(
                containers = [
                    k8s.V1Container(
                        name = "I-am-rich",
                        env = [k8s.V1EnvVar(
                            name = "HTTP_PROXY",
                            value = proxyURL
                            ),
                            k8s.V1EnvVar(
                            name = "http_proxy",
                            value = proxyURL
                            ),
                            k8s.V1EnvVar(
                            name = "HTTPS_PROXY",
                            value = proxyURL
                            ),
                            k8s.V1EnvVar(
                            name = "https_proxy",
                            value = proxyURL
                            ),
                        ],
                        resources = k8s.V1ResourceRequirements(
                            requests = {
                                # "memory": "512Mi"
                                "memory": "1Gi"
                            },
                        ),
                        volume_mounts = [
                            k8s.V1VolumeMount(
                                name = config["k8s"]["volumeMountsName"],
                                mount_path = config["k8s"]["volumeMountsPath"], # ssl_truststore.pemのコンテナ内配置先パスを指定。
                            ),
                        ],
                    ),
                ],
                volumes = [
                    k8s.V1Volume(
                        name = config["k8s"]["volumeMountsName"],
                        config_map = k8s.V1ConfigMapVolumeSource(
                            name = config["k8s"]["configMap"], # ssl_truststore.pemに対応したconfigmap名に要書き換え
                        ),
                    ),
                ],
            ),
        ),
    }

def get_proself_k8s_config():
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
    return pod_config