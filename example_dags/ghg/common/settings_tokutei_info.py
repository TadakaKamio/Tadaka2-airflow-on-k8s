import os
from decimal import Decimal

path_separator = os.path.sep

# 総ファイル数
TOTAL_FILE_COUNT_TOKUTEI_INFO = 1
# フォルダーパス
FOLDER_PATH_TOKUTEI_INFO = "/dags/gitdags/dags/ghg/files"
# jsonフォルダーパス
FOLDER_PATH_TOKUTEI_INFO_JSON = "/dags/ghg/template/tokutei_info_json_template.json"
TOKUTEI_INFO_FOLDER = (
    f".{path_separator}dags{path_separator}ghg{path_separator}files{path_separator}"
    f"input_files{path_separator}tokutei_info{path_separator}"
)
# 中間ファイル出力用テンプレート
TOKUTEI_INTERMEDIATE_OUTPUT_TEMPLATE = (
    # r".\dags\ghg\template\tokutei_output_template.json"
    f".{path_separator}dags{path_separator}ghg{path_separator}template"
    f"{path_separator}tokutei_output_template.json"
)
# 中間ファイル出力用フォルダ
TOKUTEI_INTERMEDIATE_OUTPUT_FOLDER = (
    # r".\dags\ghg\files\output_files\tokutei_info_intermediate_file"
    f".{path_separator}dags{path_separator}ghg{path_separator}files{path_separator}"
    f"output_files{path_separator}tokutei_info_intermediate_file{path_separator}"
)
# 読み込むシート名のリスト
SHEET_NAMES_TOKUTEI_INFO = [
    "第０表",
    "第１表",
    "第２表",
    "第３表",
    "第４表",
    "第５表",
    "第６表",
    "第７表",
    "第８表",
    "第９表",
    "第１０表",
    "第１１表",
    "第１２表",
]
# 各シートの読み込む列範囲リスト
COL_RANGE_OF_TOKUTEI_LIST = [
    "B:K",
    "B:R",
    "B:APL",
    "B:CO",
    "B:DO",
    "B:F",
    "B:R",
    "B:S",
    "B:BL",
    "B:CA",
    "B:K",
    "B:H",
    "B:BE",
]
# 各シートの読み込む最終列インデックス
LASTCOL_INDEX_OF_TOKUTEI_LIST = [
    9,
    14,
    1084,
    91,
    117,
    4,
    6,
    9,
    62,
    6,
    0,
    0,
    54,
]

