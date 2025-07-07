from enum import Enum

######### エネルギー種類日本名用マップ
energy_name_jp_map = {
'HEAVY_OIL_A' :'A重油',
    'HEAVY_OIL_BC' :'B・C重油',
    'LIGHT_OIL' :'軽油',
    'KEROSENE' :'灯油',
    'GASOLINE':'ガソリン',
    'CITY_GAS' :'都市ガス',
    'LPG' :'LPG',
    'INDUSTRIAL_STEAM' :'産業用蒸気',
    'INDUSTRIAL_EXCEPT_STEAM':'産業用以外の蒸気',
    'WARM_WATER' :'温水',
    'COLD_WATER':'冷水',
    'CRUDE_OIL_CONDENSATE_EXCEPT' :'原油(コンデンセートを除く)',
    'CRUDE_OIL_CONDENSATE' :'原油のうちコンデンセート(NGL)',
    'NAPHTHA' :'ナフサ',
    'PETROLEUM_ASPHALT':'石油アスファルト',
    'PETROLEUM_COKE' :'石油コークス',
    'LNG' :'LNG',
    'PETROLEUM_HYDROCARBON_GAS' :'石油系炭化水素ガス',
    # 'OTHER_FLAMMABLE_NATURAL_GAS':'その他可燃性天然ガス',
    'RAW_CHARCOAL' :'原料炭',
    'ORDINARY_CHARCOAL' :'一般炭',
    'SMOKELESS_COAL' :'無煙炭',
    'COAL_COKE' :'石炭コークス',
    'COAL_TAR':'コールタール',
    'COKE_OVEN_GAS' :'コークス炉ガス',
    'BLAST_FURNACE_GAS' :'高炉ガス',
    'CONVERTER_GAS' :'転炉ガス',
    'JET_FUEL' :'ジェット燃料油',
    'ELECTRIC_POWER':'電気',
    'SUPPLY_INDUSTRIAL_WATER' :'水道および工業用水',
    'PUBLIC_SEWAGE_SYSTEM':'公共下水道',
    'SUPPLY_INDUSTRIAL_WATER' :'輸入原料炭',
    'COKING_COAL' :'コークス用原料炭',
    'PCI_COAL' :'吹込用原料炭',
    'IMPORT_ORDINARY_CHARCOAL' :'輸入一般炭',
    'DOMESTIC_STANDARD_COAL' :'国産一般炭',
    'IMPORT_SMOKELESS_COAL' :'輸入無煙炭',
    'FCC_COKE' :'FCCコーク',
    'CRUDE_OIL_CONDENSATE' :'コンデンセート（NGL）',
    'CRUDE_OIL_CONDENSATE_EXCEPT' :'原油',
    'GASOLINE' :'揮発油',
    'HEAVY_OIL_BC' :'B・C重油',
    'LUBRICATING_OIL' :'潤滑油',
    'LPG' :'液化石油ガス（LPG）',
    'LNG' :'液化天然ガス（LNG）',
    'NATURAL_GAS' :'その他可燃性天然ガス',
    'POWER_GENERATION_BLAST_FURNACE_GAS':'発電用高炉ガス'
}
######### Excelの読み込みの際に値を入り替える用
convert_mapping = {
    '金融機関コード（4桁・半角数字）':'BANK_CODE',
    '支店コード（3桁・半角数字）':'BRANCH_CODE',
    '法人番号（13桁・半角数字）':'CORPORATE_NUMBER',
    '対象年度（4桁・半角数字）':'FISCAL_YEAR',
    '登録回数':'REGISTRATION_SEQ',
    '金融機関名':'BANK_NAME',
    '支店・部署名':'DEPARTMENT_BRANCH_NAME',
    '氏名':'CONTACT_PERSON_NAME_LOCAL_BANK',
    '電話番号（半角数字・ハイフン不要）':'PHONE_NUMBER_LOCAL_BANK',
    'メールアドレス（「@」必須）':'EMAIL_ADDRESS_LOCAL_BANK',
    'ご担当者さま氏名':'CONTACT_PERSON_NAME_CORPORATE',
    'ご担当者さま電話番号（半角数字・ハイフン不要）':'PHONE_NUMBER_CORPORATE',
    'データ利用承諾日（8桁・半角数字　例：20240401）':'UTILIZATION_APPROVAL_DATE_CORPORATE',
    '企業名':'CORPORATE_NAME',
    '本社住所':'OFFICE_ADDRESS',
    '事業所数（半角数字）':'NUMBER_OFFICES',
    '産業分類（大分類・プルダウンから選択）':'INDUSTRY_BROAD_CATEGORIZATION',
    '産業分類（中分類・プルダウンから選択）':'INDUSTRY_INTERMEDIATE_CLASSIFICATION',
    '期初（6桁・半角数字　例：202404）':'START_PERIOD',
    '期末（自動入力）':'END_PERIOD',
    'エリアID':'AREA_ID',
    '事業所名':'AREA_INFORMATION',
    '建物ID':'BUILDING_ID',
    '建物名':'BUILDING_NAME',
    '産業分類（小分類・プルダウンから選択）':'INDUSTRY_CATEGORY_SMALL',
    '供給地点特定番号（22桁・半角数字）':'SUPPLY_POINT_NUMBER',
    '事業所コード（3桁・半角数字）':'EP_STORE_NUMBER',
    'お客さま番号（13桁・半角数字）':'CUSTOMER_NUMBER_EP',
    '建物竣工年（西暦4桁・半角数字）':'BUILDING_COMPLETION_YEAR',
    '建物耐震基準（プルダウンから選択）':'EARTHQUAKE_RESISTANCE_STANDARDS',
    '住所':'ADDRESS',
    '延床面積（半角数字）':'GROSS_FLOOR_AREA',
    '契約先電気事業者登録番号（自動入力）':'REGISTRATION_NUMBER',
    '契約先電気事業者（プルダウンから選択）':'ELECTRIC_POWER_CORPORATE_NAME',
    '契約電力（半角数字）':'CONTRACTED_POWER',
    # '電力量料金（夏季）（半角数字）':'ELECTRICITY_USAGE_FEE_SUMMER',
    # '電力量料金（その他季）（半角数字）':'ELECTRICITY_USAGE_FEE_OTHER_SEASONS',
    # '燃料費調整額（半角数字）':'FUEL_COST_ADJUSTMENT',
    # '再エネ賦課金（半角数字）':'RENEWABLE_ENERGY_SURCHARGE',
    # '従業員数（半角数字）':'EMPLOYEES',
    # '年間稼働日数（半角数字）':'ANNUAL_WORKING_DAYS',
    # '1日の稼働時間（半角数字）':'WORKING_HOURS_ONE_DAY',
    # '給湯用（プルダウンから選択）':'GAS_WATER_HEATING',
    # '生産用（プルダウンから選択）':'GAS_PRODUCTION_USE',
    # '空調用（プルダウンから選択）':'GAS_AIR_CONDITIONING_USE',
    # '発電設備（プルダウンから選択）':'POWER_GENERATION_FACILITIES',
    # '再エネ電力（プルダウンから選択）':'RENEWABLE_ENERGY_POWER',
    # '環境証書（プルダウンから選択）':'ENVIRONMENTAL_CERTIFICATE',
    # '屋根面積（半角数字）':'ROOF_AREA',
    # '駐車場面積（半角数字）':'PARKING_AREA',
    # '空調方式（プルダウンから選択）':'AIR_CONDITIONING_SYSTEM',
    # '空調入れ替え有無（プルダウンから選択）':'NEED_AIR_CONDITIONING_REPLACEMENT',
    # '空調入れ替え年（西暦4桁・半角数字）':'YEAR_AIR_CONDITIONING_REPLACEMENT',
    # '蛍光灯割合':'FLUORESCENT_LIGHTS_PERCENTAGE',
    # 'LED割合':'LED_LIGHTS_PERCENTAGE',
    'A重油': 'HEAVY_OIL_A', 
    'B・C重油': 'HEAVY_OIL_BC', 
    '軽油': 'LIGHT_OIL', 
    '灯油': 'KEROSENE', 
    'ガソリン': 'GASOLINE',
    '都市ガス': 'CITY_GAS', 
    'LPG': 'LPG', 
    '産業用蒸気': 'INDUSTRIAL_STEAM', 
    '産業用以外の蒸気': 'INDUSTRIAL_EXCEPT_STEAM',
    '温水': 'WARM_WATER', 
    '冷水': 'COLD_WATER',
    '原油(コンデンセートを除く)': 'CRUDE_OIL_CONDENSATE_EXCEPT', 
    '原油のうちコンデンセート(NGL)': 'CRUDE_OIL_CONDENSATE', 
    'ナフサ': 'NAPHTHA', 
    '石油アスファルト': 'PETROLEUM_ASPHALT',
    '石油コークス': 'PETROLEUM_COKE', 
    'LNG': 'LNG', 
    '石油系炭化水素ガス': 'PETROLEUM_HYDROCARBON_GAS', 
    # 'その他可燃性天然ガス': 'OTHER_FLAMMABLE_NATURAL_GAS',
    '原料炭': 'RAW_CHARCOAL', 
    '一般炭': 'ORDINARY_CHARCOAL', 
    '無煙炭': 'SMOKELESS_COAL', 
    '石炭コークス': 'COAL_COKE', 
    'コールタール': 'COAL_TAR',
    'コークス炉ガス': 'COKE_OVEN_GAS', 
    '高炉ガス': 'BLAST_FURNACE_GAS', 
    '転炉ガス': 'CONVERTER_GAS', 
    'ジェット燃料油': 'JET_FUEL', 
    '電気': 'ELECTRIC_POWER',
    '水道および工業用水': 'SUPPLY_INDUSTRIAL_WATER', 
    '公共下水道': 'PUBLIC_SEWAGE_SYSTEM',
    '輸入原料炭': 'SUPPLY_INDUSTRIAL_WATER', 
    'コークス用原料炭': 'COKING_COAL', 
    '吹込用原料炭': 'PCI_COAL', 
    '輸入一般炭': 'IMPORT_ORDINARY_CHARCOAL', 
    '国産一般炭': 'DOMESTIC_STANDARD_COAL', 
    '輸入無煙炭': 'IMPORT_SMOKELESS_COAL', 
    'FCCコーク': 'FCC_COKE', 
    'コンデンセート（NGL）': 'CRUDE_OIL_CONDENSATE', 
    '原油': 'CRUDE_OIL_CONDENSATE_EXCEPT', 
    '揮発油': 'GASOLINE', 
    'B・C重油': 'HEAVY_OIL_BC', 
    '潤滑油': 'LUBRICATING_OIL', 
    '液化石油ガス（LPG）': 'LPG', 
    '液化天然ガス（LNG）': 'LNG', 
    'その他可燃性天然ガス': 'NATURAL_GAS', 
    '発電用高炉ガス': 'POWER_GENERATION_BLAST_FURNACE_GAS'
    # '✓': '1',
    # '-': '0',
    # '導入済み':'2',
    # '導入なし(意向なし)':'0',
    # '導入なし(意向あり)':'1',
    # '使用済み':'2',
    # '使用なし(意向なし)':'0',
    # '使用なし(意向あり)':'1',
    # 'セントラル空調':'0',
    # '個別':'1',
    # '有':'1',
    # '無':'0'
}

