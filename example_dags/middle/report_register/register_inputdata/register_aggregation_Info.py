import os
import math
import numpy as np
import pandas as pd
import middle.report_register.common.CommonEnergyAlgorithms as ceas
import middle.common.utils as utils
import middle.common.log as log
import middle.common.constants_colums as constants_colums
import middle.common.constants_values as constants_values
from middle.report_register.common.BuildingMonthlyEntity import BuildingMonthlyEntity
from middle.report_register.common.BuildingYearlyEntity import BuildingYearlyEntity
from middle.report_register.common.CorporationMonthlyEntity import CorporationMonthlyEntity
from middle.report_register.common.CorporationYearlyEntity import CorporationYearlyEntity
from middle.common.hql_processor import insert_data

# 空文字
json_config = utils.get_json_config()
schema_middle = json_config["database_posgre"]["schema_middle"]

DOT = constants_colums.SpecialChars.DOT.value
BLANK = constants_colums.SpecialChars.BLANK.value

# log用instance
logger = log.MiddleAppLog()
systemTime = utils.get_current_timestamp()

@log.log_writer(logger)
@utils.check_time
def register_energy_aggregation_info(
    conn, basic_df, df_generalInfo, df_buildingInfo, df_energyInfo, file_name):

    """
    関数名：企業カルテエネルギー集計結果登録
    params:
        df_generalInfo 企業基本情報
        df_buildingInfo 事業所情報
        df_energyInfo エネルギー情報
    """
    # 実行モード
    run_mode = constants_colums.RunMode.DEV.value \
        if os.environ.get("MIDDLE_RUN_MODE") is None else os.environ.get("MIDDLE_RUN_MODE")
    
    from middle.report_register.register_inputdata.common_main import master_data

    # マスタデータ取得
    ccmst = pd.read_json(master_data[constants_colums.MasterTable.CCMST.value], dtype=str) #
    ecmst = pd.read_json(master_data[constants_colums.MasterTable.ECMST.value]) #電力会社換算係数マスタ
    calmst = pd.read_json(master_data[constants_colums.MasterTable.CALMST.value]) #算定ロジックマスタ

    # ccmst, ecmst, calmst = get_mst_data(conn)
    #カラム名大文字にする
    ccmst.columns = ccmst.columns.str.upper()
    ecmst.columns = ecmst.columns.str.upper()
    calmst.columns = calmst.columns.str.upper()

    # ccmst['REPORT_YEAR'] = ccmst['REPORT_YEAR'].astype(str)
    # ccmst = ccmst[ccmst['REPORT_YEAR'] == df_generalInfo["FISCAL_YEAR"].iloc[0]]

    # 建物月別DF
    corporation_df = get_building_month_df(basic_df, df_generalInfo, df_buildingInfo, df_energyInfo, ccmst, ecmst, calmst)
    
    # 事業所年度別DF
    corporationProfileEntity_df = get_building_year_df(basic_df, corporation_df, df_generalInfo)
    
    # 企業月別DF
    corporationMonthlyEntity_df = get_company_month_df(basic_df, corporation_df, df_generalInfo)

    # 企業年度別DF
    corporationYearlyEntity_df = get_company_year_df(basic_df, corporation_df, df_generalInfo)

    
    try:
        #postgreへ生データ登録
        register_to_postgre(conn, corporation_df, corporationProfileEntity_df,corporationMonthlyEntity_df,
            corporationYearlyEntity_df, file_name)

        return corporation_df, corporationProfileEntity_df, corporationMonthlyEntity_df, corporationYearlyEntity_df

    except Exception as e:
        raise e

