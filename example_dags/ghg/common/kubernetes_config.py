import kubernetes.client.models as k8s

from ghg.common.log import MyAppLog, log_writer

logger = MyAppLog()


@log_writer(logger)
def get_k8s_config():
    """
    Kubernetes Podの設定を返す関数。

    Kubernetes上で動作するコンテナのプロキシ設定、リソース要求（メモリ）、
    および必要なボリュームのマウント設定を含むPod設定を生成します。
    これにより、コンテナがプロキシを介して外部リソースにアクセスし、
    必要な証明書を利用して安全な通信を行うことができます。

    戻り値:
        dict: Kubernetes Pod設定を含む辞書。
    """
    return {
        "pod_override": k8s.V1Pod(
            spec=k8s.V1PodSpec(
                containers=[
                    k8s.V1Container(
                        name="base",
                        env=[
                            k8s.V1EnvVar(
                                name="HTTP_PROXY", value="http://10.191.3.145:80"
                            ),
                            k8s.V1EnvVar(
                                name="http_proxy", value="http://10.191.3.145:80"
                            ),
                            k8s.V1EnvVar(
                                name="HTTPS_PROXY", value="http://10.191.3.145:80"
                            ),
                            k8s.V1EnvVar(
                                name="https_proxy", value="http://10.191.3.145:80"
                            ),
                        ],
                        resources=k8s.V1ResourceRequirements(
                            requests={"memory": "512Mi"},
                        ),
                        volume_mounts=[
                            k8s.V1VolumeMount(
                                name="hive-ssl-volume",
                                # ssl_truststore.pemのコンテナ内配置先パスを指定
                                mount_path="/tmp",
                            ),
                        ],
                    ),
                ],
                volumes=[
                    k8s.V1Volume(
                        name="hive-ssl-volume",
                        config_map=k8s.V1ConfigMapVolumeSource(
                            # ssl_truststore.pemに対応したconfigmap名に要書き換え
                            name="hive-ssl-config"
                        ),
                    ),
                ],
            ),
        ),
    }