enery_code_mapping = {
    'A重油': '0100120000', 
    'B・C重油': '0100130000', 
    '軽油': '0100110000', 
    '灯油': '0100100000', 
    '都市ガス': '0100230000', 
    '液化石油ガス（LPG）': '0100190000', 
    '産業用蒸気': '0300010000', 
    '産業用以外の蒸気': '0300020000',
    '温水': '0300030000', 
    '冷水': '0300040000',
    '原油(コンデンセートを除く)': '0100150000', 
    '原油のうちコンデンセート(NGL)': '0100140000', 
    'ナフサ': '0100180000', 
    '石油アスファルト': '0100160000',
    '石油コークス': '0100080000', 
    '液化天然ガス（LNG）': '0100210000', 
    '石油系炭化水素ガス': '0100200000', 
    'その他可燃性天然ガス': '0100220000',
    '原料炭': '0100020000', 
    '一般炭': '0100010000', 
    '無煙炭': '0100030000', 
    '石炭コークス': '0100070000', 
    'コールタール': '0100170000',
    'コークス炉ガス': '0100240000', 
    '高炉ガス': '0100250000', 
    '転炉ガス': '0100260000', 
    'ジェット燃料油': '0100300000', 
    '輸入原料炭': '0100020000', 
    'コークス用原料炭': '0100310000', 
    '吹込用原料炭': '0100320000', 
    '輸入一般炭': '0100010000', 
    '国産一般炭': '0100330000', 
    '輸入無煙炭': '0100030000', 
    'FCCコーク': '0100350000', 
    'コンデンセート（NGL）': '0100140000', 
    '原油': '0100150000', 
    '揮発油': '0100090000', 
    '潤滑油': '0100360000', 
    # 'その他可燃性天然ガス': '2200070000', 
    '発電用高炉ガス': '0100340000',
    '電気': '0200010011'
}