def get_value(officeUsedEnergyInfo, energyRowData, electricPowerCorporateCode, fiscal_year, ec_mst, calmst):
    #熱量換算エネルギー使用量
    calorificEnergyConsumption = crudeOilEnergyConsumption = co2EmissionCoefficient = None
    if officeUsedEnergyInfo is not None:
        # energyRowData['ENERGY_QUANTITY'] = energyRowData['ENERGY_QUANTITY'].replace('', np.nan).fillna(0)
        if energyRowData['ENERGY_QUANTITY'] is None or energyRowData['ENERGY_QUANTITY'] == '' or \
        (isinstance(energyRowData['ENERGY_QUANTITY'], float) and math.isnan(energyRowData['ENERGY_QUANTITY'])):
            energyRowData['ENERGY_QUANTITY'] = 0

        calorificEnergyConsumption = ceas.calorieConvert(calmst, 
            energyRowData['ENERGY_QUANTITY'], officeUsedEnergyInfo['CONVERSION_COEF'])

        #原油使用量
        crudeOilEnergyConsumption = ceas.crudeOilConvert(calmst, 
            energyRowData['ENERGY_QUANTITY'], officeUsedEnergyInfo['CONVERSION_COEF'], 
            constants_values.CRUDE_OIL_ENERGY_CONSUMPTION)
        
        #CO2排出量
        if constants_values.ENERGY_CODE_CITY_GAS == energyRowData['ENERGY_CODE'] and int(fiscal_year) > 2023: #2024年度都市ガス
            co2EmissionCoefficient = ceas.co2EmissionsConvert(calmst, energyRowData['ENERGY_QUANTITY'], officeUsedEnergyInfo['ENERGY_CO2_EMISSION_COEF'])
        #産業用蒸気、産業用以外の蒸気、温水、冷水
        elif constants_values.ENERGY_CODE_INDUSTRIAL_STEAM == energyRowData['ENERGY_CODE'] or\
             constants_values.ENERGY_CODE_INDUSTRIAL_EXCEPT_STEAM == energyRowData['ENERGY_CODE'] or\
             constants_values.ENERGY_CODE_HOT_WATER == energyRowData['ENERGY_CODE'] or\
             constants_values.ENERGY_CODE_COLD_WATER == energyRowData['ENERGY_CODE'] :
            co2EmissionCoefficient = ceas.co2EmissionsConvert(calmst, energyRowData['ENERGY_QUANTITY'], officeUsedEnergyInfo['ENERGY_CO2_EMISSION_COEF'])
        elif constants_values.ENERGY_CODE_ELECTRIC_POWER_2022 == energyRowData['ENERGY_CODE'] or\
             constants_values.ENERGY_CODE_ELECTRIC_POWER_2023 == energyRowData['ENERGY_CODE'] : #電力
            co2EmissionCoefficient = ceas.co2ElectricCoefficient(calmst, energyRowData['ENERGY_QUANTITY'], 
                                                                 utils.get_co2EmissionCoefficient(ec_mst,electricPowerCorporateCode, str(fiscal_year)))
        else:
            coefficient = ceas.co2ElectricExceptCoefficient(calmst, officeUsedEnergyInfo['CONVERSION_COEF'], 
                                                            officeUsedEnergyInfo['ENERGY_CO2_EMISSION_COEF'])
            co2EmissionCoefficient = ceas.co2EmissionsConvert(calmst, energyRowData['ENERGY_QUANTITY'], coefficient)

    return calorificEnergyConsumption, crudeOilEnergyConsumption, co2EmissionCoefficient

