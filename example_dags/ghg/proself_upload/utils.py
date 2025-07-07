import os
import subprocess
import sys
from io import BytesIO

import ghg.common.settings as Constants
from ghg.common.log import MyAppLog, log_writer

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

logger = MyAppLog()


@log_writer(logger)
def get_file_from_hadoop(base_path, sub_path, key):
    files_io = {}

    # Hadoop対象フォルダを取得
    target_paths = get_target_paths(base_path, sub_path, key)
    logger.debug(f"target_paths {target_paths}")

    for target_path in target_paths:
        # Hadoop対象ファイルパスを取得
        file_paths = get_hadoop_file_paths(target_path)

        if not file_paths:
            logger.warn(
                f"Hadoop対象フォルダ:{target_path}がありません、または、フォルダにファイルがありません。"
            )
            continue

        for file_path in file_paths:

            # HadoopからファイルのBytesIOを取得
            file_io = get_hadoop_file_io(file_path)

            if not file_io:
                logger.warn(f"{file_path}のBytesIOを取得できません。")
                continue

            files_io[file_path] = file_io

    return files_io


@log_writer(logger)
def get_hadoop_file_io(file_path):
    command = ["hadoop", "fs", "-cat", file_path]
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False
    )
    if result.returncode != 0:
        logger.error(f"Error reading file {file_path}: {result.stderr}")
        return None

    return BytesIO(result.stdout)


@log_writer(logger)
def get_target_paths(base_path, sub_path, key):
    target_paths = []

    edited_path = get_joined_path(base_path, sub_path)

    if key == Constants.CompanyUM.UM_ALL.value:
        target_paths = [
            get_joined_path(edited_path, d)
            for d in [
                Constants.CompanyUM.UM_PG.value,
                Constants.CompanyUM.UM_HD.value,
                Constants.CompanyUM.UM_EP.value,
                Constants.CompanyUM.UM_RP.value,
            ]
        ]
    else:
        target_paths.append(get_joined_path(edited_path, key))

    return target_paths


@log_writer(logger)
def get_hadoop_file_paths(path):
    command = ["hadoop", "fs", "-ls", path]
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8"
    )
    if result.returncode != 0:
        logger.error(f"Error listing files in {path}: {result.stderr}")
        return []
    lines = result.stdout.splitlines()
    files = [line.split()[-1] for line in lines[1:]]
    return files


@log_writer(logger)
def get_joined_path(*path_list):
    path_list = [path.strip("/") for path in path_list]
    return "/".join(path_list)


@log_writer(logger)
def put_file_to_proself(_url, _file_names, _file_io, _auth):
    import requests
    from requests.auth import HTTPBasicAuth

    # ファイルをproselfへアプロードする
    headers = {
        "Content-Type": "application/octet-stream",
        "Content-Disposition": f'attachment; filename="{_file_names}"',
    }
    response = requests.put(
        _url,
        headers=headers,
        data=_file_io,
        auth=HTTPBasicAuth(_auth["user"], _auth["password"]),  # ベーシック認証
        verify=False,
    )
    check_status(response.status_code)

    return response


# ステータスコードが400,500番台の時raiseする
@log_writer(logger)
def check_status(code):
    code = int(code)
    if code >= 500:
        msg = "Check webdav service status. code was " + str(code)
        logger.error(msg)
        raise Exception(msg)

    elif code >= 400:
        msg = "something wrong to connect webdav target. code was " + str(code)
        logger.error(msg)
        raise Exception(msg)


def basename(_path):
    import os

    return os.path.basename(_path)


def make_proself_url(_base_url, _file_path):
    from urllib.parse import quote

    _file_path = quote(_file_path)
    return pathjoin(_base_url, _file_path)


def pathjoin(*_path_list):
    import os

    _path_list = [_path[1:] if _path[0] == "/" else _path for _path in _path_list]
    _path_list = [
        _path[:-1] if ((_path[-1] == "/") and (_path[-3:] != "://")) else _path
        for _path in _path_list
    ]
    return os.path.join(*_path_list)
