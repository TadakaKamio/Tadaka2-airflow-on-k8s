import json
import os
from stat import S_ISDIR

import paramiko


def transfer_file_between_servers(kubun):

    config_file = get_relative_path(r"sftp_tool/conf/variables_for_dev.json")

    with open(config_file, "r") as f:
        data = json.load(f)

    if kubun == "HD":
        source = "HD"
        target = "PG"
    else:
        source = "PG"
        target = "HD"

    source_config = data[source]["sftp"]
    source_host = source_config["host"]
    source_port = source_config["port"]
    source_user = source_config["user"]
    source_password = source_config["password"]

    target_config = data[target]["sftp"]
    target_host = target_config["host"]
    target_port = target_config["port"]
    target_user = target_config["user"]
    target_password = target_config["password"]

    source_dir = data[source]["source_dir"]
    target_dir = data[source]["target_dir"]

    # ソースサーバーのSSHクライアントをセットアップ
    source_client = paramiko.SSHClient()
    source_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    # ソースサーバーに接続
    source_client.connect(
        source_host, port=source_port, username=source_user, password=source_password
    )
    source_sftp = source_client.open_sftp()

    # ターゲットサーバーのSSHクライアントをセットアップ
    target_client = paramiko.SSHClient()
    target_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    # ターゲットサーバーに接続
    target_client.connect(
        target_host, port=target_port, username=target_user, password=target_password
    )
    target_sftp = target_client.open_sftp()

    # ファイル連携実行
    execute_transfer_file(source_sftp, target_sftp, source_dir, target_dir)

    source_sftp.close()
    target_sftp.close()
    source_client.close()
    target_client.close()


def execute_transfer_file(source_sftp, target_sftp, source_dir, target_dir):
    """
    ファイル連携実行

    パラメータ:
        source_sftp (str): ソースサーバーSFTPクライアント。
        target_sftp (str): ターゲットサーバーSFTPクライアント。
        source_dir (str): ソースサーバーディレクトリ。
        target_dir (str): ターゲットサーバーディレクトリ。

    戻り値:
        なし
    """
    dir_items = source_sftp.listdir_attr(source_dir)

    for item in dir_items:
        source_file_path = os.path.join(source_dir, item.filename).replace('\\', '/')
        target_file_path = os.path.join(target_dir, item.filename).replace('\\', '/')

        if S_ISDIR(item.st_mode):
            execute_transfer_file(
                source_sftp, target_sftp, source_file_path, target_file_path
            )
        else:
            # ファイル転送
            source_file = source_sftp.open(source_file_path, 'r')
            target_file = target_sftp.open(target_file_path, 'w')
            data = source_file.read()
            target_file.write(data)
            source_file.close()
            target_file.close()

            print(
                f"■ファイル連携済み：From【{source_file_path}】 TO【{target_file_path}】"
            )


def get_relative_path(file_name):
    """
    指定されたファイル名に対して、プロジェクトルートディレクトリからの相対パスを取得する。

    パラメータ:
        file_name (str): 相対パスを取得したいファイルの名前。

    戻り値:
        str: プロジェクトルートディレクトリからの相対パス。
    """
    # 現在のファイルが存在するディレクトリのパスを取得
    current_dir_path = os.path.dirname(os.path.abspath(__file__))

    # 現在のディレクトリの親ディレクトリのパスを取得
    parent_dir_path = os.path.dirname(current_dir_path)

    # 相対パスを組み立て
    return os.path.join(parent_dir_path, file_name)


def main(**kwargs):
    transfer_file_between_servers()
