"""
テスト対象: middle_download.py
- このテストコードはテスト対象コードの実行によりコールされる(test_flagをTrueに設定した場合)

テスト方針
- テスト対象DAGのTask単位で期待する結果が得られるかテストを行う

テストケース
[get_file_list]
- DAGコード内で定義された変数のdownload_listの内容と取得を期待するファイルリストの内容が一致している事
[download_files] 
- EDFの指定したPATH内に取得を期待するファイルが存在している事

テスト方法
- ダウンロードを期待するファイル名をAirflow Variablesの"test_p001_expect_files"に設定
    e.g.: ["D30_TELEMETER_20231106-20231101.csv.gz", "MAST_CTN_20231111.csv.gz.003", "Mast_JYSKY_20231003.csv.bat"] 
- DTaps接続名をAirflow Variablesの"middle_download_put_base_path"に設定 (DAGコードで使用する変数と同一)
- フラグファイルが配置されるPATHをAirflow Variablesの"middle_download_ignore_files_dir"に設定 (DAGコードで使用する変数と同一)
- ダウンロードされたファイルが配置されるPATHをAirflow Variablesの"middle_download_put_inputfiles_path"に設定 (DAGコードで使用する変数と同一)

注意
- "test_p001_expect_files"に指定した取得を期待するファイルは、"middle_download_ignore_files_dir"に設定したEDFのPATHに既に存在する場合は削除される (テスト自動化のため)
"""

from airflow.models import Variable
from os.path import exists
from pyarrow import fs
import json

# Airflow Variable Check
## Use same Variables as Dag Codes deliberately
test_flag = Variable.get("middle_download_test",
                         default_var="false")  # Test Flag
dtap_path = Variable.get("middle_download_put_base_path",
                         default_var="dtap://test")
flag_file_path = Variable.get("middle_download_ignore_files_dir")
data_file_path = Variable.get("middle_download_put_inputfiles_path")
expect_download_list_str = Variable.get("middle_test_expect_files")
expect_download_list = json.loads(expect_download_list_str)

if test_flag.lower() in ['true', '1', 'yes', 'maybe', 'yeah', 'yup']:
    test_flag = True
else:
    test_flag = False