# 入力情報
caitbl_columns = (
    "BANK_CODE",
    "BRANCH_CODE",
    "CORPORATE_NUMBER",
    "FISCAL_YEAR",
    "REGISTRATION_SEQ",
    "BANK_NAME",
    "DEPARTMENT_BRANCH_NAME",
    "CONTACT_PERSON_NAME_LOCAL_BANK",
    "CONTACT_PERSON_NAME_CORPORATE",
    "PHONE_NUMBER_CORPORATE",
    "UTILIZATION_APPROVAL_DATE_CORPORATE",
    "CORPORATE_NAME",
    "OFFICE_ADDRESS",
    "NUMBER_OFFICES",
    "INDUSTRY_BROAD_CATEGORIZATION",
    "INDUSTRY_INTERMEDIATE_CLASSIFICATION",
    "START_PERIOD",
    "END_PERIOD",
    "AREA_ID",
    "AREA_INFORMATION",
    "BUILDING_ID",
    "BUILDING_NAME",
    "INDUSTRY_CATEGORY_SMALL",
    "SUPPLY_POINT_NUMBER",
    "EP_STORE_NUMBER",
    "CUSTOMER_NUMBER_EP",
    "ADDRESS",
    "GROSS_FLOOR_AREA",
    "REGISTRATION_NUMBER",
    "ELECTRIC_POWER_CORPORATE_NAME",
    "CONTRACTED_POWER",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG",
)

# 入力情報
caitbl_hive_columns = (
    "BRANCH_CODE",
    "REGISTRATION_SEQ",
    "BANK_NAME",
    "DEPARTMENT_BRANCH_NAME",
    "CONTACT_PERSON_NAME_LOCAL_BANK",
    "CONTACT_PERSON_NAME_CORPORATE",
    "PHONE_NUMBER_CORPORATE",
    "UTILIZATION_APPROVAL_DATE_CORPORATE",
    "CORPORATE_NAME",
    "OFFICE_ADDRESS",
    "NUMBER_OFFICES",
    "INDUSTRY_BROAD_CATEGORIZATION",
    "INDUSTRY_INTERMEDIATE_CLASSIFICATION",
    "START_PERIOD",
    "END_PERIOD",
    "AREA_ID",
    "AREA_INFORMATION",
    "BUILDING_NAME",
    "INDUSTRY_CATEGORY_SMALL",
    "SUPPLY_POINT_NUMBER",
    "EP_STORE_NUMBER",
    "CUSTOMER_NUMBER_EP",
    "ADDRESS",
    "GROSS_FLOOR_AREA",
    "REGISTRATION_NUMBER",
    "ELECTRIC_POWER_CORPORATE_NAME",
    "CONTRACTED_POWER",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG",
)

# レポート格納情報
rsitbl_columns = (
    "BANK_CODE",
    "BANK_NAME",
    "BRANCH_CODE",
    "DEPARTMENT_BRANCH_NAME",
    "CORPORATE_NUMBER",
    "CORPORATE_NAME",
    "USER_CD",
    "CONTACT_PERSON_NAME_LOCAL_BANK",
    "BUILDING_ID",
    "FISCAL_YEAR",
    "REPORT_TYPE",
    "REGISTRATION_SEQ",
    "FILE_ID",
    "REPORT_LOCATION",
    "STATUS",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG",
)

