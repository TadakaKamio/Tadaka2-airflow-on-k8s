# 入力情報-数値チェック
application_basic_information_checknumber_list = [
    ["GROSS_FLOOR_AREA", 6, 2],                                     #延床面積
    ["CONTRACTED_POWER", 7, 3],                                     #契約電力
    ["ELECTRICITY_USAGE_FEE_SUMMER", 4, 2],                         #電力量料金（夏季）
    ["ELECTRICITY_USAGE_FEE_OTHER_SEASONS", 4, 2],                  #電力量料金（その他季）
    ["FUEL_COST_ADJUSTMENT", 4, 2],                                 #燃料費調整額
    ["RENEWABLE_ENERGY_SURCHARGE", 4, 2],                           #再エネ賦課金
    ["WORKING_HOURS_ONE_DAY", 7, 3],                                #1日の稼働時間
    ["ROOF_AREA", 6, 2],                                            #屋根面積
    ["ROOF_AREA", 6, 2],                                            #駐車場面積
    ["FLUORESCENT_LIGHTS_PERCENTAGE", 1, 4],                        #蛍光灯割合
    ["LED_LIGHTS_PERCENTAGE", 1, 4]                                 #LED割合
]
# 入力情報-メールチェック
application_basic_information_checkmail_list = [
    ["EMAIL_ADDRESS_LOCAL_BANK"]                                    #メールアドレス(地銀)
]
# 入力情報-日付チェック
application_basic_information_checkdate_list = [
    ["UTILIZATION_APPROVAL_DATE_CORPORATE", 8],                     #利用承諾日(企業)
    ["FISCAL_YEAR", 4],                                             #年度
    ["START_PERIOD", 8],                                            #期初
    ["END_PERIOD", 8],                                              #期末
    ["BUILDING_COMPLETION_YEAR", 4],                                #建物竣工年
    ["YEAR_AIR_CONDITIONING_REPLACEMENT", 4]                        #空調入れ替え年
]
# 入力情報-固定長さチェック
application_basic_information_fixed_length_data_check_list = [
    ["BANK_CODE", 4],                                               #金融機関コード
    ["BRANCH_CODE", 3],                                             #支店コード
    ["CORPORATE_NUMBER", 13],                                       #法人番号
    ["AREA_ID", 6],                                                 #エリアID
    ["SUPPLY_POINT_NUMBER", 27],                                    #供給地点特定番号
    ["EP_STORE_NUMBER", 3],                                         #EP店所番号
    ["CUSTOMER_NUMBER_EP", 16],                                     #EPお客さま番号
    ["REGISTRATION_NUMBER", 5]                                      #登録番号
]
# 入力情報-電話番号チェック
application_basic_information_phone_number_check_list = [
    ["PHONE_NUMBER_LOCAL_BANK"],                                #電話番号(地銀)
    ["PHONE_NUMBER_CORPORATE"]                                  #電話番号(企業)
]
# エネルギー費用-数値チェック
tepco_energy_solution_info_checknumber_list = [
    ["ELECTRIC_USAGE_TARIFFS", 4, 2],                               #電気従量課金単価
    ["CITY_GAS_RATES_SUMMER", 4, 2],                                #都市ガス従量料金(夏季)
    ["CITY_GAS_RATES_OTHER_SEASONS", 4, 2],                         #都市ガス従量料金(その他季)
    ["CITY_GAS_RATES_WEIGHTED_AVERAGE", 4, 2],                      #都市ガス従量料金(加重平均)
    ["CITY_GAS_RATES_FIFTY", 4, 2],                                 #都市ガス従量料金(50m4あたり)
    ["CITY_GAS_RATES_ONE", 4, 2],                                   #都市ガス従量料金(1m3あたり)
    ["RENDERABLE_RATIO", 1, 2],                                     #レンタブル比
    ["LED_PRICE", 8, 0],                                            #LED電球単価
    ["LED_INSTALLATION_PRICE", 6, 0],                               #LED工事単価
    ["LED_ANNUAL_POWER_CONSUMPTION", 6, 0],                         #LED電球年間消費電力量
    ["LED_RATED_POWER_CONSUMPTION", 5, 1],                          #LED電球定格消費電力
    ["LED_RATED_LIFETIME", 8, 0],                                   #LED電球定格寿命
    ["LEGAL_SERVICE_LIFE", 6, 0],                                   #法定耐用年数
    ["PRACTICAL_SERVICE_LIFE", 5, 1],                               #実用耐用年数
    ["FLUORESCENT_LAMP_PRICE", 6, 0],                               #電球型蛍光灯単価
    ["ANNUAL_POWER_CONSUMPTION", 6, 0],                             #年間消費電力量
    ["FLUORESCENT_LAMP_ANNUAL_POWER_CONSUMPTION", 6, 0],            #電球型蛍光灯定格消費電力
    ["FLUORESCENT_LAMP_LIFETIME", 8, 0],                            #電球型蛍光灯定格寿命
    ["REQUIRED_LIGHT", 4, 2],                                       #実用耐用年数
    ["FLUORESCENT_LAMP_REPLACEMENT_FREQUENCY", 5, 1],               #電球型蛍光灯交換回数
    ["SUBSIDIE", 8, 0],                                             #補助金
    ["ADJUSTMENT_VARIABLE", 6, 0],                                  #調整用変数
    ["PV_USABLE_AREA_RATIO", 1, 2],                                 #PV使用可能面積比率
    ["AREA_TO_POWER_CONVERSION", 4, 2],                             #使用可能面積PV設置時の面積kW換算
    ["ANNUAL_GENERATION_PER_CAPACITY", 6, 0],                       #設備容量あたりの年間発電量
    ["SELF_CONSUMPTION_RATE", 1, 2],                                #自家消費率
    ["PV_UNIT_PRICE", 8, 0],                                        #PV単価(工事費含む)
    ["PV_MOUNTING_INSTALLATION_COST", 8, 0],                        #PV架台・工事費単価
    ["PV_OM_COST_PER_UNIT", 8, 0],                                  #PVのO&M費用単価
    ["EQUIPMENT_UNIT_PRICE", 8, 0],                                 #設備単価
    ["CONSTRUCTION_UNIT_PRICE", 8, 0],                              #工事単価
    ["ANNUAL_GENERATION_PER_CAPACITY", 6, 0],                       #設備容量あたりの年間発電量    
    ["HEAT_LOAD_BASIS_UNIT", 5, 1],                                 #熱負荷原単位
    ["MULTI_EQUIPMENT_COST", 8, 0],                                 #機器代金(ビル用マルチエアコン)
    ["COMMERCIAL_EQUIPMENT_COST", 8, 0],                            #機器代金(店舗・オフィスエアコン)
    ["CENTRAL_EQUIPMENT_COST", 8, 0],                               #機器代金(セントラル空調)
    ["MULTI_EQUIPMENT_COST_AREA", 8, 0],                            #面積当たり機器代金(ビル用マルチエアコン)
    ["COMMERCIAL_EQUIPMENT_COST_AREA", 8, 0],                       #面積当たり機器代金(店舗・オフィスエアコン)
    ["CENTRAL_EQUIPMENT_COST_AREA", 8, 0],                          #面積当たり機器代金(セントラル空調)
    ["COOLING_LOAD_RUNTIME", 6, 0],                                 #全負荷相当運転時間（冷房）
    ["HEATING_LOAD_RUNTIME", 6, 0],                                 #全負荷相当運転時間（暖房）
    ["GAS_UNIT_PRICE", 4, 2],                                       #ガス単価
    ["ECO_CUTE_EXPENSES", 8, 0],                                    #エコキュート費用
    ["MODEL_EQUIPMENT_CAPACITY_INTERIM", 5, 1],                     #モデル機器設備容量(中間期)
    ["MODEL_EQUIPMENT_CAPACITY_WINTER", 5, 1],                      #モデル機器設備容量(冬季)
    ["ENERGY_EFFICIENCY", 4, 2],                                    #エネルギー効率
    ["CITY_GAS_HIGH_CALORIFIC", 5, 1],                              #都市ガス高位発熱量
    ["LPG_GAS_HIGH_CALORIFIC", 5, 1],                               #LPGガス高位発熱量
    ["CITY_GAS_LOW_CALORIFIC", 5, 1],                               #都市ガス低位発熱量
    ["LPG_GAS_LOW_CALORIFIC", 5, 1],                                #LPGガス低位発熱量    
    ["OPERATING_DAYS_SEASON", 6, 0],                                #季節n稼働日数
    ["OPERATING_DAYS_OTHER", 6, 0],                                 #その他季稼働日数
    ["HOT_WATER_TEMPERTURE", 5, 1],                                 #給湯温度
    ["WATER_SUPPLY_TEMPERTURE_SEASON", 5, 1],                       #給水温度(季節n)
    ["WATER_SUPPLY_TEMPERTURE_OTHER", 5, 1],                        #給水温度(その他季節加重平均)
    ["EHP_OPERATING_HOURS", 5, 1],                                  #EHPの1日当たりの稼働時間
    ["HOT_WATER_SYSTEM_EFFICIENCY", 1, 2],                          #給湯システムの効率
    ["PEAK_FACTOR", 5, 1],                                          #ピーク係数
    ["SEVERE_WINTER_COP", 5, 1],                                    #厳冬期COP
    ["INTERIM_COP", 5, 1]                                           #中間期COP 
]
# エネルギー費用-日付チェック
tepco_energy_solution_info_checkdate_list = [
    ["FISCAL_YEAR",4]                                               #年度
]
# エネルギー費用-固定長さチェック
tepco_energy_solution_info_fixed_length_data_check_list = [
    ["CORPORATE_NUMBER",13],                                        #法人番号
    ["BANK_CODE",4]                                                 #金融機関コード
]
# 年度別建物エネルギー集計情報-数値チェック
annual_building_energy_aggregation_checknumber_list = [
    ["ENERGY_CONSUMPTION", 10, 2],                                  #年度エネルギー使用量
    ["CO2_EMISSIONS", 10, 2],                                       #CO2排出量
    ["CO2_EMISSIONS_AREA_UNIT", 4, 4],                              #CO2排出原単位
    ["CALORIFIC_ENERGY_CONSUMPTION", 10, 2],                        #熱量換算エネルギー使用量
    ["CALORIFIC_ENERGY_CONSUMPTION_UNIT", 4, 4],                    #熱量換算エネルギー消費原単位
    ["CRUDE_OIL_ENERGY_CONSUMPTION", 10, 2],                        #原油換算エネルギー使用量 
    ["CRUDE_OIL_ENERGY_CONSUMPTION_UNIT", 4, 4],                    #原油換算エネルギー消費原単位  
    ["ELECTRIC_CONSUMPTION_UNIT", 4, 4]                             #電力消費原単位  
]
# 年度別建物エネルギー集計情報-日付チェック
annual_building_energy_aggregation_checkdate_list = [
    ["FISCAL_YEAR",4]                                               #年度
]
# 年度別建物エネルギー集計情報-固定長さチェック
annual_building_energy_aggregation_fixed_length_data_check_list = [
    ["CORPORATE_NUMBER",13],                                        #法人番号
    ["BANK_CODE",4],                                                #金融機関コード
    ["BUILDING_ID",16]                                              #建物ID
]
# 月別建物エネルギー集計情報-数値チェック
monthly_building_energy_aggregation_checknumber_list = [
    ["ENERGY_CONSUMPTION", 10, 2],                                  #年度エネルギー使用量
    ["CO2_EMISSIONS", 10, 2],                                       #CO2排出量
    ["CO2_EMISSIONS_AREA_UNIT", 4, 4],                              #CO2排出原単位
    ["CALORIFIC_ENERGY_CONSUMPTION", 10, 2],                        #熱量換算エネルギー使用量
    ["CALORIFIC_ENERGY_CONSUMPTION_UNIT", 4, 4],                    #熱量換算エネルギー消費原単位
    ["CRUDE_OIL_ENERGY_CONSUMPTION", 10, 2],                        #原油換算エネルギー使用量 
    ["CRUDE_OIL_ENERGY_CONSUMPTION_UNIT", 4, 4],                    #原油換算エネルギー消費原単位  
    ["ELECTRIC_CONSUMPTION_UNIT", 4, 4]                             #電力消費原単位  
]
# 月別建物エネルギー集計情報-日付チェック
monthly_building_energy_aggregation_checkdate_list = [
    ["FISCAL_YEAR",4],                                              #年度
    ["YEAR",4]                                                      #対象年  
]
# 月別建物エネルギー集計情報-月チェック
monthly_building_energy_aggregation_month_check_list = [
    ["MONTH"]                                                       #対象月
]
# 月別建物エネルギー集計情報-固定長さチェック
monthly_building_energy_aggregation_fixed_length_data_check_list = [
    ["CORPORATE_NUMBER",13],                                        #法人番号
    ["BANK_CODE",4],                                                #金融機関コード
    ["BUILDING_ID",16]                                              #建物ID
]
# 年度別法人エネルギー集計情報-数値チェック
annual_corporate_energy_aggregation_checknumber_list = [
    ["ENERGY_CONSUMPTION", 10, 2],                                  #年度エネルギー使用量
    ["CO2_EMISSIONS", 10, 2],                                       #CO2排出量
    ["CO2_EMISSIONS_AREA_UNIT", 4, 4],                              #CO2排出原単位
    ["CALORIFIC_ENERGY_CONSUMPTION", 10, 2],                        #熱量換算エネルギー使用量
    ["CALORIFIC_ENERGY_CONSUMPTION_UNIT", 4, 4],                    #熱量換算エネルギー消費原単位
    ["CRUDE_OIL_ENERGY_CONSUMPTION", 10, 2],                        #原油換算エネルギー使用量 
    ["CRUDE_OIL_ENERGY_CONSUMPTION_UNIT", 4, 4],                    #原油換算エネルギー消費原単位  
    ["ELECTRIC_CONSUMPTION_UNIT", 4, 4]                             #電力消費原単位  
]
# 年度別法人エネルギー集計情報-日付チェック
annual_corporate_energy_aggregation_checkdate_list = [
    ["FISCAL_YEAR",4]                                               #年度
]
# 年度別法人エネルギー集計情報-固定長さチェック
annual_corporate_energy_aggregation_fixed_length_data_check_list = [
    ["CORPORATE_NUMBER",13],                                        #法人番号
    ["BANK_CODE",4]                                                 #金融機関コード
]
# 月別法人エネルギー集計情報-数値チェック
monthly_corporate_energy_aggregation_checknumber_list = [
    ["ENERGY_CONSUMPTION", 10, 2],                                  #年度エネルギー使用量
    ["CO2_EMISSIONS", 10, 2],                                       #CO2排出量
    ["CO2_EMISSIONS_AREA_UNIT", 4, 4],                              #CO2排出原単位
    ["CALORIFIC_ENERGY_CONSUMPTION", 10, 2],                        #熱量換算エネルギー使用量
    ["CALORIFIC_ENERGY_CONSUMPTION_UNIT", 4, 4],                    #熱量換算エネルギー消費原単位
    ["CRUDE_OIL_ENERGY_CONSUMPTION", 10, 2],                        #原油換算エネルギー使用量 
    ["CRUDE_OIL_ENERGY_CONSUMPTION_UNIT", 4, 4],                    #原油換算エネルギー消費原単位  
    ["ELECTRIC_CONSUMPTION_UNIT", 4, 4]                             #電力消費原単位  
]
# 月別法人エネルギー集計情報-日付チェック
monthly_corporate_energy_aggregation_checkdate_list = [
    ["FISCAL_YEAR",4],                                              #年度
    ["YEAR",4]                                                      #対象年  
]
# 月別法人エネルギー集計情報-月チェック
monthly_corporate_energy_aggregation_month_check_list = [
    ["MONTH"]                                                       #対象月
]
# 月別法人エネルギー集計情報-固定長さチェック
monthly_corporate_energy_aggregation_fixed_length_data_check_list = [
    ["CORPORATE_NUMBER",13],                                        #法人番号
    ["BANK_CODE",4]                                                 #金融機関コード
]
# ソリューション計算結果-数値チェック
solution_calculation_results_checknumber_list = [
    ["CONVENTIONAL_FLUORESCENT_LAMP_QUANTITY", 6, 0] ,              # 従来の蛍光灯数
    ["LED_ANNUAL_POWER_CONSUMPTION", 8, 0] ,                        # LEDの年間電力使用量
    ["FLUORESCENT_LAMP_ANNUAL_POWER_CONSUMPTION", 8, 0] ,           # 蛍光灯の年間電力使用量
    ["LED_ANNUAL_POWER_REDUCTION", 5, 1] ,                          # LED導入による電力削減量(年間)
    ["EQUIPMENT_COST", 8, 0] ,                                      # 設備費
    ["CONSTRUCTION_COST", 8, 0] ,                                   # 工事費
    ["IMPLEMENTATION_COST", 8, 0] ,                                 # 導入費用
    ["ANNUAL_EQUIPMENT_REPLACEMENT_COST", 8, 0] ,                   # 年間設備交換費用
    ["PV_INSTALLABLE_AREA", 6, 0] ,                                 # PV設置可能面積
    ["PV_CAPACITY", 6, 0] ,                                         # PV容量
    ["PV_ANNUAL_GENERATION", 8, 0] ,                                # PV発電量(年間)
    ["PV_TOTAL_GENERATION", 8, 0] ,                                 # PV発電量(総計)
    ["PV_OM_ANNUAL_COST", 8, 0] ,                                   # PVのO&M費用(年間)
    ["CONVENTIONAL_RUNNING_COST", 8, 0] ,                           # 従来ランニング費用
    ["AIR_CONDITIONING_LOAD", 6, 0] ,                               # 空調負荷
    ["EQUIPMENT_CAPACITY", 6, 0] ,                                  # 設備容量
    ["COOLING_HIGH_AIRCON_ANNUAL_POWER_USAGE", 8, 0] ,              # 高性能空調年間電力使用量(冷房)
    ["HEATING_HIGH_AIRCON_ANNUAL_POWER_USAGE", 8, 0] ,              # 高性能空調年間電力使用量(暖房)
    ["TOTAL_HIGH_AIRCON_ANNUAL_POWER_USAGE", 8, 0] ,                # 高性能空調年間電力使用量(合計)
    ["COOLING_CONVENTIONAL_AIRCON_ANNUAL_POWER_USAGE", 8, 0] ,      # 従来の電気空調年間電力使用量(冷房)
    ["HEATING_CONVENTIONAL_AIRCON_ANNUAL_POWER_USAGE", 8, 0] ,      # 従来の電気空調の年間電力使用量(暖房)
    ["TOTAL_CONVENTIONAL_AIRCON_ANNUAL_POWER_USAGE", 8, 0] ,        # 従来の電気空調の年間電力使用量(合計)
    ["GAS_USAGE_REFUELING_OTHER", 6, 0] ,                           # 給湯に使用するガス量（その他季)
    ["HOT_WATER_HEAT_LOAD_SEASON", 8, 0] ,                          # 季節n給湯熱負荷
    ["DAY_HOT_WATER_HEAT_LOAD_SEASON", 6, 0] ,                      # 季節n日給湯熱負荷
    ["EHP_REQUIRED_HEATING_CAPACITY_SEASON", 5, 1] ,                # 季節nEHP必要加熱能力
    ["INSTALLED_EQUIPMENT_CAPACITY", 5, 1] ,                        # 導入機器設備容量
    ["DAY_HOT_WATER_VOLUME_SEASON", 6, 0] ,                         # 季節n日給湯量
    ["TIME_AVERAGE_HOT_WATER_VOLUME_SEASON", 6, 0] ,                # 季節n時間平均給湯量
    ["PEAK_HOT_WATER_VOLUME_SEASON", 6, 0] ,                        # 季節nピーク給湯量
    ["POWER_CONSUMPTION_SEASON", 6, 0] ,                            # 季節n電力使用量
    ["HOT_WATER_HEAT_LOAD_OTHER", 8, 0] ,                           # その他季給湯熱負荷
    ["DAY_HOT_WATER_HEAT_LOAD_OTHER", 6, 0] ,                       # その他季日給湯熱負荷  
    ["EHP_REQUIRED_HEATING_CAPACITY_OTHER", 5, 1],                  # その他季EHP必要加熱能力
    ["DAY_HOT_WATER_VOLUME_OTHER", 6, 0] ,                          # その他季日給湯量
    ["TIME_AVERAGE_HOT_WATER_VOLUME_OTHER", 6, 0] ,                 # その他季時間平均給湯量
    ["PEAK_HOT_WATER_VOLUME_OTHER", 6, 0] ,                         # その他季ピーク給湯量
    ["POWER_CONSUMPTION_SEASON_OTHER", 6, 0] ,                      # その他季電力使用量
    ["EHP_POWER_CONSUMPTION", 8, 0] ,                               # EHP電力使用量
    ["REQUIRED_ECO_CUTE_QUANTITY", 6, 0] ,                          # 必要なエコキュート台数
    ["ANNUAL_COST_SAVINGS_ECOCUTE_GAS_REDUCTION", 8, 0] ,           # エコキュートガス削減による費用削減分(年間)
    ["ANNUAL_POWER_INCREASE_ECOCUTE_INSTALLATION", 8, 0]            # エコキュート導入による電力増加分(年間)

]
# ソリューション計算結果-日付チェック
solution_calculation_results_checkdate_list = [
    ["FISCAL_YEAR",4]                                               # 年度
]
# ソリューション計算結果-固定長さチェック
solution_calculation_results_length_data_check_list = [
    ["CORPORATE_NUMBER",13],                                        # 法人番号
    ["BANK_CODE",4]                                                 # 金融機関コード
]
# エネルギー費用-数値チェック
tepco_energy_solution_info_checknumber_list = [
    ["ELECTRIC_USAGE_TARIFFS",8,2],                                 # 電気従量課金単価
    ["CITY_GAS_RATES_SUMMER",8,2],                                  # 都市ガス従量料金(夏季)
    ["CITY_GAS_RATES_OTHER_SEASONS",8,2],                           # 都市ガス従量料金(その他季)
    ["CITY_GAS_RATES_WEIGHTED_AVERAGE",8,2],                        # 都市ガス従量料金(加重平均)
    ["CITY_GAS_RATES_FIFTY",8,2],                                   # 都市ガス従量料金(50m4あたり)
    ["CITY_GAS_RATES_ONE",8,2],                                     # 都市ガス従量料金(1m3あたり)
    ["RENDERABLE_RATIO",1,2],                                       # レンタブル比
    ["LED_PRICE",8,0],                                              # LED電球単価
    ["LED_INSTALLATION_PRICE",6,0],                                 # LED工事単価
    ["LED_ANNUAL_POWER_CONSUMPTION",6,0],                           # LED電球年間消費電力量
    ["LED_RATED_POWER_CONSUMPTION",9,1],                            # LED電球定格消費電力
    ["LED_RATED_LIFETIME",8,0],                                     # LED電球定格寿命
    ["LEGAL_SERVICE_LIFE",6,0],                                     # 法定耐用年数
    ["PRACTICAL_SERVICE_LIFE",9,1],                                 # 実用耐用年数
    ["FLUORESCENT_LAMP_PRICE",6,0],                                 # 電球型蛍光灯単価
    ["ANNUAL_POWER_CONSUMPTION",6,0],                               # 年間消費電力量
    ["FLUORESCENT_LAMP_ANNUAL_POWER_CONSUMPTION",6,0],              # 電球型蛍光灯定格消費電力
    ["FLUORESCENT_LAMP_LIFETIME",8,0],                              # 電球型蛍光灯定格寿命
    ["REQUIRED_LIGHT",10,2],                                        # 必要照明量
    ["FLUORESCENT_LAMP_REPLACEMENT_FREQUENCY",9,1],                 # 電球型蛍光灯交換回数
    ["SUBSIDIE",8,0],                                               # 補助金
    ["ADJUSTMENT_VARIABLE",6,0],                                    # 調整用変数
    ["PV_USABLE_AREA_RATIO",1,2],                                   # PV使用可能面積比率
    ["AREA_TO_POWER_CONVERSION",10,2],                              # 使用可能面積PV設置時の面積kW換算
    ["ANNUAL_GENERATION_PER_CAPACITY",6,0],                         # 設備容量あたりの年間発電量
    ["SELF_CONSUMPTION_RATE",1,2],                                  # 自家消費率
    ["PV_UNIT_PRICE",8,0],                                          # PV単価(工事費含む)
    ["PV_MOUNTING_INSTALLATION_COST",8,0],                          # PV架台・工事費単価
    ["PV_OM_COST_PER_UNIT",8,0],                                    # PVのO&M費用単価
    ["EQUIPMENT_UNIT_PRICE",8,0],                                   # 設備単価
    ["CONSTRUCTION_UNIT_PRICE",8,0],                                # 工事単価
    ["HEAT_LOAD_BASIS_UNIT",9,1],                                   # 熱負荷原単位
    ["INDIVIDUAL_EQUIPMENT_COST",8,0],                              # 高性能空調の機器代金(個別)
    ["CENTRAL_EQUIPMENT_COST",8,0],                                 # 高性能空調の機器代金(セントラル)
    ["INDIVIDUAL_EQUIPMENT_COST_AREA",8,0],                         # 高性能空調の面積当たり機器代金(個別)
    ["CENTRAL_EQUIPMENT_COST_AREA",8,0],                            # 高性能空調の面積当たり機器代金(セントラル)
    ["COOLING_LOAD_RUNTIME,",1,0],                                  # 全負荷相当運転時間（冷房）
    ["HEATING_LOAD_RUNTIME,",10,0],                                 # 全負荷相当運転時間（暖房）
    ["GAS_UNIT_PRICE",10,2],                                        # ガス単価
    ["ECO_CUTE_EXPENSES",8,0],                                      # エコキュート費用
    ["MODEL_EQUIPMENT_CAPACITY_INTERIM",9,1],                       # モデル機器設備容量(中間期)
    ["MODEL_EQUIPMENT_CAPACITY_WINTER",9,1],                        # モデル機器設備容量(冬季)
    ["ENERGY_EFFICIENCY",10,2],                                     # エネルギー効率
    ["CITY_GAS_HIGH_CALORIFIC",9,1],                                # 都市ガス高位発熱量
    ["LPG_GAS_HIGH_CALORIFIC",9,1],                                 # LPGガス高位発熱量
    ["CITY_GAS_LOW_CALORIFIC",9,1],                                 # 都市ガス低位発熱量 
    ["LPG_GAS_LOW_CALORIFIC",9,1],                                  # LPGガス低位発熱量
    ["OPERATING_DAYS_SEASON",10,0],                                 # 季節n稼働日数
    ["OPERATING_DAYS_OTHER",10,0],                                  # その他季稼働日数
    ["HOT_WATER_TEMPERTURE",9,1],                                   # 給湯温度
    ["WATER_SUPPLY_TEMPERTURE_SEASON",9,1],                         # 給水温度(季節n)
    ["WATER_SUPPLY_TEMPERTURE_OTHER",9,1],                          # 給水温度(その他季節加重平均)
    ["EHP_OPERATING_HOURS",9,1],                                    # EHPの1日当たりの稼働時間
    ["HOT_WATER_SYSTEM_EFFICIENCY",1,2],                            # 給湯システムの効率
    ["PEAK_FACTOR",2,1],                                            # ピーク係数
    ["SEVERE_WINTER_COP",2,1],                                      # 厳冬期COP
    ["INTERIM_COP",2,1]                                             # COP

]
# エネルギー費用-日付チェック
tepco_energy_solution_info_checkdate_list = [
    ["FISCAL_YEAR",4]                                               # 年度

]
# エネルギー費用-固定長さチェック
tepco_energy_solution_info_length_data_check_list =[
    ["BANK_CODE",4],                                                # 金融機関コード  
    ["CORPORATE_NUMBER",13]                                         # 法人番号
]


