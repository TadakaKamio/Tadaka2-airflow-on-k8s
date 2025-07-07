import datetime
import numbers
import os
import subprocess
import sys
from decimal import ROUND_HALF_UP, Decimal
from importlib.metadata import distribution
from io import BytesIO

import pandas as pd
import pytz

import ghg.common.settings as Constants
from ghg.common.log import MyAppLog, log_writer

logger = MyAppLog()


def set_log_level(run_mode):
    """
    AirflowのVariableから実行モードに応じてログレベルを設定する。
    - 開発環境、ステージング環境ではDEBUGレベル
    - 本番環境ではINFOレベル

    パラメータ:
        run_mode (str): 実行モード

    戻り値:
        なし
    """
    if run_mode == Constants.RunMode.DEV.value:
        os.environ["LOG_LEVEL"] = "DEBUG"
    elif run_mode == Constants.RunMode.STG.value:
        os.environ["LOG_LEVEL"] = "DEBUG"
    elif run_mode == Constants.RunMode.PROD.value:
        os.environ["LOG_LEVEL"] = "INFO"


def print_progress_bar(
    iteration,
    total,
    prefix="Progress:",
    suffix="Complete",
    decimals=1,
    length=50,
    fill="█",
):
    """
    プロセスの進行状況をグラフィカルに表示する関数。
    - 進行状況のパーセンテージとバーで現在の進捗を表示する。
    - ロガーを使用してAirflowのログに情報を記録する。

    パラメータ:
        iteration (int): 現在のイテレーション数
        total (int): 総イテレーション数
        prefix (str): プログレスバーの前に表示するテキスト
        suffix (str): プログレスバーの後に表示するテキスト
        decimals (int): 進行状況のパーセンテージ表示における小数点以下の桁数
        length (int): プログレスバーの長さ
        fill (str): プログレスバーの充填に使用する文字

    戻り値:
        なし
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + "-" * (length - filled_length)
    logger.info(f"{prefix} |{bar}| {percent}% {suffix} 【{iteration}/{total}】")


@log_writer(logger)
def check_install_package(package_name):
    """
    指定されたPythonパッケージが既にインストールされているかをチェックし、インストールされていない場合はインストールを試みます。

    パラメータ:
        package_name (str): チェックおよびインストールが必要なパッケージ名。

    戻り値:
        None
    """
    try:
        # パッケージがインストールされているかどうかを確認するためにインポートを試みます
        dist = distribution(package_name)
        logger.info(
            f"{package_name} は既にインストールされています。バージョン: {dist.version}"
        )
    except Exception:
        # パッケージがインストールされていないため、pipを使ってインストールを試みます
        logger.info(
            f"{package_name} はインストールされていません。インストールを試みます..."
        )
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name]
            )
            logger.info(f"{package_name} のインストールが成功しました。")
        except Exception as e:
            logger.error(f"{package_name} のインストール中にエラーが発生しました：{e}")


@log_writer(logger)
def get_current_date():
    """
    現在の日付を"YYYY-MM-DD"形式の文字列で取得する。

    パラメータ:
        なし

    戻り値:
        str: 現在の日付を表す文字列。
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")