# 簡易診断設定シート入力項目
roadmap_setting = {
    "基準年":"BASE_YEAR",
    "熱源照明更新周期":"HEAT_SOURCE_LIGHTING_RENEWAL_CYCLE",
    "その他対策周期":"OTHER_MEASURES_CYCLE",
    "対策考慮区分":"CONSIDERATION_OF_MEASURES",
    "省エネ努力目標":"ENERGY_SAVING_TARGET",
    "電力CO2排出係数パターン":"ELECTRICITY_CO2_EMISSIONS_COEFFICIENT_PATTERN",
    "証書購入基準年～2030年":"BASE_YEAR_FOR_CERTIFICATE_PURCHASE_TO_2030",
    "証書購入2030～2050年":"CERTIFICATE_PURCHASE_FROM_2030_TO_2050",
    "太陽光導入年":"SOLAR_INTRODUCTION_YEAR",
    "竣工年記載無の代替":"ALTERNATIVE_FOR_NON-CONSTRUCTION_YEAR_INDICATION",
    "中央個別判断":"CENTRAL_INDIVIDUAL_JUDGMENT",
    "太陽光発電設置可能比率":"SOLAR_POWER_INSTALLATION_POSSIBLE_RATE",
    "新耐震区分け年数":"NEW_SEISMIC_ZONING_YEARS",
    "太陽光発電":"SOLAR_POWER_GENERATION",
    "太陽光発電発電量":"SOLAR_POWER_GENERATION_AMOUNT",
    "建物用途区分":"BUILDING_USAGE"
}
corporate_column = [
    "BANK_CODE",
    "BANK_NAME",
    "BRANCH_CODE",
    "CORPORATE_NUMBER",
    "DEPARTMENT_BRANCH_NAME",
    "CONTACT_PERSON_NAME_LOCAL_BANK",
    "PHONE_NUMBER_LOCAL_BANK",
    "EMAIL_ADDRESS_LOCAL_BANK",
    "CONTACT_PERSON_NAME_CORPORATE",
    "PHONE_NUMBER_CORPORATE",
    "UTILIZATION_APPROVAL_DATE_CORPORATE",
    "CORPORATE_NAME",
    "OFFICE_ADDRESS",
    "NUMBER_OFFICES",
    "INDUSTRY_BROAD_CATEGORIZATION",
    "INDUSTRY_BROAD_CATEGORIZATION_NAME",
    "INDUSTRY_INTERMEDIATE_CLASSIFICATION",
    "INDUSTRY_INTERMEDIATE_CLASSIFICATION_NAME",
    "FISCAL_YEAR",
    "START_PERIOD",
    "END_PERIOD",
    "AREA_ID",
    "USER_CD"
]

building_column = [
    "AREA_INFORMATION",
    "BUILDING_ID",
    "BUILDING_NAME",
    "INDUSTRY_CATEGORY_SMALL_CODE",
    "INDUSTRY_CATEGORY_SMALL",
    "SUPPLY_POINT_NUMBER",
    "EP_STORE_NUMBER",
    "CUSTOMER_NUMBER_EP",
    "BUILDING_COMPLETION_YEAR",
    "EARTHQUAKE_RESISTANCE_STANDARDS",
    "ADDRESS",
    "GROSS_FLOOR_AREA",
    "REGISTRATION_NUMBER",
    "ELECTRIC_POWER_CORPORATE_NAME",
    "CONTRACTED_POWER"
]
# エネルギー情報のコラム作成
energy_column = [
    'AREA_INFORMATION',
    'BUILDING_ID',
    'BUILDING_NAME',
    'ENERGY_CODE',
    'CATEGORY',
    'ENERGY_NAME',
    'ENERGY_NAME_JP',
    'YEAR',
    'MONTH',
    'FISCAL_YEAR',
    'ENERGY_QUANTITY'
]

# 必須チェック用項目格納用配列
CORPORATE_REQUIRED_COLUMNS = [
    "BANK_CODE",
    "BANK_NAME",
    "BRANCH_CODE",
    "CORPORATE_NUMBER",
    "DEPARTMENT_BRANCH_NAME",
    "CONTACT_PERSON_NAME_LOCAL_BANK",
    # "PHONE_NUMBER_LOCAL_BANK",
    "CONTACT_PERSON_NAME_CORPORATE",
    "PHONE_NUMBER_CORPORATE",
    "UTILIZATION_APPROVAL_DATE_CORPORATE",
    "CORPORATE_NAME",
    "OFFICE_ADDRESS",
    "NUMBER_OFFICES",
    "FISCAL_YEAR",
    "START_PERIOD"
]

BUILDING_REQUIRED_COLUMNS = [
    "AREA_INFORMATION"
]

NEITHER_REQUIRED_COLUMNS = [
    "CORPORATE_NUMBER",
    "EP_STORE_NUMBER",
    "CUSTOMER_NUMBER_EP",
    "AREA_INFORMATION"
]

# マスタテーブル
class MasterTable(Enum):
    """
    マスタテーブル名列挙
        業種マスタ
        排出係数マスタ
        電力換算係数マスタ
        建物群マスタ
        区分マスタ
        活動項目小分類マスタ
        日本標準産業分類マスタ
        電力会社の換算係数マスタ
    """        
    JICMST = "M_JP_ST_INDUSTRY_CLASSIFICATION"
    CCMST = "ACTIVITY_MINOR_CATEGORY_MST"
    ECMST = "M_ELECTRICITY_CONVERSION_FACTOR"
    AIMST = "M_AREA_INFO"
    KBNMST = "KUBUN_MST"
    ECDMST = "ENERGY_CONSUMPTION_DESTINATION_MST"
    ECEMST = "ELECTRICITY_CO2_EMISSION_MST"
    BECRMST = "BASE_ENERGY_CONSUMPTION_RATE_MST"
    CMST = "COUNTERMEASURE_MST"	
    CALMST = "M_CALCULATION_LOGIC"
    AMCMST = "ACTIVITY_MINOR_CATEGORY_MST"
    MJSIC = "M_JP_ST_INDUSTRY_CLASSIFICATION"
    MECF = "M_ELECTRICITY_CONVERSION_FACTOR"
    MUMST = "M_USER"


