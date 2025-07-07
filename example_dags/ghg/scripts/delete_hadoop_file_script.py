import os
import subprocess

from airflow.models import Variable

from ghg.common.log import MyAppLog, log_writer

logger = MyAppLog()


@log_writer(logger)
def delete_hadoop_file(**kwargs):
    """
    関数名：Hadoop上のファイル又はフォルダを削除

    Hadoop上のファイル又はフォルダを削除する処理

    パラメータ:
        なし

    戻り値:
        なし
    """

    try:
        logger.info("処理開始")

        # Hadoop対象フォルダを指定
        base_path = Variable.get("GHG_HADOOP_BASE_PATH")
        file_path = Variable.get("GHG_DELETE_HADOOP_FILES_PATH", deserialize_json=True)

        # ファイルパースがリストを判断する
        if not isinstance(file_path, list):
            file_paths = [file_path]
        else:
            file_paths = file_path

        # コマンドを初期化
        command = ["hadoop", "fs", "-rm"]

        # ファイルパースをルプー
        full_paths = []
        need_r_flag = False
        for file_path in file_paths:
            # パースをスプライス
            full_path = f"{base_path}{file_path}"

            # 拡張子があるかどうかを判断する
            if not os.path.splitext(file_path)[1]:
                need_r_flag = True
            full_paths.append(full_path)
        if need_r_flag:
            command.insert(3, "-r")
        command.extend(full_paths)

        logger.info(f"ファイル削除パースは:{full_paths}")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            logger.error(f"{result.stderr.decode('utf-8')}")
        logger.info(f"▲--->{command}")
        logger.info(f"■--->{result.stdout}")

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        logger.info("処理終了")