def get_building_month_entity(basic_df, df_generalInfo, energyRowData, officeUsedEnergyInfo,
    calorificEnergyConsumption, co2EmissionCoefficient, crudeOilEnergyConsumption, buildingArea):
    buildingMonthlyEntity = BuildingMonthlyEntity(
        df_generalInfo.at[0, 'CORPORATE_NUMBER'],       #法人番号
        df_generalInfo.at[0, 'BANK_CODE'],              #金融機関コード
        df_generalInfo.at[0,'AREA_ID'],                 #エリアID（事業所）
        energyRowData['AREA_INFORMATION'],              #エリア名称（事業所)
        basic_df['REGISTRATION_SEQ'].iloc[0],           #登録回数
        energyRowData['BUILDING_ID'],                   #建物ID
        energyRowData['BUILDING_NAME'],                 #事業所名称
        energyRowData['ENERGY_CODE'],                   #エネルギーコード
        energyRowData['ENERGY_SCOPE'],                  #スコープ
        energyRowData['ENERGY_NAME_JP'],                #エネルギー名称
        None,                                           #エネルギーカテゴリコード
        df_generalInfo.at[0, 'FISCAL_YEAR'],            #年度
        energyRowData['YEAR'],                          #対象年
        energyRowData['MONTH'],                         #対象月
        None if officeUsedEnergyInfo is None else officeUsedEnergyInfo['UNIT'],           #エネルギー単位
        energyRowData['ENERGY_QUANTITY'],               #年度エネルギー使用量
        calorificEnergyConsumption,                     #熱量換算エネルギー使用量
        # officeUsedEnergyInfo['UNIT_HEAT_GENERATION'],   #熱量換算面積単位使用量
        round(calorificEnergyConsumption/float(buildingArea), 6),   #熱量換算面積単位使用量
        None if co2EmissionCoefficient is None else \
            round(co2EmissionCoefficient/float(buildingArea), 6),           #CO2排出面積単位使用量
        co2EmissionCoefficient,                         #co2排出量
        None if crudeOilEnergyConsumption is None else \
              round(crudeOilEnergyConsumption/float(buildingArea), 6),      #原油換算エネルギー単位使用量
        crudeOilEnergyConsumption,                      #原油換算エネルギー使用量
        # officeUsedEnergyInfo['UNIT_HEAT_GENERATION'],
        round(energyRowData['ENERGY_QUANTITY']/float(buildingArea), 6),     #電力消費原単位
        systemTime,                                     #作成日時
        basic_df['CREATOR'].iloc[0],                            #作成者
        None,
        None,
        False)
    return buildingMonthlyEntity

def get_building_annual_entity(basic_df, df_generalInfo, row):
    buildingYearlyEntity = BuildingYearlyEntity(
        df_generalInfo.at[0,'CORPORATE_NUMBER'],        #法人番号
        df_generalInfo.at[0,'BANK_CODE'],               #金融機関コード
        df_generalInfo.at[0,'AREA_ID'],                 #エリアID（事業所）
        row.AREA_INFORMATION,                           #エリア名称（事業所）
        basic_df['REGISTRATION_SEQ'].iloc[0],           #登録回数
        row.BUILDING_ID,                                #建物ID
        row.BUILDING_NAME,                              #建物名称
        row.ENERGY_CODE,                                #エネルギーコード
        row.ENERGY_NAME,                                #エネルギー名称
        None,                                           #エネルギーカテゴリー
        df_generalInfo.at[0,'FISCAL_YEAR'],             #年度
        row.ENERGY_UNITS,                               #エネルギー単位
        row.ENERGY_CONSUMPTION,                         #年度エネルギー使用量
        row.CALORIFIC_ENERGY_CONSUMPTION,               #熱量換算エネルギー使用量
        row.CALORIFIC_ENERGY_CONSUMPTION_UNIT,          #熱量換算面積単位使用量
        row.CO2_EMISSIONS_AREA_UNIT,                    #CO2排出面積単位使用量
        row.CO2_EMISSIONS_AREA_RANKING,
        row.CO2_EMISSIONS,                              #CO2排出量
        row.CRUDE_OIL_ENERGY_CONSUMPTION_UNIT,          #原油換算エネルギー単位使用量
        row.CRUDE_OIL_ENERGY_CONSUMPTION,               #原油換算エネルギー使用量
        row.ELECTRIC_CONSUMPTION_UNIT,
        systemTime,                                     #作成日時　　
        basic_df['CREATOR'].iloc[0],                            #作成者
        None,
        None,
        False)
    return buildingYearlyEntity