# 業務テーブル
class BusinessTable(Enum):
    """
    業務用テーブル名列挙
        エネルギー集計情報
        エネルギー集計月別情報
        年度別法人エネルギー集計情報
        月別法人エネルギー集計情報
        入力情報
        ファイルステータス
    """        
    EATBL = "T_ANNUAL_BUILDING_ENERGY_AGGREGATION"
    EAMTBL = "T_MONTHLY_BUILDING_ENERGY_AGGREGATION"
    ACEATBL = "T_ANNUAL_CORPORATE_ENERGY_AGGREGATION"
    MCEATBL = "T_MONTHLY_CORPORATE_ENERGY_AGGREGATION"
    CAITBL = "T_CN_APPLICATION_INFO"
    CBBITBL = "M_CUSTOMER_BANK_BASIC_INFO"
    BBITBL = "M_BANK_BRANCH_INFO"
    BSITBL = "M_BANK_STAFF_INFO"
    CBITBL = "M_CORPORATE_BASIC_INFO"
    RSITBL = "T_REPORT_STORAGE_INFO"

class ExcelExtension(Enum):
    """Excelファイル拡張子列挙"""
    XLSX = ".xlsx"
    XLS = ".xls"
    XLSM = ".xlsm"
    CSV = ".csv"

class FileProcessStatus(Enum):
    """ファイル処理ステータス"""
    ERROR = "0"
    COMPELETED = "1"
    PENDING = "2"

class StringOfExcelFile(Enum):
    """Excelファイル内容特定文字列"""
    OFFICE = "事業所"
    INPUT_SHEET = "記入シート"
    ENERGY_INFO = "エネルギー使用量（半角数字）"
    INPUT_SPECS= "入力（TEPCO用）諸元"
    SETTING= "設定"

class NumberingStartValue(Enum):
    """採番用スタート番号用"""
    THREE_NUMBER = "001"
    SIX_NUMBER = "000001"

class SpecialChars(Enum):
    """特殊文字列用列挙"""
    COLON = ":"
    DOT = "."
    COMMA = ","
    UNDERSCORE = "_"
    SPACE = " "
    HATENA = "?"
    BLANK = ""
    HYPHEN = "-"
    LINUX_PATH_DELIMITER = "/"
    WINDOWS_PATH_DELIMITER = "\\"

class RunMode(Enum):
    """実行モード"""
    DEV = "dev"
    STG = "staging"
    PROD = "product"
    S2_PROD = "s2_product"

class EncodingMethod(Enum):
    """エンコーディング方法"""
    UTF8 = "utf-8"
    SJIS = "sjis"
    UTF8BOM = "utf-8-sig"

class TableauReport(Enum):
    """Tableauに表示するレポート"""
    KARTE = "企業カルテ"
    ABATEMENT = "アベイトメントカーブ"
    ROADMAP = "簡易診断ツール"
    COMMON = "企業カルテ_ロードマップ"

class InputFileIndentify(Enum):
    """Tableauに表示するレポート"""
    KARTE = "行員向け入力シート"
    ABATEMENT = "CNアベイトメントカーブ"
    ROADMAP = "CNロードマップ"

class HqlConditonOperators(Enum):
    """hql条件文操作子列挙"""
    EQUAL = '='
    NOT_EQUAL = '<>'
    GREATER_THAN = '>'
    LESS_THAN = '<'
    GREATER_THAN_OR_EQUAL = '>='
    LESS_THAN_OR_EQUAL = '<='
    LIKE = 'LIKE'
    NOT_LIKE = 'NOT_LIKE'
    IN = 'IN'
    NOT_IN = 'NOT IN'
    IS_NULL = 'IS NULL'
    IS_NOT_NULL = 'IS NOT NULL'

class EEGSMasterSheetName(Enum):
    """EEGSマスタシート名"""
    AMCMST_SHEET_NAME = "活動項目小分類（事業者）"
    MJSIC_SHEET_NAME = "産業分類"
    MECF_SHEET_NAME = "電気事業者メニュー別"
    MUMST_SHEET_NAME = "ユーザ登録・変更・削除申請表"

class UserApplicationKbn(Enum):
    ADD = "追加"
    UPDATE = "変更"
    DELETE = "削除"

# 業種マスタカラム情報
JICMST_COLUMNS = (
    "CLASSFICATION_ID",
    "LARGE_CATEGORY_CODE",
    "MEDIUM_CATEGORY_CODE", 
    "SMALL_CATEGORY_CODE",
    "DETAIL_CATEGORY_CODE",
    "INDUSTRY_NAME",
    "LARGE_CATEGORY_NAME",
    "MEDIUM_CATEGORY_NAME",
    "START_DATE",
    "END_DATE",
    "CREATION_DATETIME",
    "CREATOR",
    "update_datetime",
    "updateor",
    "delete_flg"
)

# 算定ロジックマスタカラム情報
CALMST_COLUMNS = (
    "LOGIC_ID",
    "NAME",
    "FORMULA",
    "VARIABLES",
    "DESCRIPTION"
)