@log_writer(logger)
def get_current_timestamp():
    """
    現在のタイムスタンプを"YYYY-MM-DD HH:MM:SS"形式の文字列で取得する。

    パラメータ:
        なし

    戻り値:
        str: 現在のタイムスタンプを表す文字列。
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@log_writer(logger)
def get_current_tokyo_timestamp():
    """
    タイムゾーンが東京現在のタイムスタンプを"yyyyMMddHMS"形式の文字列で取得する。

    パラメータ:
        なし

    戻り値:
        str: 東京現在のタイムスタンプを表す文字列。
    """
    # タイムゾーンが取得する
    timezone = pytz.timezone("Asia/Tokyo")
    # UTC時間が東京時間を変換する
    local_time = datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(timezone)
    return local_time.strftime("%Y%m%d")


@log_writer(logger)
def get_current_tokyo_timestamp2():
    """
    タイムゾーンが東京現在のタイムスタンプを"yyyyMMddHMS"形式の文字列で取得する。

    パラメータ:
        なし

    戻り値:
        str: 東京現在のタイムスタンプを表す文字列。
    """
    # タイムゾーンが取得する
    timezone = pytz.timezone("Asia/Tokyo")
    # UTC時間が東京時間を変換する
    local_time = datetime.datetime.now().replace(tzinfo=pytz.utc).astimezone(timezone)
    return local_time.strftime("%Y-%m-%d %H:%M:%S")


@log_writer(logger)
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


@log_writer(logger)
def value_trans_formation(value):
    """
    float型の場合は、整数・小数合計で15(小数点含まず)桁のデータに変換する。

    パラメータ:
        value (any): Excelの読み込むデータ

    戻り値:
        value: 変換後のデータ。
    """
    if isinstance(value, float):
        if value < 1:
            format_value = float("{:.14g}".format(round(value, 14)))
        else:
            format_value = float("{:.15g}".format(value))
        return format_value
    else:
        return value


@log_writer(logger)
def round_to_decimal(value, precision):
    """
    指定桁数によりデータを変換する。

    パラメータ:
        value (any): Excelの読み込むデータ
        precision (int): 小数点以下の桁数

    戻り値:
        value (Decimal): 変換後のデータ
    """
    value_as_decimal = Decimal(str(value))
    rounding_factor = Decimal("1e-{}".format(precision))
    rounded_value = value_as_decimal.quantize(rounding_factor, rounding=ROUND_HALF_UP)
    return rounded_value


@log_writer(logger)
def round_to_str(value, precision):
    """
    指定桁数によりデータを変換する。

    パラメータ:
        value (any): Excelの読み込むデータ
        precision (int): 小数点以下の桁数

    戻り値:
        value (str): 変換後のデータ
    """
    value_as_decimal = Decimal(str(value))
    rounding_factor = Decimal("1e-{}".format(precision))
    rounded_value = value_as_decimal.quantize(rounding_factor, rounding=ROUND_HALF_UP)
    return str(rounded_value)


@log_writer(logger)
def turn_excel_item_to_dict(df, keyRow, valueRow, startCol, endCol):
    """
    指定表、特定表中の項目と値を辞書に変換する。
    ※当該変換の固定フォーマットのインプットが必要です、汎用はできません。

    例えば:Excelに項目「name:桃太郎」を変換して、{"name":"桃太郎"}

    パラメータ:
        df:pandas DataFrameタイプのデータ
        keyRow:項目keyの行(固定フォーマットの行インデックス)
        valueRow:項目valueの行(固定フォーマットの行インデックス)
        startCol:変換対象項目の開始列(固定フォーマットの列インデックス)
        endCol:変換対象項目の終了列(固定フォーマットの列インデックス)

    戻り値:
        itemData:変換後の辞書データ
        lastCol:変換対象の最後列(固定フォーマットの列インデックス)
    """
    lastCol = startCol
    itemData = {}

    col = startCol
    while col <= endCol:
        lastCol = col
        itemValue = df.iloc[valueRow, col]
        if isinstance(itemValue, str) and len(itemValue) != 0 and itemValue[0] == "$":
            cellInfo = itemValue.split("_")
            itemData[df.iloc[keyRow, col]], lastCol = turn_excel_item_to_dict(
                df, keyRow, valueRow, int(cellInfo[1]), int(cellInfo[2])
            )
        elif isinstance(itemValue, str) and len(itemValue) != 0 and itemValue[0] == "@":
            cellInfo = itemValue.split("_")
            itemData[df.iloc[keyRow, col]] = turn_excel_list_to_dict(
                df,
                int(cellInfo[1]),
                int(cellInfo[2]),
                int(cellInfo[3]),
                int(cellInfo[4]),
            )
        else:
            itemData[df.iloc[keyRow, col]] = value_trans_formation(
                df.iloc[valueRow, col]
            )
        col = lastCol + 1

    return itemData, lastCol


@log_writer(logger)
def turn_excel_list_to_dict(df, startCol, startRow, endCol, endRow):
    """
    指定表、特定表中のリストの項目と値を辞書に変換する。
    ※当該変換の固定フォーマットのインプットが必要です、汎用はできません。

    パラメータ:
        df:pandas DataFrameタイプのデータ
        startCol:変換対象項目の開始列(固定フォーマットの列インデックス)
        startRow:変換対象項目の開始行(固定フォーマットの行インデックス)
        endCol:変換対象項目の終了列(固定フォーマットの列インデックス)
        endRow:変換対象項目の終了行(固定フォーマットの行インデックス)

    戻り値:
        listData:変換後の辞書データ
    """
    arrayData = []
    parentKey = df.iloc[startRow, startCol]
    row = startRow + 2
    while row <= endRow:
        rowData = {}
        col = startCol
        # この行の一番目は空白以外、またはこの行は必須出力(一番目項目の前の列に「!」を付く)
        if df.iloc[row, col] is not None or df.iloc[row, col - 1] == "!":
            while col <= endCol:
                object, alastCol = turn_excel_item_to_dict(
                    df, startRow + 1, row, col, col
                )  # 指定Objectを取得する
                rowData[df.iloc[startRow + 1, col]] = list(object.values())[0]
                col = alastCol + 1
            nameRowData = {}
            nameRowData[parentKey] = rowData
            arrayData.append(nameRowData)
        row += 1

    return arrayData


@log_writer(logger)
def cleaned_json(json_str):
    """
    指定表、特定表中のJSON項目のエスケープシーケンスの変換。
    ※json中の \n → \\n を変換

    パラメータ:
        json_str:json文字列

    戻り値:
        cleaned_data:変換後のjsonデータ
    """
    cleaned_data = json_str.replace("\n", "\\n").replace("\t", "\\t")
    return cleaned_data


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
            if not file_path.endswith((Constants.CSVExtension.CSV.value,)):
                logger.warn(f"{file_path}がcsvファイルではありません。")
                continue

            # HadoopからファイルのBytesIOを取得
            file_io = get_hadoop_file_io(file_path)

            if not file_io:
                logger.warn(f"{file_path}のBytesIOを取得できません。")
                continue

            files_io[file_path] = file_io

    return files_io


@log_writer(logger)
def get_target_paths(base_path, sub_path, key):
    target_paths = []

    edited_path = get_joined_path(base_path, sub_path)

    if key == Constants.CompanyUM.UM_ALL.value:
        target_paths = [
            get_joined_path(edited_path, d)
            for d in [
                Constants.CompanyUM.UM_HD.value,
                Constants.CompanyUM.UM_EP.value,
                Constants.CompanyUM.UM_RP.value,
            ]
        ]
    else:
        target_paths.append(get_joined_path(edited_path, key))

    return target_paths


@log_writer(logger)
def get_joined_path(*path_list):
    path_list = [path.strip("/") for path in path_list]
    return "/".join(path_list)


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
def get_hadoop_file_io(file_path):
    command = ["hadoop", "fs", "-cat", file_path]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        logger.error(f"Error reading file {file_path}: {result.stderr}")
        return None

    return BytesIO(result.stdout)


# Hadoopコマンドを使ってファイルに書き込む
def put_file_to_hadoop(file, file_path):
    with BytesIO(file.encode("utf-8")) as file_io:
        command = ["hadoop", "fs", "-put", "-", file_path]

        result = subprocess.run(
            command,
            input=file_io.read(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            logger.error(
                f"Error writing file to Hadoop "
                f"{file_path}: {result.stderr.decode('utf-8')}"
            )

        logger.info(f"XML file successfully written to Hadoop {file_path}")


def put_fileio_to_hadoop(file_io, file_path):
    command = ["hadoop", "fs", "-put", "-", file_path]

    result = subprocess.run(
        command,
        input=file_io.read(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        logger.error(
            f"Error writing file to Hadoop "
            f"{file_path}: {result.stderr.decode('utf-8')}"
        )

    logger.info(f"XML file successfully written to Hadoop {file_path}")


def mul(*args):
    """計算用の変数が数字以外の場合、0として計算する"""
    ret = 1
    for arg in args:
        if isinstance(arg, pd.Series):
            arg = arg.apply(
                lambda x: x if isinstance(x, (numbers.Number, Decimal)) else 0
            )
        elif not isinstance(arg, (numbers.Number, Decimal)):
            arg = 0
        ret *= arg
    return ret