def get_company_month_entity(basic_df, df_generalInfo, row):
    corporationMonthlyEntity = CorporationMonthlyEntity(
        df_generalInfo.at[0,'CORPORATE_NUMBER'],        #法人番号
        df_generalInfo.at[0,'BANK_CODE'],               #金融機関コード
        row.ENERGY_CODE,                                #エネルギーコード
        row.ENERGY_NAME,                                #エネルギー名称
        None,                                           #エネルギーカテゴリー
        basic_df['REGISTRATION_SEQ'].iloc[0],           #登録回数
        df_generalInfo.at[0,'FISCAL_YEAR'],             #年度
        row.YEAR,                                       #対象年
        row.MONTH,                                      #対象月
        row.ENERGY_UNITS,                               #エネルギー単位
        row.ENERGY_CONSUMPTION,                         #年度エネルギー使用量
        row.CALORIFIC_ENERGY_CONSUMPTION,               #熱量換算エネルギー使用量
        row.CALORIFIC_ENERGY_CONSUMPTION_UNIT,          #熱量換算面積単位使用量
        row.CO2_EMISSIONS_AREA_UNIT,                    #CO2排出面積単位使用量
        row.CO2_EMISSIONS,                              #co2排出量
        row.CO2_EMISSIONS_RANKING,                      #co2排出量ランキング
        row.CRUDE_OIL_ENERGY_CONSUMPTION_UNIT ,         #原油換算エネルギー単位使用量
        row.CRUDE_OIL_ENERGY_CONSUMPTION ,              #原油換算エネルギー使用量
        row.ELECTRIC_CONSUMPTION_UNIT,
        systemTime,                                     #作成日時　　
        basic_df['CREATOR'].iloc[0],                            #作成者
        None,
        None,
        False)     
    return corporationMonthlyEntity

def get_company_annual_entity(basic_df, df_generalInfo, row):
    corporationYearlyEntity = CorporationYearlyEntity(
        df_generalInfo.at[0,'CORPORATE_NUMBER'],        #法人番号
        df_generalInfo.at[0,'BANK_CODE'],               #金融機関コード
        row.ENERGY_CODE,                                #エネルギーコード
        row.ENERGY_NAME,                                #エネルギー名称
        None,                                           #エネルギーカテゴリー
        basic_df['REGISTRATION_SEQ'].iloc[0],           #登録回数
        df_generalInfo.at[0,'FISCAL_YEAR'],             #年度
        row.ENERGY_UNITS,                               #エネルギー単位
        row.ENERGY_CONSUMPTION,                         #年度エネルギー使用量
        row.CALORIFIC_ENERGY_CONSUMPTION,               #熱量換算エネルギー使用量
        row.CALORIFIC_ENERGY_CONSUMPTION_UNIT,          #熱量換算面積単位使用量
        row.CO2_EMISSIONS_AREA_UNIT,                    #CO2排出面積単位使用量
        row.CO2_EMISSIONS,                              #co2排出量
        row.CO2_EMISSIONS_RANKING,                      #co2排出量ランキング
        row.CRUDE_OIL_ENERGY_CONSUMPTION_UNIT ,         #原油換算エネルギー単位使用量
        row.CRUDE_OIL_ENERGY_CONSUMPTION ,              #原油換算エネルギー使用量
        row.ELECTRIC_CONSUMPTION_UNIT,
        systemTime,                                     #作成日時　　
        basic_df['CREATOR'].iloc[0],                            #作成者
        None,
        None,
        False)
    return corporationYearlyEntity

def make_df_columns(df_columns, grouped_df):
    target_df = pd.DataFrame(columns = df_columns)
    for column in df_columns:
        if column in grouped_df.columns:
            target_df[column] = grouped_df[column]
        else:
            target_df[column] = np.nan
    target_df.fillna(BLANK, inplace=True)

    return target_df