# 換算係数マスタカラム情報            
CCMST_COLUMNS = (
    "REPORT_YEAR",
    "MAJOR_CATEGORY_ID",
    "MIDDLE_CATEGORY_ID",
    "MINOR_CATEGORY_ID",
    "CONVERSION_COEF",
    "ENERGY_CO2_EMISSION_COEF",
    "UNIT"
)

# 活動項目小分類マスタカラム情報            
AMCMST_COLUMNS = (
    "REPORT_YEAR",
    "MAJOR_CATEGORY_ID",
    "MIDDLE_CATEGORY_ID",
    "MINOR_CATEGORY_ID",
    "MINOR_CATEGORY_NM",
    "UNIT",
    "CONVERSION_COEF",
    "NON_FOSSIL_CONV_COEF",
    "NON_FOSSIL_WEIGHT_COEF",
    "ELECTRIC_DEMAND_OPT_COEF",
    "ENERGY_CO2_EMISSION_COEF",
    "NON_ENERGY_CO2_EMISSION_COEF",
    "CH4_EMISSION_COEF",
    "N2O_EMISSION_COEF",
    "HFC_EMISSION_COEF",
    "PFC_EMISSION_COEF",
    "SF6_EMISSION_COEF",
    "NF3_EMISSION_COEF",
    "CONVERSION_VALUE1",
    "CONVERSION_VALUE2",
    "NON_ENERGY_KBN",
    "GLOBAL_WARMING_LAW_FLAG",
    "ENERGY_EFFICIENCY_LAW_FLAG",
    "ACTIVITY_ITEM_SCREEN_FLAG",
    "SUPPORT_SCREEN_KBN",
    "UNIT_INPUT_ENABLED_FLAG",
    "CONVERSION_COEF_INPUT_FLAG",
    "USAGE_INPUT_ENABLED_FLAG",
    "BY_PRODUCT_INPUT_ENABLED_FLAG",
    "UNUSED_HEAT_INPUT_ENABLED_FLAG",
    "ACTIVITY_MAX_LIMIT",
    "ACTIVITY_MIN_LIMIT",
    "ACTIVITY_ITEM_COMMENT",
    "HEAT_SUPPORT_SCREEN_FLAG",
    "ELECTRICITY_SUPPORT_SCREEN_FLAG",
    "NON_FOSSIL_KBN",
    "SELF_GENERATION_SCREEN_FLAG",
    "DISPLAY_ORDER",
    "START_DATE",
    "END_DATE",
    "CREATED_AT",
    "CREATED_BY",
    "UPDATED_AT",
    "UPDATED_BY",
    "DELETE_FLAG",
)

# 日本標準産業分類マスタカラム情報            
MJSIC_COLUMNS = (
    "DIVISION_CODE",
    "MAJOR_GROUP_CODE",
    "GROUP_CODE",
    "INDUSTRY_CODE",
    "DIVISION_NAME",
    "MAJOR_GROUP_NAME",
    "GROUP_NAME",
    "INDUSTRY_NAME",
    "START_DATE",
    "END_DATE",
    "CREATED_AT",
    "CREATED_BY",
    "UPDATED_AT",
    "UPDATED_BY",
    "DELETE_FLAG",
)

# 電力会社の換算係数マスタカラム情報
MECF_COLUMNS = (
    "REGISTRATION_NUMBER",
    "ELECTRICITY_SUPPLIER_NAME",
    "FISCAL_YEAR",
    "ADJUSTED_EMISSION_FACTOR",
    "START_DATE",
    "END_DATE",
    "CREATION_DATETIME",
    "CREATE_BY",
    "UPDATE_DATETIME",
    "UPDATE_BY",
    "DELETE_FLG",
)

# ユーザ
MUMST_COLUMNS = (
    "USER_MAIL",
    "USER_NAME",
    "COMPANY_NAME",
    "DEPARTMENT_ID",
    "DEPARTMENT_NAME",
    "USER_PASSWORD",
    "USER_ROLE",
    "START_DATE",
    "END_DATE",
    "CREATION_DATETIME",
    "CREATE_BY",
    "UPDATE_DATETIME",
    "UPDATE_BY",
    "DELETE_FLG",
)

# 排出係数マスタカラム情報
ECMST_COLUMNS = (
    "REGISTRATION_NUMBER",
    "ELECTRICITY_SUPPLIER_NAME",
    "FISCAL_YEAR",
    "ADJUSTED_EMISSION_FACTOR"
)

# エリアマスタカラム情報
AIMST_COLUMNS = (
    "AREA_ID",
    "PARENT_AREA_ID",
    "CORPORATE_NUMBER",
    "BUILDING_ID",
    "AREA_NAME",
    "CORPORATE_NAME",
    "BUILDING_NAME",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
)

# エリアマスタカラム情報
FPSTBL_COLUMNS = (
    "FILE_NAME",
    "FILE_PATH",
    "FILE_TYPE",
    "STATUS",
    "CREATION_DATETIME",
    "CREATOR"
)

# エリアマスタカラム情報
KBNMST_COLUMNS = (
    "CATEGORY_CD",
    "CATEGORY_NAME",
    "KBN_CD",
    "KBN_NAME",
    "KBN_SORT",
    "CREATION_DATETIME",
    "CREATOR"
)

ECDMST_COLUMNS = (
    "BUILDING_USAGE",
    "FISCAL_YEAR",
    "ENERGY_CATEGORY_DIV",
    "ENERGY_CATEGORY_NAME",
    "ENERGY_SUB_DIV",
    "ENERGY_SUB_NAME",
    "VALUE",
    "CREATION_DATETIME",
    "CREATOR"
)

