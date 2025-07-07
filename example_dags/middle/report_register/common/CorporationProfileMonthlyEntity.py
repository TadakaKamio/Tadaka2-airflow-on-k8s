from dataclasses import dataclass
import datetime
 
@dataclass
#建物年別
class CorporationProfileMonthlyEntity:
    CORPORATE_NUMBER:str                      #法人番号
    BANK_CODE:str                             #金融機関コード
    AREA_ID:str            
    AREA_INFORMATION:str                           #事業所名                     
    BUILDING_ID:str            
    BUILDING_NAME:str                           #事業所名
    ENERGY_CODE:str                           #エネルギーコード
    ENERGY_NAME:str                           #エネルギー名
    CATEGORY:str                       #エネルギーコード
    FISCAL_YEAR:str                           #年度
    YEAR:str                                  #対象年
    MONTH:str                                 #対象月
    ENERGY_UNITS:str                          #エネルギー単位
    ENERGY_CONSUMPTION:str                    #年度エネルギー使用量
    CALORIFIC_ENERGY_CONSUMPTION:str          #熱量換算エネルギー使用量
    CALORIFIC_ENERGY_CONSUMPTION_UNIT:str
    CO2_EMISSIONS_AREA_UNIT:str               #CO2排出面積単位使用量
    CO2_EMISSIONS:str                         #CO2排出量
    CRUDE_OIL_ENERGY_CONSUMPTION_UNIT:str     #原油換算エネルギー単位使用量
    CRUDE_OIL_ENERGY_CONSUMPTION:str          #原油換算エネルギー使用量
    ELECTRIC_CONSUMPTION_UNIT:str
    TARGET_YEAR:str
    BUILDING_USAGE:str
    QUADRANT:str
    SCATTER_PLOT_LABEL:str
    PRIMARY_ENERGY_CONSUMPTION_E:str
    PRIMARY_ENERGY_CONSUMPTION_GAS:str
    PRIMARY_ENERGY_CONSUMPTION_OTHER:str
    PRIMARY_ENERGY_CONSUMPTION:str
    PRIMARY_ENERGY_EQUIVALENT:str
    ENERGY_CONSUMPTION_DUE_RENOVATION_E:str
    REDUCTION_AMOUNT_DUE_RENOVATION_E:str
    REDUCTION_AMOUNT_DUE_ENERGY_EFFORTS_GOAL_E:str
    REDUCTION_AMOUNT_DUE_POWER_GENERATION_E:str
    TRANSFER_REMOVAL_SALE_E:str
    ACTUAL_PERFORMANCE_E:str
    CO2_EMISSIONS_C:str
    REDUCTION_AMOUNT_DUE_RENOVATION_C:str
    REDUCTION_AMOUNT_DUE_ENERGY_EFFORTS_GOAL_C:str
    REDUCTION_AMOUNT_DUE_POWER_GENERATION_C:str
    REDUCTION_AMOUNT_DUE_ELECTRIFICATION:str
    TRANSFER_REMOVAL_SALE_C:str
    REDUCTION_EFFECT_SUPPLY_SIDE:str
    REDUCTION_EFFECT_DUE_CERTIFICATE_PURCHASE:str
    ACTUAL_PERFORMANCE_C:str
    CREATION_DATETIME:datetime                #作成日時
    CREATOR:str                               #作成者
 