def get_building_year_df(basic_df, corporation_df, df_generalInfo):
    '''
    建物年別集計データDF取得
    params:
    return:
    '''
    corporationProfileEntityList = []
    officeYearly_grouped_df = corporation_df.groupby(
        ['ENERGY_CODE','AREA_INFORMATION','BUILDING_NAME','ENERGY_NAME','ENERGY_UNITS','BUILDING_ID'])\
        [['ENERGY_CONSUMPTION','CALORIFIC_ENERGY_CONSUMPTION','CALORIFIC_ENERGY_CONSUMPTION_UNIT',\
          'CO2_EMISSIONS_AREA_UNIT','CO2_EMISSIONS','CRUDE_OIL_ENERGY_CONSUMPTION_UNIT',\
            'CRUDE_OIL_ENERGY_CONSUMPTION', 'ELECTRIC_CONSUMPTION_UNIT']].sum().reset_index()
    
    #CO2排出量ランキング計算
    area_emissions_rank = officeYearly_grouped_df.groupby('AREA_INFORMATION')['CO2_EMISSIONS_AREA_UNIT'].sum()\
    .rank(method='first', ascending=False).astype(int)

    officeYearly_grouped_df['CO2_EMISSIONS_AREA_RANKING'] = officeYearly_grouped_df['AREA_INFORMATION'].map(area_emissions_rank)


    officeYearly_df = make_df_columns(constants_colums.officeYearly_columns, officeYearly_grouped_df)

    for row in officeYearly_df.itertuples(index=True):
        corporationProfileEntity = get_building_annual_entity(basic_df, df_generalInfo, row)
        #リストに集計済エネルギー情報格納
        corporationProfileEntityList.append(corporationProfileEntity)
    corporationProfileEntity_df = pd.DataFrame(corporationProfileEntityList)
    
    return corporationProfileEntity_df

def get_company_month_df(basic_df, corporation_df, df_generalInfo):
    '''
    企業月別集計データDF取得
    params:
    return:
    '''
    corporationMonthlyEntityList = []
    corporateMonthly_grouped_df = corporation_df.groupby(
        ['ENERGY_CODE','ENERGY_NAME','ENERGY_UNITS','FISCAL_YEAR','YEAR','MONTH'])\
        [['ENERGY_CONSUMPTION','CALORIFIC_ENERGY_CONSUMPTION','CALORIFIC_ENERGY_CONSUMPTION_UNIT',\
          'CO2_EMISSIONS_AREA_UNIT','CO2_EMISSIONS', 'CRUDE_OIL_ENERGY_CONSUMPTION_UNIT',\
            'CRUDE_OIL_ENERGY_CONSUMPTION', 'ELECTRIC_CONSUMPTION_UNIT']].sum().reset_index()
    
    #CO2排出量ランキング計算
    monthly_emissions_rank = corporateMonthly_grouped_df.groupby('MONTH')['CO2_EMISSIONS'].sum()\
    .rank(method='first', ascending=False).astype(int)

    corporateMonthly_grouped_df['CO2_EMISSIONS_RANKING'] = corporateMonthly_grouped_df['MONTH'].map(monthly_emissions_rank)
    
    # corporateMonthly_grouped_df['CO2_EMISSIONS_RANKING'] = \
    #     corporateMonthly_grouped_df.groupby(['MONTH'])['CO2_EMISSIONS'].sum().\
    #         rank(method = 'first',ascending=False).astype(int)
    
    corporateMonthly_df = make_df_columns(constants_colums.corporateMonthly_columns, corporateMonthly_grouped_df)

    for row in corporateMonthly_df.itertuples(index=True):
        corporationMonthlyEntity = get_company_month_entity(basic_df, df_generalInfo, row)                 
        #リストに集計済エネルギー情報格納
        corporationMonthlyEntityList.append(corporationMonthlyEntity)
    
    corporationMonthlyEntity_df = pd.DataFrame(corporationMonthlyEntityList)

    return corporationMonthlyEntity_df

def get_company_year_df(basic_df, corporation_df, df_generalInfo):
    '''
    企業年別集計データDF取得
    params:
    return:
    '''
    corporationYearlyEntityList = []
    corporateYearly_grouped_df = corporation_df.groupby(
        ['ENERGY_CODE','ENERGY_NAME','ENERGY_UNITS'])\
        [['ENERGY_CONSUMPTION','CALORIFIC_ENERGY_CONSUMPTION','CALORIFIC_ENERGY_CONSUMPTION_UNIT',\
          'CO2_EMISSIONS_AREA_UNIT','CO2_EMISSIONS','CRUDE_OIL_ENERGY_CONSUMPTION_UNIT',\
            'CRUDE_OIL_ENERGY_CONSUMPTION','ELECTRIC_CONSUMPTION_UNIT']].sum().reset_index()
    
    #CO2排出量ランキング計算
    corporateYearly_grouped_df['CO2_EMISSIONS_RANKING'] = corporateYearly_grouped_df['CO2_EMISSIONS'].\
    rank(method='dense', ascending=False).astype(int)
    
    corporateYearly_df = make_df_columns(constants_colums.corporateYearly_columns, corporateYearly_grouped_df)

    for row in corporateYearly_df.itertuples(index=True):
        corporationYearlyEntity = get_company_annual_entity(basic_df, df_generalInfo, row)   
        #リストに集計済エネルギー情報格納
        corporationYearlyEntityList.append(corporationYearlyEntity)
    corporationYearlyEntity_df = pd.DataFrame(corporationYearlyEntityList)

    return corporationYearlyEntity_df