ECEMST_COLUMNS =(
    "FISCAL_YEAR",
    "FIXED_PATTERN",
    "ELECTRIC_POWER_2030_PATTERN",
    "CUSTOM_SETTING_PATTERN",
    "NATIONAL_AVERAGE_PATTERN",
    "CREATION_DATETIME",
    "CREATOR"
)

BECRMST_COLUMNS =(			
    "FISCAL_YEAR",
    "MENU_NUM",
    "MENU_ITEM",
    "ENERGY_CONSUMPTION_CATEGORY",
    "CORRECTION_CATEGORY_USAGE",
    "CORRECTION_CATEGORY_RANGE",
    "BASE_ENERGY_CONSUMPTION_RATE",
    "CREATION_DATETIME",
    "CREATOR"
)

CMST_COLUMNS = (
    "FISCAL_YEAR",
    "MENU_NUM",
    "MENU_ITEM",
    "COUNTERMEASURE_MENU",
    "COUNTERMEASURE_FLAG",
    "CREATION_DATETIME",
    "CREATOR"
)

# CN対策実施申込パーティション情報
PARTITION_COLUMNS_CAITBL = (
    "BANK_CODE",
    "CORPORATE_NUMBER",
    "BUILDING_ID",
    "FISCAL_YEAR"
    # "PART_REGISTRATION_NUMBER",
)

PARTITION_COMPANY_COLUMNS = (
    "BANK_CODE",
    "CORPORATE_NUMBER",
    "FISCAL_YEAR"
)

# パーティション情報
SELECT_COLUMNS = (
    "REGISTRATION_SEQ"
)

#計算用DATA
MONTH_DATA =[
    "BANK_CODE",                            #金融機関コード
    "CORPORATE_NUMBER",                     #法人番号
    "BUILDING_NAME",                          #事業所名
    "ENERGY_NAME",                          #エネルギー名称
    "YEAR",                                 #年
    "MONTH",                                #月
    "ENERGY_CONSUMPTION"                    #エネルギー使用量
]

CONSIDERATION_OF_MEASURES_dict ={
    'する' :'0',    
    'しない':'1'
}