def task_test(name):
    if test_flag:
        if name == "get_file_list":

            def _test(task):
                ###
                # Proselfに以下をおいている前提です。
                # - ディレクトリに含まれたファイル
                # - 取得予定のないファイル
                # - 取得予定のファイル
                ###
                def _get_file_list_test(
                        *args):  # this method name should be same as task name
                    flag_file_list, deleted_files = _delete_files_if_exist()
                    print(f"Already existing files deleted: {deleted_files}")
                    res = task(*args)
                    print(res)

                    print(
                        f"########################## Task TEST: {name} #################################"
                    )
                    print("TEST: Check download list")

                    # diff expect files and dags actually files
                    # remove path from actually files (need only file name)
                    extracted_filenames = [path.split('/')[-1] for path in res]
                    print(f"splited actually file list: {extracted_filenames}")
                    set_res = set(extracted_filenames)
                    set_expect = set(expect_download_list)

                    if set_expect == set_res:
                        print(
                            f"Already existing files deleted: {deleted_files}")
                        print(f"DAGs actually download list: {res}")
                        print(
                            f"Expected download list: {expect_download_list}")
                        print("Test Passed.")
                    else:
                        # expect_download_listにあってresにない要素
                        missing_in_res = set_expect - set_res
                        # resにあってexpect_download_listにない要素
                        extra_in_res = set_res - set_expect

                        if missing_in_res:
                            print(
                                f"Already existing files deleted: {deleted_files}"
                            )
                            print(f"DAGs actually download list: {res}")
                            print(
                                f"Expected download list: {expect_download_list}"
                            )
                            raise ValueError(
                                f"Missing in 'download_list': {missing_in_res}"
                            )
                        if extra_in_res:
                            print(
                                f"Already existing files deleted: {deleted_files}"
                            )
                            print(f"DAGs actually download list: {res}")
                            print(
                                f"Expected download list: {expect_download_list}"
                            )
                            raise ValueError(
                                f"Missing in 'expect_download_list': {extra_in_res}"
                            )
                        raise ValueError("Exception")
                    print(
                        "########################################################################"
                    )
                    return res

                return _get_file_list_test

            return _test
        if name == "download_files":  # this method name should be same as task name

            def _test(task):

                def _download_files_test(*args):

                    res = task(*args)

                    file_check_result = _check_all_files_exist()

                    print(
                        f"########################## Task TEST: {name} #################################"
                    )
                    print("TEST: where expected file exists")
                    if file_check_result[0]:
                        print(f"All existing files: {file_check_result[1]}")
                        print(f"Expected files: {expect_download_list}")
                        print("Test Passed.")
                    else:
                        print(f"All existing files: {file_check_result[1]}")
                        print(f"Expected files: {expect_download_list}")
                        if file_check_result[2]:
                            print("Test Failed")
                            raise ValueError(
                                f"The following files do not exist: {file_check_result[2]}"
                            )
                        else:
                            print("Test Failed")
                            raise ValueError("Exception error")
                    print(
                        "########################################################################"
                    )
                    return res

                return _download_files_test

            return _test
        else:

            def _test(task):

                def _others(*args):
                    res = task(*args)
                    print(
                        f"########################## Task TEST: {name} #################################"
                    )
                    print("Skipped...")
                    print(f"Not defined test: {name}")
                    print(
                        "########################################################################"
                    )
                    return res

                return _others

            return _test
    else:

        def _no_test(task):

            def _wrapper(*args):
                print(
                    f"########################## TEST Skipped: {name} #################################"
                )
                res = task(*args)
                return res

            return _wrapper

        return _no_test


# Test Methods


def _delete_files_if_exist():
    dtapfs = fs.HadoopFileSystem.from_uri(dtap_path)
    print(expect_download_list)

    file_list_info = dtapfs.get_file_info(
        fs.FileSelector(flag_file_path, recursive=True))
    flag_file_list = [
        info.path.split('/')[-1] for info in file_list_info
        if info.type == fs.FileType.File
    ]

    print(flag_file_list)

    # Example:
    # [2023-11-16, 10:17:51 JST] {logging_mixin.py:137} INFO - ['D30_HI_KK_20231106-20231101.csv.gz', 'D30_TELEMETER_20231106-20231101.csv.gz', 'MAST_CTN_20231111.csv.gz.001', 'MAST_CTN_20231111.csv.gz.002', 'MAST_CTN_20231111.csv.gz.003', 'MAST_CTN_20231111.csv.gz.004', 'MAST_HTSHAKY_20231101.csv.gz', 'haiden_setsubi_231111-1115.tar.Z']
    deleted_files = []

    for file_name in expect_download_list:
        if file_name in flag_file_list:

            file_to_delete = f"{flag_file_path}/{file_name}"

            dtapfs.delete_file(file_to_delete)
            deleted_files.append(file_to_delete)

            print(f"Deleted file: {file_to_delete}")
    return flag_file_list, deleted_files


def _check_all_files_exist():
    # Dtaps接続
    dtapfs = fs.HadoopFileSystem.from_uri(dtap_path)
    # 対象のPATHに存在するファイルリストを取得
    file_list_info = dtapfs.get_file_info(
        fs.FileSelector(data_file_path, recursive=True))
    existing_files = [
        info.path.split('/')[-1] for info in file_list_info
        if info.type == fs.FileType.File
    ]

    # 対象のPATHに存在するファイルリストの中に期待するファイルすべてが含まれているかどうかをチェック
    all_files_exist = all(file in existing_files
                          for file in expect_download_list)

    # 存在しないファイルをリスト化
    missing_files = [
        file for file in expect_download_list if file not in existing_files
    ]

    return all_files_exist, existing_files, missing_files
