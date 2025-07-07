from dataclasses import dataclass
import datetime
 
@dataclass
#建物年別
class BuildingYearlyEntity:
    CORPORATE_NUMBER:str                      #法人番号
    BANK_CODE:str                             #金融機関コード 
    AREA_ID:str            
    AREA_INFORMATION:str                      #事業所名
    REGISTRATION_SEQ:int                      #登録回数           
    BUILDING_ID:str            
    BUILDING_NAME:str                         #事業所名
    ENERGY_CODE:str                           #エネルギーコード
    ENERGY_NAME:str                           #エネルギー名
    ENERGY_CATEGORY:str                       #カテゴリ
    FISCAL_YEAR:str                           #年度
    ENERGY_UNITS:str                          #エネルギー単位
    ENERGY_CONSUMPTION:str                    #年度エネルギー使用量
    CALORIFIC_ENERGY_CONSUMPTION:str          #熱量換算エネルギー使用量
    CALORIFIC_ENERGY_CONSUMPTION_UNIT:str
    CO2_EMISSIONS_AREA_UNIT:str               #CO2排出面積単位使用量
    CO2_EMISSIONS_AREA_RANKING:str
    CO2_EMISSIONS:str                         #CO2排出量
    CRUDE_OIL_ENERGY_CONSUMPTION_UNIT:str     #原油換算エネルギー単位使用量
    CRUDE_OIL_ENERGY_CONSUMPTION:str          #原油換算エネルギー使用量
    ELECTRIC_CONSUMPTION_UNIT:str
    CREATION_DATETIME:datetime                #作成日時
    CREATOR:str                               #作成者
    UPDATE_DATETIME:str
    UPDATEOR:str
    DELETE_FLG:bool