officeMonthly_columns = [
    "BANK_CODE",
    "CORPORATE_NUMBER",
    "BUILDING_ID",
    "FISCAL_YEAR",
    "MONTH",
    "ENERGY_CODE",
    "ENERGY_SCOPE",
    "REGISTRATION_SEQ",
    "AREA_ID",
    "AREA_INFORMATION",
    "BUILDING_NAME",
    "YEAR",
    "ENERGY_NAME",
    "ENERGY_CATEGORY",
    "ENERGY_UNITS",
    "ENERGY_CONSUMPTION",
    "CO2_EMISSIONS",
    "CO2_EMISSIONS_AREA_UNIT",
    "CALORIFIC_ENERGY_CONSUMPTION",
    "CALORIFIC_ENERGY_CONSUMPTION_UNIT",
    "CRUDE_OIL_ENERGY_CONSUMPTION",
    "CRUDE_OIL_ENERGY_CONSUMPTION_UNIT",
    "ELECTRIC_CONSUMPTION_UNIT",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

officeYearly_columns = [
    "BANK_CODE",
    "CORPORATE_NUMBER",
    "BUILDING_ID",
    "FISCAL_YEAR",
    "ENERGY_CODE",
    "REGISTRATION_SEQ",
    "AREA_ID",
    "AREA_INFORMATION",
    "BUILDING_NAME",
    "ENERGY_NAME",
    "ENERGY_CATEGORY",
    "ENERGY_UNITS",
    "ENERGY_CONSUMPTION",
    "CO2_EMISSIONS",
    "CO2_EMISSIONS_AREA_UNIT",
    "CO2_EMISSIONS_AREA_RANKING",
    "CALORIFIC_ENERGY_CONSUMPTION",
    "CALORIFIC_ENERGY_CONSUMPTION_UNIT",
    "CRUDE_OIL_ENERGY_CONSUMPTION",
    "CRUDE_OIL_ENERGY_CONSUMPTION_UNIT",
    "ELECTRIC_CONSUMPTION_UNIT",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

corporateMonthly_columns = [
    "BANK_CODE",
    "CORPORATE_NUMBER",
    "FISCAL_YEAR",
    "MONTH",
    "ENERGY_CODE",
    "REGISTRATION_SEQ",
    "YEAR",
    "ENERGY_NAME",
    "ENERGY_CATEGORY",
    "ENERGY_UNITS",
    "ENERGY_CONSUMPTION",
    "CO2_EMISSIONS",
    "CO2_EMISSIONS_RANKING",
    "CO2_EMISSIONS_AREA_UNIT",
    "CALORIFIC_ENERGY_CONSUMPTION",
    "CALORIFIC_ENERGY_CONSUMPTION_UNIT",
    "CRUDE_OIL_ENERGY_CONSUMPTION",
    "CRUDE_OIL_ENERGY_CONSUMPTION_UNIT",
    "ELECTRIC_CONSUMPTION_UNIT",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

corporateYearly_columns = [
    "BANK_CODE",
    "CORPORATE_NUMBER",
    "FISCAL_YEAR",
    "ENERGY_CODE",
    "REGISTRATION_SEQ",
    "ENERGY_NAME",
    "ENERGY_CATEGORY",
    "ENERGY_UNITS",
    "ENERGY_CONSUMPTION",
    "CO2_EMISSIONS",
    "CO2_EMISSIONS_RANKING",
    "CO2_EMISSIONS_AREA_UNIT",
    "CALORIFIC_ENERGY_CONSUMPTION",
    "CALORIFIC_ENERGY_CONSUMPTION_UNIT",
    "CRUDE_OIL_ENERGY_CONSUMPTION",
    "CRUDE_OIL_ENERGY_CONSUMPTION_UNIT",
    "ELECTRIC_CONSUMPTION_UNIT",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

#####以下はSTEP2リソース#####
#契約先金融機関基本情報マスタ
mCustomerBankBasicInfo_colums = [
    "BANK_CODE",
    "START_DATE",
    "END_DATE",
    "BANK_NAME",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

#支店マスタ
mBankBranchInfo_colums = [
    "BANK_CODE",
    "BRANCH_CODE",
    "START_DATE",
    "END_DATE",
    "BANK_NAME",
    "DEPARTMENT_BRANCH_NAME",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

#金融機関担当者マスタ
mBankStaffInfo_colums = [
    "USER_CD",
    "BANK_CODE",
    "BRANCH_CODE",
    "CONTACT_PERSON_NAME_LOCAL_BANK",
    "START_DATE",
    "END_DATE",
    "BANK_NAME",
    "DEPARTMENT_BRANCH_NAME",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

#企業基本情報マスタ
mCorporateBasicInfo_colums = [
    "CORPORATE_NUMBER",
    "START_DATE",
    "END_DATE",
    "CORPORATE_NAME",
    "OFFICE_ADDRESS",
    "NUMBER_OFFICES",
    "INDUSTRY_BROAD_CATEGORIZATION_NAME",
    "INDUSTRY_INTERMEDIATE_CLASSIFICATION_NAME",
    "INDUSTRY_BROAD_CATEGORIZATION",
    "INDUSTRY_INTERMEDIATE_CLASSIFICATION",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

#レポート格納情報
reportStorageInfo_colums = [
    "BANK_CODE",
    "BRANCH_CODE",
    "CORPORATE_NUMBER",
    "BUILDING_ID",
    "FISCAL_YEAR",
    "REPORT_TYPE",
    "REGISTRATION_SEQ",
    "FILE_ID",
    "REPORT_LOCATION",
    "STATUS",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

officeMonthly_hive_columns = [
    "MONTH",
    "ENERGY_CODE",
    "REGISTRATION_SEQ",
    "AREA_ID",
    "AREA_INFORMATION",
    "BUILDING_NAME",
    "YEAR",
    "ENERGY_NAME",
    "ENERGY_CATEGORY",
    "ENERGY_UNITS",
    "ENERGY_CONSUMPTION",
    "CO2_EMISSIONS",
    "CO2_EMISSIONS_AREA_UNIT",
    "CALORIFIC_ENERGY_CONSUMPTION",
    "CALORIFIC_ENERGY_CONSUMPTION_UNIT",
    "CRUDE_OIL_ENERGY_CONSUMPTION",
    "CRUDE_OIL_ENERGY_CONSUMPTION_UNIT",
    "ELECTRIC_CONSUMPTION_UNIT",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

officeYearly_hive_columns = [
    "ENERGY_CODE",
    "REGISTRATION_SEQ",
    "AREA_ID",
    "AREA_INFORMATION",
    "BUILDING_NAME",
    "ENERGY_NAME",
    "ENERGY_CATEGORY",
    "ENERGY_UNITS",
    "ENERGY_CONSUMPTION",
    "CO2_EMISSIONS",
    "CO2_EMISSIONS_AREA_UNIT",
    "CALORIFIC_ENERGY_CONSUMPTION",
    "CALORIFIC_ENERGY_CONSUMPTION_UNIT",
    "CRUDE_OIL_ENERGY_CONSUMPTION",
    "CRUDE_OIL_ENERGY_CONSUMPTION_UNIT",
    "ELECTRIC_CONSUMPTION_UNIT",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

corporateMonthly_hive_columns = [
    "MONTH",
    "ENERGY_CODE",
    "REGISTRATION_SEQ",
    "YEAR",
    "ENERGY_NAME",
    "ENERGY_CATEGORY",
    "ENERGY_UNITS",
    "ENERGY_CONSUMPTION",
    "CO2_EMISSIONS",
    "CO2_EMISSIONS_RANKING",
    "CO2_EMISSIONS_AREA_UNIT",
    "CALORIFIC_ENERGY_CONSUMPTION",
    "CALORIFIC_ENERGY_CONSUMPTION_UNIT",
    "CRUDE_OIL_ENERGY_CONSUMPTION",
    "CRUDE_OIL_ENERGY_CONSUMPTION_UNIT",
    "ELECTRIC_CONSUMPTION_UNIT",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]

corporateYearly_hive_columns = [
    "ENERGY_CODE",
    "REGISTRATION_SEQ",
    "ENERGY_NAME",
    "ENERGY_CATEGORY",
    "ENERGY_UNITS",
    "ENERGY_CONSUMPTION",
    "CO2_EMISSIONS",
    "CO2_EMISSIONS_RANKING",
    "CO2_EMISSIONS_AREA_UNIT",
    "CALORIFIC_ENERGY_CONSUMPTION",
    "CALORIFIC_ENERGY_CONSUMPTION_UNIT",
    "CRUDE_OIL_ENERGY_CONSUMPTION",
    "CRUDE_OIL_ENERGY_CONSUMPTION_UNIT",
    "ELECTRIC_CONSUMPTION_UNIT",
    "CREATION_DATETIME",
    "CREATOR",
    "UPDATE_DATETIME",
    "UPDATEOR",
    "DELETE_FLG"
]