from enum import Enum


class RunMode(Enum):
    """
    実行環境のモードを定義するEnumクラス。

    - DEV: 開発環境を表します。
    - STG: ステージング環境を表します。
    - PROD: 本番環境を表します。
    """

    DEV = "dev"
    STG = "stg"
    PROD = "prod"


class ExcelExtension(Enum):
    """
    Excelファイルの拡張子を定義するEnumクラス。

    - XLSX: Excelファイルの拡張子が.xlsxの場合。
    - XLS: Excelファイルの拡張子が.xlsの場合。
    - XLSM: Excelファイルの拡張子が.xlsmの場合。
    """

    XLSX = ".xlsx"
    XLS = ".xls"
    XLSM = ".xlsm"
    
class CSVExtension(Enum):
    """
    CSVファイルの拡張子を定義するEnumクラス。

    - CSV: CSVファイルの拡張子が.CSVの場合。
    """

    CSV = ".csv"


class DBoperation(Enum):
    """
    DB操作を定義するEnumクラス。

    - NONE: 検索不要の場合。
    - FETCHALL: 全件検索の場合。
    - FETCHONE: 1件検索の場合。
    """

    NONE = ""
    FETCHALL = "fetchall"
    FETCHONE = "fetchone"


class XMLExtension(Enum):
    """
    XMLファイルの拡張子を定義するEnumクラス。
    """

    XML = ".xml"


class Number(Enum):
    """
    基本数字を定義するEnumクラス。
    """

    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2
    NUMBER_3 = 3
    NUMBER_4 = 4
    NUMBER_5 = 5
    NUMBER_6 = 6
    NUMBER_7 = 7
    NUMBER_8 = 8
    NUMBER_9 = 9
    NUMBER_10 = 10
    NUMBER_11 = 11
    NUMBER_12 = 12
    NUMBER_13 = 13


class CompanyUM(Enum):
    """
    会社名略称を定義するEnumクラス。
    """

    UM_ALL = "ALL"
    UM_PG = "PG"
    UM_HD = "HD"
    UM_EP = "EP"
    UM_RP = "RP"
    UM_FP = "FP"


class PackageName(Enum):
    """
    各パッケージのEnumクラス。
    """

    # PANDAS実行エンジン
    PANDAS_ENGINE = "openpyxl"
    # impyla実行エンジン
    IMPYLA = "impyla"
    # dicttoxml実行エンジン
    DICTTOXML = "dicttoxml"
    # chardet実行エンジン
    CHARDET = "chardet"


# XML構造書パス（このパスは仮想のものです。テストをローカルで行う必要がある場合は、担当者は自分のローカルパスに設定してください。）
FOLDER_PATH_XML_TEMPLETE = (
    "/usr/local/airflow/dags/gitdags/dags/ghg/files/"
    "xml_structure_definition/kouzouteigi.xlsx"
)
