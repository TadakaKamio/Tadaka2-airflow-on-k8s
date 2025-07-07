import os
import sys
from middle.common.log import MiddleAppLog,log_writer

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

logger = MiddleAppLog()

@log_writer(logger)
def ls_volume(_path):
    import subprocess
    """ expect like this
    drwxr-xr-x   - kishikawa [playground, dev]          0 2023-10-12 02:43 dtap://test/volume8/lake
    drwxr-xr-x   - kishikawa [playground, dev]          0 2023-10-12 02:43 dtap://test/volume8/lake/CNST_ADDRESS
    drwxr-xr-x   - kishikawa [playground, dev]          0 2023-10-12 02:43 dtap://test/volume8/lake/CNST_ADDRESS/work
    drwxr-xr-x   - kishikawa [playground, dev]          0 2023-10-12 02:43 dtap://test/volume8/lake/CNST_GYOUSHU
    drwxr-xr-x   - kishikawa [playground, dev]          0 2023-10-12 02:43 dtap://test/volume8/lake/CNST_GYOUSHU/work
    drwxr-xr-x   - kishikawa [playground, dev]          0 2023-10-12 02:43 dtap://test/volume8/lake/CNST_KK_KATA
    """
    ls_out = subprocess.run(["hdfs", "dfs", "-ls", "-R", _path],
                            encoding='utf-8',
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    if ls_out.returncode != 0:
        msg = f'hdfs dfs -ls command is failed. path is {_path}. stdout is {ls_out.stdout}. stderr is {ls_out.stderr}'
        logger.error(msg)
        raise Exception(msg)
    exist_files = [_line.split() for _line in ls_out.stdout.splitlines()[0:]]
    exist_files = [basename(_line[-1]) for _line in exist_files]
    return exist_files


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


@log_writer(logger)
def get_list(_url, _auth):
    import requests
    from requests.auth import HTTPBasicAuth

    headers = {
        'Depth': '1',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = "<D:propfind xmlns:D='DAV:' xmlns:Z='http://www.northgrid.co.jp/proself/'><D:prop></D:prop></D:propfind>"
    response = requests.request('PROPFIND',
                                _url,
                                headers=headers,
                                data=data,
                                verify=False,
                                auth=HTTPBasicAuth(_auth["user"],
                                                   _auth["password"]))
    check_status(response.status_code)

    return response.content


# xml形式のresponceからファイルパスのリストを取得
@log_writer(logger)
def xml_to_list(content, _get_path):
    import re
    from urllib.parse import unquote

    path_pattern = '<D:href>(.*)</D:href>'
    sentence = unquote(content)
    _file_list = [find_str for find_str in re.findall(path_pattern, sentence)]
    # 1番目はcurrent dirなので捨てる
    _folder_list = [_item for _item in _file_list if not isfile(_item)][1:]
    _file_list = [_file for _file in _file_list if isfile(_file)]

    return _file_list, _folder_list


@log_writer(logger)
def recursive_get_list(_base_url, _get_path, _auth, _files=None):
    if _files is None:
        _files = []

    url = make_proself_url(_base_url, _get_path)
    content = get_list(url, _auth)

    file_list, folder_list = xml_to_list(content.decode(), _get_path)
    _files += file_list

    for folder in folder_list:
        folder = folder.split('/')[-2]
        if folder == 'old': continue
        _files = recursive_get_list(_base_url, pathjoin(_get_path, folder),
                                    _auth, _files)

    return _files


@log_writer(logger)
def make_proself_url(_base_url, _file_path):
    from urllib.parse import quote

    _file_path = quote(_file_path)
    return pathjoin(_base_url, _file_path)


@log_writer(logger)
def get_file(_url, _local_path, _auth):
    import requests
    from io import BytesIO
    from requests.auth import HTTPBasicAuth

    # 未格納ファイルをダウンロード
    response = requests.get(_url,
                            auth=HTTPBasicAuth(_auth["user"],
                                               _auth["password"]),
                            verify=False)
    check_status(response.status_code)

    # ローカルにダウンロードしたファイルを書き出し
    with open(_local_path, "wb") as f:
        f.write(response.content)

    return _local_path


# 引数のファイルがVariables"middle_download_filter_taget_files"に含まれているか確認する
@log_writer(logger)
def filter_target_file(file_name):
    import json
    import re
    from airflow.models import Variable
    filter_str = Variable.get("middle_download_filter_taget_files")
    filter_list = _load_json_to_list(filter_str)
    try:
        for filter_str in filter_list:
            if file_name.lower().startswith(filter_str.lower()):
                return True
    except Exception as e:
        logger.error(f'error in filter list area. error message : {e}')
        raise e

    return False


@log_writer(logger)
def put_file(_local_path, _put_path):
    import subprocess

    out = subprocess.run(["hadoop", "fs", "-put", _local_path, _put_path],
                         capture_output=True)
    return out

@log_writer(logger)
def make_folder(_full_path):
    import subprocess
    
    out = subprocess.run(["hdfs", "dfs", "-mkdir", "-p", _full_path],
                         capture_output=True)
    return out

@log_writer(logger)
def remove_local_file(_local_path):
    from pathlib import Path
    
    Path(_local_path).unlink(missing_ok=True)
    is_exist = Path(_local_path).exists()
    return not is_exist


# VariablesのJson文字列からlistに変換する
def _load_json_to_list(_json_file):
    import json
    try:
        target_list = json.loads(_json_file)
    except Exception as e:
        logger.error(f'error in target list area. error message : {e}')
        raise e

    return target_list


def _splittext(_path):
    import os
    return os.path.splitext(_path)


def basename(_path):
    import os
    return os.path.basename(_path)


def pathjoin(*_path_list):
    import os
    _path_list = [
        _path[1:] if _path[0] == '/' else _path for _path in _path_list
    ]
    _path_list = [
        _path[:-1] if ((_path[-1] == '/') and (_path[-3:] != '://')) else _path
        for _path in _path_list
    ]
    return os.path.join(*_path_list)


def isfile(_path):
    return bool(_splittext(_path)[1])