ENERGY_INFO = [
    ("A01", "Netsuryo.Genyu"),
    ("A02", "Netsuryo.Condensate"),
    ("A03", "Netsuryo.Kihatsuyu"),
    ("A04", "Netsuryo.Nafusa"),
    ("A05", "Netsuryo.Jet"),
    ("A06", "Netsuryo.Toyu"),
    ("A07", "Netsuryo.Keiyu"),
    ("A08", "Netsuryo.JyuyuA"),
    ("A09", "Netsuryo.JyuyuBC"),
    ("A10", "Netsuryo.SekiyuAsphalt"),
    ("A11", "Netsuryo.SekiyuCoke"),
    ("A12", "Netsuryo.SekiyuGas1"),
    ("A13", "Netsuryo.SekiyuGas2"),
    ("A14", "Netsuryo.TennenGas1"),
    ("A15", "Netsuryo.TennenGas2"),
    ("A16", "Netsuryo.Import_Genryotan"),
    ("A17", "Netsuryo.Coke_Genryotan"),
    ("A18", "Netsuryo.Hukikomi_Genryotan"),
    ("A19", "Netsuryo.Import_Ippantan"),
    ("A20", "Netsuryo.Kokusan_Ippantan"),
    ("A21", "Netsuryo.Import_Muentan"),
    ("A22", "Netsuryo.SekitanCoke"),
    ("A23", "Netsuryo.Coaltar"),
    ("A24", "Netsuryo.COG"),
    ("A25", "Netsuryo.BFG"),
    ("A26", "Netsuryo.Hatuden_BFG"),
    ("A27", "Netsuryo.LDG"),
    ("A28", "Netsuryo.ToshiGas"),
    ("B01", "Hikaseki_Netsuryo.Kokueki"),
    ("B02", "Hikaseki_Netsuryo.Mokuzai"),
    ("B03", "Hikaseki_Netsuryo.Mokushitsu_Haizai"),
    ("B04", "Hikaseki_Netsuryo.Bioethanol"),
    ("B05", "Hikaseki_Netsuryo.Biodiesel"),
    ("B06", "Hikaseki_Netsuryo.Biogas"),
    ("B07", "Hikaseki_Netsuryo.Sonota_Biomass"),
    ("B08", "Hikaseki_Netsuryo.RDF"),
    ("B09", "Hikaseki_Netsuryo.RPF"),
    ("B10", "Hikaseki_Netsuryo.HaiTire"),
    ("B11", "Hikaseki_Netsuryo.HaiPlastic"),
    ("B12", "Hikaseki_Netsuryo.Haiyu"),
    ("B13", "Hikaseki_Netsuryo.HaikibutsuGas"),
    ("B14", "Hikaseki_Netsuryo.Mix_Haizai"),
    ("B15", "Hikaseki_Netsuryo.Suiso"),
    ("B16", "Hikaseki_Netsuryo.Ammonia"),
    ("C0102", "Netsu.BuyNetsu.Jyoki"),
    ("C02", "Netsu.BuyNetsu.Jyoki.UchiHikaseki"),
    ("C0304", "Netsu.BuyNetsu.Jyoki2"),
    ("C04", "Netsu.BuyNetsu.Jyoki2.UchiHikaseki"),
    ("C0506", "Netsu.BuyNetsu.Onsui"),
    ("C06", "Netsu.BuyNetsu.Onsui.UchiHikaseki"),
    ("C0708", "Netsu.BuyNetsu.Reisui"),
    ("C08", "Netsu.BuyNetsu.Reisui.UchiHikaseki"),
    ("C11", "Netsu.SonotaShiyoNetsu.Chinetsu"),
    ("C12", "Netsu.SonotaShiyoNetsu.Onsennetsu"),
    ("C13", "Netsu.SonotaShiyoNetsu.Taiyonetsu"),
    ("C14", "Netsu.SonotaShiyoNetsu.Seppyonetsu"),
    ("D01", "Denki.Baiden.DenkiJigyosya"),
    ("D07", "Denki.PPA_NotWeight.PPA_NotWeight"),
    ("D08", "Denki.PPA_NotWeight.PPA_Weight"),
    ("D09", "Denki.PPA_NotWeight.Jikotakuso"),
    ("D1011", "Denki.PPA_NotWeight.HokaJikotakuso"),
    ("D11", "Denki.PPA_NotWeight.HokaJikotakuso.UchiHikaseki"),
    ("D12", "Denki.PPA_NotWeight.HokaJikotakuso.WeightHikaseki"),
    ("D16", "Denki.Jikahatsuden.Taiyoko_Kwh"),
    ("D17", "Denki.Jikahatsuden.Taiyoko_Kw"),
    ("D18", "Denki.Jikahatsuden.Huryoku_Kwh"),
    ("D19", "Denki.Jikahatsuden.Huryoku_Kw"),
    ("D20", "Denki.Jikahatsuden.Chinetsu_Kwh"),
    ("D21", "Denki.Jikahatsuden.Chinetsu_Kw"),
    ("D22", "Denki.Jikahatsuden.Suiryoku_Kwh"),
    ("D23", "Denki.Jikahatsuden.Suiryoku_Kw"),
    ("D28", "Denki.Jikahatsuden.Jikahatsuden_SonotaNenryo.Kaseki"),
    ("D29", "Denki.Jikahatsuden.Jikahatsuden_SonotaNenryo.Hikaseki"),
    ("D30", "Denki.Jikahatsuden.Jikahatsuden_SonotaNetsu.Kaseki"),
    ("D31", "Denki.Jikahatsuden.Jikahatsuden_SonotaNetsu.Hikaseki"),
]

# 原油換算係数［kL/GJ］
OIL_CONV_FACTOR = Decimal(0.0258)

# 非化石燃料補助係数
NON_FOSSIL_FUEL_COMPENSATION_FACTOR = Decimal(0.8)

# 電気平準化時間帯の電気使用量用係数
ELECTRICITY_LEVELING_TIME_FACTOR = Decimal(0.3)

# 自己託送（非燃料由来の非化石電気）係数
JIKOTAKUSO_COEFFICIENT = Decimal(3.6)

# 熱(その他以外)のエネルギーIDリスト
NETSU_ENERGY_ID_WITHOUT_OTHER = [
    "C01",
    "C02",
    "C03",
    "C04",
    "C05",
    "C06",
    "C07",
    "C08",
    "C11",
    "C12",
    "C13",
    "C14",
]

FLG_0 = "0"
FLG_1 = "1"
