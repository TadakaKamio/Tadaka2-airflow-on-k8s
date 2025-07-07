import pandas as pd
import os, traceback
from pyhive.exc import DatabaseError
from middle.common.hive_connect import ImpalaSingleton
import middle.common.hql_processor as hql_processor
import middle.common.utils as utils
import middle.common.log as log
import middle.common.constants_colums as constants

# loogerオブジェクト取得
logger = log.MiddleAppLog()

# "." "" "-"
DOT = constants.SpecialChars.DOT.value
BLANK = constants.SpecialChars.BLANK.value
HYPHEN = constants.SpecialChars.HYPHEN.value

@log.log_writer(logger)
def delete_file(_volume_path, _table_name, _file_name):
    import subprocess

    # hadoop fs -rm /hd/hd-volume-01/middle/
    # /hd/hd-volume-01/middle/
    _table_name = "area_info"
    _file_name = "000000_0"
    _volume_path = "/hd/hd-volume-01/middle/"
    target_data_list = ["999999999","001"]
    find_target_file(target_data_list,_table_name)
    out = subprocess.run(["hadoop", "fs", "-rm", "-r", 
                          _volume_path + "/" +  _table_name + "/" + _file_name],
                         capture_output=True)
    return out

def find_target_file(target_data_list, _table_name):
    # データの選択（ここではテキストファイルと仮定）
    target_data = target_data_list.join(",") # 主キーデータ

    # 対象ボリュームパス
    volume_path = "/hd/hd-volume-01/middle/"
    
    # ファイルの特定
    for filename in os.listdir(volume_path):
        if filename.startswith("000000_0"):  # ファイル名が特定のパターンに一致する場合
            file_path = os.path.join(volume_path, filename)
            with open(file_path, 'r') as file:
                data = file.read()
                if target_data in data:  # データがファイルに含まれる場合
                    print("目的のデータが含まれるファイル:", file_path)
                    # ここでファイルに対する必要な処理を実行する
                    return file_path
                    # break  # 最初に見つかったファイルのみを扱う場合
    