def get_electric_company_buildingarea(df_buildingInfo, energyRowData):
    #電力会社名前変数定義
    electricPowerCorporateCode = BLANK
    #建物面積変数定義
    buildingArea = BLANK

    for index, buildingRowData in df_buildingInfo.iterrows():

        if buildingRowData['AREA_INFORMATION'] == energyRowData['AREA_INFORMATION']:
            electricPowerCorporateCode = buildingRowData['REGISTRATION_NUMBER']
            buildingArea = buildingRowData['GROSS_FLOOR_AREA']
            return electricPowerCorporateCode, buildingArea
            
def get_office_usedenergy_info(ccmst, energyRowData, emission_coef_year):
    # 換算係数マスタから処理中エネルギーデータを取得する(DataFrame型)
    office_usedenergy_info = None
    
    ccmst_sub = ccmst[ccmst['REPORT_YEAR'] == str(emission_coef_year)]

    for index, item in ccmst_sub.iterrows():
        if str(item['MAJOR_CATEGORY_ID']) + str(item['MIDDLE_CATEGORY_ID']) + str(item['MINOR_CATEGORY_ID'])\
              == energyRowData['ENERGY_CODE'] :
            # if str(item['REPORT_YEAR']) == str(emission_coef_year):
            office_usedenergy_info = item
            return office_usedenergy_info

