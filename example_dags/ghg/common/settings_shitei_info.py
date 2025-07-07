# 総ファイル数
TOTAL_FILE_COUNT_SHITEI_INFO = 0
# フォルダーパス
FOLDER_PATH_SHITEI_INFO = (
    "/usr/local/airflow/dags/gitdags/dags/ghg/files/input_files/shitei_info"
)

# 読み込むシート名のリスト
SHEET_NAMES_SHITEI_INFO = [
    "STEP２（第１、2表）",
    "STEP２（第３表～）",
    "第0表",
    "第1表",
    "第2表",
    "第3表",
    "第4表",
    "第5表",
    "第6表",
    "第7表",
    "第8表",
    "第9表",
    "第10表",
]
# 各シートの読み込む列範囲リスト
COL_RANGE_OF_SHITEI_LIST = [
    "B:D",
    "B:AC",
    "B:AEX",
    "B:L",
    "B:J",
    "B:N",
    "B:BH",
    "B:F",
    "B:JO",
    "B:D",
    "B:R",
]
# 各シートの読み込む最終列インデックス
LASTCOL_INDEX_OF_SHITEI_LIST = [2, 24, 820, 1, 8, 12, 58, 4, 273, 2, 16]

# フォルダーパス
FOLDER_PATH_SHITEI_INFO_XML = (
    "/usr/local/airflow/dags/gitdags/dags/ghg/files/output_files/shitei_info_xml"
)

# jsonフォルダーパス（このパスは仮想のものです。テストをローカルで行う必要がある場合は、担当者は自分のローカルパスに設定してください。）
FOLDER_PATH_SHITEI_INFO_JSON = (
    "/usr/local/airflow/dags/gitdags/dags/ghg/template/shitei_info_json_template.json"
)