def get_building_month_df(basic_df, df_generalInfo, df_buildingInfo, df_energyInfo, ccmst, ecmst, calmst):
    '''
    建物月別集計データDF取得
    params:
    return:
    '''
    corporationProfileMonthlyList = []
    # ENERGY_NAME_JPが「電気」の場合、ENERGY_CODEを設定
    df_energyInfo["ENERGY_CODE"] = df_energyInfo["ENERGY_NAME_JP"].map(lambda x: constants_colums.enery_code_mapping.get(x, None))
    
    df_energyInfo = df_energyInfo.assign(ENERGY_SCOPE = None)
    
    # 建物月別DF
    for index, energyRowData in df_energyInfo.iterrows():
        #初期化
        calorificEnergyConsumption = crudeOilEnergyConsumption = co2EmissionCoefficient = buildingArea = 0

        #係数年度
        emission_coef_year = None
        emission_coef_month = str(energyRowData['YEAR']) + '4'
        input_month = str(energyRowData['YEAR']) + str(energyRowData['MONTH'])
        #月の年ごとに係数情報取得
        if int(input_month) < int(emission_coef_month):
            emission_coef_year = energyRowData['YEAR']
        else:
            emission_coef_year = energyRowData['YEAR'] + 1    
            
        #エネルギー値0へ変換
        if bool(energyRowData['ENERGY_QUANTITY']) is False:
            energyRowData['ENERGY_QUANTITY'] = 0

        #2023年度以前で電気の場合、電気エネルギーコード変更
        if int(emission_coef_year) < 2024 and energyRowData["ENERGY_NAME_JP"] == '電気':
            energyRowData["ENERGY_CODE"] = constants_values.ENERGY_CODE_ELECTRIC_POWER_2022

        # 換算係数マスタから処理中エネルギーデータを取得する(DataFrame型)
        officeUsedEnergyInfo = get_office_usedenergy_info(ccmst, energyRowData, emission_coef_year)

        if officeUsedEnergyInfo is None:
            print('換算係数マスタ情報取得は失敗しました。' + energyRowData["ENERGY_CODE"] )
            print(emission_coef_year)
        
        # 電力会社名、建物面積取得
        electricPowerCorporateCode, buildingArea = \
            get_electric_company_buildingarea(df_buildingInfo, energyRowData)

        #月単位の年の対象外エネルギーを外す
        if energyRowData['ENERGY_QUANTITY'] != 0 and bool(energyRowData['ENERGY_QUANTITY']):

            #熱量、原油、CO2排出量換算
            calorificEnergyConsumption, crudeOilEnergyConsumption, co2EmissionCoefficient = \
                get_value(officeUsedEnergyInfo, energyRowData, electricPowerCorporateCode, \
                        emission_coef_year, ecmst, calmst)
        
        #スコープバリュー設定
        set_scope_value(energyRowData)

        #Nan値を0に変更
        calorificEnergyConsumption = 0 if math.isnan(calorificEnergyConsumption) else calorificEnergyConsumption
        crudeOilEnergyConsumption = 0 if math.isnan(crudeOilEnergyConsumption) else crudeOilEnergyConsumption
        co2EmissionCoefficient = 0 if math.isnan(co2EmissionCoefficient) else co2EmissionCoefficient

        #TABLEAU表示のため、エネルギーコード統一にする
        if energyRowData['ENERGY_CODE'] == '0200010001':
            energyRowData['ENERGY_CODE'] = '0200010011'

        # 建物月別集計データEntity取得
        corporationProfileMonthlyEntity = get_building_month_entity(
            basic_df, df_generalInfo, energyRowData, officeUsedEnergyInfo,calorificEnergyConsumption, 
            co2EmissionCoefficient, crudeOilEnergyConsumption, buildingArea)
        
        #エネルギー消費がない月はスキップ
        # if corporationProfileMonthlyEntity.ENERGY_CONSUMPTION == 0:
        #     continue

        #リストに集計済エネルギー情報格納
        corporationProfileMonthlyList.append(corporationProfileMonthlyEntity)
    
    #集計済みエネルギー情報登録
    corporation_df = utils.toDf(corporationProfileMonthlyList)

    return corporation_df

def register_to_postgre(
        conn, corporation_df, corporationProfileEntity_df,corporationMonthlyEntity_df,
        corporationYearlyEntity_df, file_name):
    '''
    Hadoop Hiveデータ蓄積
    params:
    '''
    # TDH登録処理実行
    
    # エネルギー集計結果テーブル名
    table_name_EATBL = constants_colums.BusinessTable.EATBL.value      #T_ANNUAL_BUILDING_ENERGY_AGGREGATION
    table_name_EAMTBL = constants_colums.BusinessTable.EAMTBL.value    #T_MONTHLY_BUILDING_ENERGY_AGGREGATION
    table_name_ACEATBL = constants_colums.BusinessTable.ACEATBL.value  #T_ANNUAL_CORPORATE_ENERGY_AGGREGATION
    table_name_MCEATBL = constants_colums.BusinessTable.MCEATBL.value  #T_MONTHLY_CORPORATE_ENERGY_AGGREGATION
    
    # partition_values = (bank_cd, company_number, area_id, year)
    # partiontion_dict = dict(zip(constants_colums.PARTITION_COLUMNS, partition_values))
    
    insert_data(conn,corporation_df,constants_colums.officeMonthly_columns,None,
                schema_middle + DOT + table_name_EAMTBL,file_name)
    insert_data(conn,corporationProfileEntity_df,constants_colums.officeYearly_columns,None,
                schema_middle + DOT + table_name_EATBL,file_name)
    
    # partition_values = (bank_cd, company_number, year)
    # partiontion_dict = dict(zip(constants_colums.PARTITION_COMPANY_COLUMNS, partition_values))
    insert_data(conn,corporationMonthlyEntity_df,constants_colums.corporateMonthly_columns,None,
                schema_middle + DOT + table_name_MCEATBL,file_name)
    insert_data(conn,corporationYearlyEntity_df,constants_colums.corporateYearly_columns,None,
                    schema_middle + DOT + table_name_ACEATBL,file_name)

def register_to_hive(
        conn, corporation_df, corporationProfileEntity_df,corporationMonthlyEntity_df,
        corporationYearlyEntity_df, file_name):
    '''
    Hadoop Hiveデータ蓄積
    params:
    '''
    # TDH登録処理実行
    
    # エネルギー集計結果テーブル名
    table_name_EATBL = constants_colums.BusinessTable.EATBL.value      #T_ANNUAL_BUILDING_ENERGY_AGGREGATION
    table_name_EAMTBL = constants_colums.BusinessTable.EAMTBL.value    #T_MONTHLY_BUILDING_ENERGY_AGGREGATION
    table_name_ACEATBL = constants_colums.BusinessTable.ACEATBL.value  #T_ANNUAL_CORPORATE_ENERGY_AGGREGATION
    table_name_MCEATBL = constants_colums.BusinessTable.MCEATBL.value  #T_MONTHLY_CORPORATE_ENERGY_AGGREGATION

    bank_cd = corporation_df["BANK_CODE"].iloc[0]
    company_number = corporation_df["CORPORATE_NUMBER"].iloc[0]
    year = corporation_df["FISCAL_YEAR"].iloc[0]
    building_id = corporation_df['BUILDING_ID'].iloc[0]
    
    partition_values = (bank_cd, company_number, building_id, year)
    partiontion_dict = dict(zip(constants_colums.PARTITION_COLUMNS_CAITBL, partition_values))
    
    insert_data(conn,corporation_df,constants_colums.officeMonthly_hive_columns,partiontion_dict,
                schema_middle + DOT + table_name_EAMTBL,file_name)
    insert_data(conn,corporationProfileEntity_df,constants_colums.officeYearly_hive_columns,partiontion_dict,
                schema_middle + DOT + table_name_EATBL,file_name)
    
    partition_values = (bank_cd, company_number, year)
    partiontion_dict = dict(zip(constants_colums.PARTITION_COMPANY_COLUMNS, partition_values))
    insert_data(conn,corporationMonthlyEntity_df,constants_colums.corporateMonthly_hive_columns,partiontion_dict,
                schema_middle + DOT + table_name_MCEATBL,file_name)
    insert_data(conn,corporationYearlyEntity_df,constants_colums.corporateYearly_hive_columns,partiontion_dict,
                    schema_middle + DOT + table_name_ACEATBL,file_name)

def set_scope_value(energyRowData):
    """
    スコープバリュー設定
    """
    # scope1_codes = {'0100010000' ,'0100020000','0100030000','0100070000','0100080000','0100090000','0100100000','0100110000','0100120000','0100130000',
    #                 '0100150000','0100180000','0100200000','0100210000','0100240000','0100250000','0100260000','0100300000','0100310000','0100320000',
    #                 '0100330000','0100340000','0100360000','2200040000','0100220000'}
    
    scope2_codes = {'0300010000','0300020000','0300030000','0300040000','0200010011', '0200010001'}
    
    if energyRowData['ENERGY_CODE'] in scope2_codes:
        energyRowData['ENERGY_SCOPE'] = '2'
    # elif energyRowData['ENERGY_CODE'] in scope1_codes:
    #     energyRowData['ENERGY_SCOPE'] =  '1'
    else: energyRowData['ENERGY_SCOPE'] =  '1' 

# def get_mst_data(conn):
#     '''
#     マスタデータ取得
#     params:
#         conn Hive接続し
#     return:
#         jic_mst  業種マスタ
#         ec_mst   電力会社排出係数マスタ
#     '''
#     ccmst = ecmst = calmst = None

#     # masterデータ格納オブジェクト
#     master_data = CommonMasterDataLoader(conn)
#     # 区分マスタ
#     # kbn_mst = master_data.kbnmst_list
#     # 業種マスタ
#     ccmst = master_data.ccmst_list
#     # 電力会社の排出係数マスタ
#     ecmst = master_data.ecmst_list

#     calmst = master_data.calmst_list
    
#     return ccmst, ecmst, calmst