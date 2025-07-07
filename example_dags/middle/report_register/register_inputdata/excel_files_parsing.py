import os
import re
import middle.common.log as log
import time
import middle.common.utils as utils
import pandas as pd
import middle.common.constants_colums as constants_colums
import traceback
from middle.common.hql_processor import (
    insert_data, 
    select_data, 
    get_new_id
)

# log出力用オブジェクト
logger = log.MiddleAppLog()
json_config = utils.get_json_config()
schema_middle = json_config["database_posgre"]["schema_middle"]

# ▼▼▼▼▼▼▼▼▼符号定数群▼▼▼▼▼▼▼▼▼
DOT = constants_colums.SpecialChars.DOT.value
BLANK = constants_colums.SpecialChars.BLANK.value
HYPHEN = constants_colums.SpecialChars.HYPHEN.value
SLASH = constants_colums.SpecialChars.LINUX_PATH_DELIMITER.value

# ▼▼▼▼▼▼▼▼▼識別用文字列群▼▼▼▼▼▼▼▼▼
# "事業所"
OFFICE_STRING = constants_colums.StringOfExcelFile.OFFICE.value
# "入力シート"
INPUT_SHEET_STRING = constants_colums.StringOfExcelFile.INPUT_SHEET.value
# "設定"
SETTING_STRING = constants_colums.StringOfExcelFile.SETTING.value

# システム操作時タイムスタンプ取得
current_timestamp = utils.get_current_timestamp()
# データ登録処理実行者
# creator_name = utils.get_sysuser()

@log.log_writer(logger)
def parse_excel_file(conn, input_files, user_id):
    print("------------入力シート解析処理開始------------")
    # excelファイル処理用ライブラリopenpyxlをインストール
    utils.install_package('openpyxl')
    # 処理する入力シートファイル一覧取得
    start_time = time.time()
    print(input_files)
    end_time= time.time()
    utils.get_process_time(start_time, end_time, "入力ファイル取得")
    creator_name = get_username(user_id)
    # 性能向上対応：検索処理をループから外出し
    basic_info_df, file_status_df = pd.DataFrame(), pd.DataFrame()
    if conn is not None: 
        basic_info_df = get_basic_info(conn)
        # file_status_df = get_file_status_df(conn)

    register_df_dic = {}
    try:
        #Excelファイル解析
        register_df_dic = file_data_process_main(
            conn, input_files, basic_info_df, creator_name)
        print("------------入力シート解析処理終了------------")
        
        return register_df_dic
    except Exception as e:
        logger.error("ファイルETL処理失敗しました。")
        logger.error(traceback.format_exc())
        raise e

def get_input_files():
    '''
    企業カルテ用生データと集計データ
    params:
        conn
        corporate_df   処理対象シート情報格納DataFrame
        building_df カラム情報
        energy_df
        file_name
    return:
        energy_dic  エネルギー情報辞書
    '''
    # rootパス取得
    project_root_path = utils.get_project_root_path()
    # 入力シートファイル格納フォルダ名取得する
    target_folder = os.path.join(project_root_path, json_config["filesDir"]["inputfiles"])
    # osがwindowsの場合、Windowsのパスdelimiterに変換する
    if os.name != 'posix': 
        target_folder = target_folder.replace(constants_colums.SpecialChars.LINUX_PATH_DELIMITER.value,
                            constants_colums.SpecialChars.WINDOWS_PATH_DELIMITER.value)
    
    # # files/inputfiles配下各銀行の入力シートファイルを取得する
    excel_files = []
    # file_path = r"C:\step2\testdata\行員向け入力シート.xlsx"  # パスはraw文字列で指定すると便利
    for root, dirs, files in os.walk(target_folder):
        # 除外するフォルダ
        dirs[:] = [d for d in dirs if d not in ["processed_files", "error_files"]]
        for file in files:
            # ファイルのフルパスを取得します
            file_path = os.path.join(root, file)
            # ファイルのフルパスをリストに追加します
            if file.endswith((constants_colums.ExcelExtension.XLS.value,
                                constants_colums.ExcelExtension.XLSM.value,
                                constants_colums.ExcelExtension.XLSX.value)):
                excel_files.append(file_path)
    if excel_files is None or len(excel_files) == 0:
        logger.info("処理する入力シートファイルが存在しません。")
        raise Exception("処理する入力シートファイルが存在しません。")
    excel_files.append(file_path)
    return excel_files

def get_basic_info(conn):
    '''
    基本情報テーブルデータ取得
    params:
        conn Hive接続し
    return:
        basic_info_df  基本情報テーブルデータ
    '''
    try:
        inputinfo_table_name = schema_middle + DOT + constants_colums.BusinessTable.CAITBL.value
        basic_info_df = select_data(conn, [], None, inputinfo_table_name)
        return basic_info_df
    except Exception as e:
        logger.error(traceback.format_exc())
        raise e

@utils.check_time
def file_data_process_main(conn, input_files, basic_info_df, creator_name):
    global error_filenames
    # セットになる行員向け入力シートと簡易診断入力シートを管理する辞書
    register_df_dic = {}

    # 入力シートファイル数分の処理を繰り返す
    for input_file_path, file_io in input_files.items(): 
    # for input_file_path in input_files: # TODO 🔥🔥🔥🔥🔥 テスト用

        # 入力情報格納用DataFrame作成
        corporate_df = pd.DataFrame(columns=constants_colums.corporate_column)
        building_df = pd.DataFrame(columns=constants_colums.building_column)
        energy_df = pd.DataFrame(columns=constants_colums.energy_column)
        # 事業所数
        number_offices = None
        #ファイル名取得（拡張し含む）
        file_name, file_extension = os.path.splitext(os.path.basename(input_file_path))
        input_file_name = file_name + file_extension

        # Hive登録時用辞書のkeyを構築する        
        df_key = get_register_df_key(input_file_path, input_file_name)
        
        logger.info(f"★処理対象ファイル名：{input_file_name}")
        
        # file_io = input_file_path # TODO 🔥🔥🔥🔥🔥テスト用 
        file_df = pd.ExcelFile(file_io) 
        # 処理対象シート名取得
        all_sheet_names = [sheet_name for sheet_name in (file_df.sheet_names) 
                            if INPUT_SHEET_STRING in sheet_name   # 記入シート
                            or sheet_name.startswith(OFFICE_STRING)] # 事業所シート

        financialYear = None
        building_id_counter = 0
        # 相関チェック項目
        correlation_check_values = {}
        # 発行する建物ID格納用リスト
        building_id_list = []

        for sheet_name in all_sheet_names:
            # 記入シート、事業所シートと設定シート以外はスキップする
            if INPUT_SHEET_STRING not in sheet_name  and \
                not sheet_name.startswith(OFFICE_STRING) and \
                sheet_name != SETTING_STRING: continue
            
            # DataFrame加工処理
            sheet_df, value_df = preprocess_sheet_df(file_io, sheet_name)
            
            # 必須チェック
            try:
                correlation_check_values = check_sheet(sheet_name, value_df, correlation_check_values)
            except Exception as e:
                logger.error(f"必須項目は未入力となっています。{traceback.format_exc()}")
                break
            
            # 相関チェック
            try:
                check_correlation_items(correlation_check_values)
            except Exception as e:
                logger.error(traceback.format_exc())
                break

            if INPUT_SHEET_STRING in sheet_name : 
                # 「記入シート」の情報の場合
                
                # 登録用df_keyに年度がない場合、記入シートの対象年度をくっ付ける
                match = re.search(r'_(\d{4})_', input_file_name)
                financialYear = value_df['FISCAL_YEAR'].iloc[0]
                
                if not match:
                    df_key = df_key + financialYear
                else:
                    df_key = re.sub(r'_(\d{4})_', f'_{financialYear}_', df_key)
                
                # 記入シートデータ格納用DF設定
                try:
                    corporate_df = set_corporate_df(value_df, corporate_df)
                    number_offices = int(corporate_df['NUMBER_OFFICES'])

                except Exception as e:
                    logger.error(traceback.format_exc())
                    break

            if sheet_name.startswith(OFFICE_STRING):

                number_offices -=1 #当シートカウント

                #最大事業所数以外のシート情報読まない
                if number_offices < 0:
                    continue

                # 事業所シートの場合
                building_id_counter += 1
                
                try:
                    # 事業所シートデータ格納用DF設定
                    building_df, energy_df = set_building_energy_df(
                        conn, sheet_df, value_df, corporate_df, building_df, energy_df,
                        basic_info_df, corporate_df['FISCAL_YEAR'].iloc[0], 
                        corporate_df['AREA_ID'].iloc[0], building_id_counter, building_id_list, creator_name)
                except Exception as e:
                    logger.error(traceback.format_exc())
                    break

        corporate_repeated_df = pd.concat([corporate_df] * len(building_df), ignore_index=True)
        # basic_df = pd.concat([corporate_repeated_df, building_df, setting_df], axis=1) # 列結合
        basic_df = pd.concat([corporate_repeated_df, building_df], axis=1) # 列結合
        #入力シート以外の情報設定
        basic_df = basic_df.assign(FILE_ID = None, REPORT_LOCATION = None, STATUS = '0', REPORT_TYPE = '1',CREATION_DATETIME=current_timestamp, CREATOR=creator_name,  
                                   UPDATE_DATETIME = None, UPDATEOR = None, DELETE_FLG = False,START_DATE = utils.get_current_date(), END_DATE = '99991231')

        # 行員向け入力シートの入力情報
        karte_dic_value = {input_file_name: {
            'basic_df':basic_df,'corporate_df':corporate_df, 'building_df':building_df, 'energy_df':energy_df}}
        # 辞書にキーが存在するかどうかを確認
        if df_key in register_df_dic:
            # 既存の値に新しい値を追加
            register_df_dic[df_key].append(karte_dic_value)
        else:
            # 新しいキーに対して値を設定
            register_df_dic[df_key] = [karte_dic_value]
        
    return register_df_dic

def get_register_df_key(input_file_path, input_file_name):
    # ファイル名からスラッシュで区切って主キー要素を取得
    global SLASH
    if os.name != 'posix': 
        SLASH = constants_colums.SpecialChars.WINDOWS_PATH_DELIMITER.value
        
    path_parts = input_file_path.split(SLASH)
    bank_nm = company_nm = filename_fiscal_year = BLANK
    if len(path_parts) > 5:
        bank_nm = path_parts[-3]
        company_nm = path_parts[-2]
    
    # ファイル名から年度を抽出
    match = re.search(r'_(\d{4})_', input_file_name)
    if match:
        filename_fiscal_year = match.group(1)
    
    df_key = bank_nm + HYPHEN + company_nm + HYPHEN + filename_fiscal_year

    return df_key

def preprocess_sheet_df(file_path,sheet_name):
    '''
    入力シート(Excelファイル)の各シートごと
    のデータを整形済みのDataFrameに設定する
    params:
        file_path  入力シートファイルパス
        sheet_name エクセルファイル上シート名
    return:
        sheet_df 全体DF
        value_df データDF
    '''

    # Excelファイル読み込み
    sheet_df = pd.read_excel(file_path,sheet_name)
    # 空白文字を取り除く
    utils.delete_nan_df(sheet_df)
    # 最後の行を捨てる
    sheet_df.drop(sheet_df.index[-1])
    # 日本語列名を物理名へ変換する
    sheet_df.replace(constants_colums.convert_mapping, inplace=True)
    # nanを空文字に変換 
    sheet_df.fillna(BLANK, inplace=True)
    # hyphenを空文字に変換 
    sheet_df.replace(HYPHEN, BLANK, inplace=True)

    # 6列目の値を列名として抽出　
    sheet_column_list = sheet_df.iloc[:, 8].tolist()
    # 8~15列の値を値として抽出
    sheet_value_data_list = sheet_df.iloc[:, 10:11].fillna(BLANK) \
        .apply(lambda row: BLANK.join(map(str, row)), axis=1).tolist()
    # 新たなDataFrame作成、重複列削除
    value_df = pd.DataFrame([sheet_value_data_list],columns = sheet_column_list) \
        .loc[:,~pd.DataFrame([sheet_value_data_list],columns = sheet_column_list).columns.duplicated()].copy()

    return sheet_df,value_df

def check_sheet(sheet_name, value_df, correlation_check_values):
    '''
    シート毎チェック
    params:
        sheet_name チェック対象シート
        value_df 対象シートデータ格納用DF
    '''
    # 必須チェック項目一覧（シート別：事業所シート）
    required_columns = None
    if INPUT_SHEET_STRING in sheet_name: 
        required_columns = constants_colums.CORPORATE_REQUIRED_COLUMNS
    elif sheet_name.startswith(OFFICE_STRING):
        required_columns = constants_colums.BUILDING_REQUIRED_COLUMNS

    if required_columns is not None:
        # バリデーションチェック（必須チェック)
        correlation_check_values = check_required_items(value_df, required_columns, correlation_check_values)
    
    return correlation_check_values

def check_required_items(df, required_columns, correlation_check_values):
    '''
    シート毎チェック
    params:
        df 対象シートデータ格納用DF
        required_columns 必須チェック項目配列
    '''
     # リスト内の各項目を検証する
    for column in required_columns:
        for index, rowdata in df.iterrows():
            if column in constants_colums.NEITHER_REQUIRED_COLUMNS:
                correlation_check_values[column] = rowdata[column]
                break 
            if not rowdata[column]:
                raise ValueError(f"空の項目{column}が検出されました。")
    
    return correlation_check_values

def check_correlation_items(correlation_check_values):
    '''
    シート毎チェック
    params:
        df 対象シートデータ格納用DF
        required_columns 必須チェック項目配列
    '''
    if correlation_check_values is None or \
        len(correlation_check_values) < 3: return
    
    # 相関チェック
    company_num, ep_store_num, ep_user_num = BLANK, BLANK, BLANK
    for column, cell_value in correlation_check_values.items():
        if "CORPORATE_NUMBER" == column: company_num = cell_value
        if "EP_STORE_NUMBER" == column: ep_store_num = cell_value
        if "CUSTOMER_NUMBER_EP" == column: ep_user_num = cell_value
    
    if company_num != BLANK or (
        ep_store_num != BLANK and ep_user_num != BLANK):pass
    else:
        raise ValueError(f"法人番号もしくはEPお客さま番号のどれかを入力してください。")
    
def set_corporate_df(value_df, corporate_df):
    
    #業種名称(大分類、中分類)情報取得
    value_df = value_df.assign(INDUSTRY_BROAD_CATEGORIZATION_NAME = value_df["INDUSTRY_BROAD_CATEGORIZATION"].iloc[0].split(constants_colums.SpecialChars.COLON.value)[1],
                               INDUSTRY_INTERMEDIATE_CLASSIFICATION_NAME = value_df["INDUSTRY_INTERMEDIATE_CLASSIFICATION"].iloc[0].split(constants_colums.SpecialChars.COLON.value)[1])
    #地銀ユーザーコード採番
    value_df = value_df.assign(USER_CD = '0001')

    # `value_df`に業種コード設定
    value_df["INDUSTRY_BROAD_CATEGORIZATION"] = value_df["INDUSTRY_BROAD_CATEGORIZATION"].iloc[0].split(constants_colums.SpecialChars.COLON.value)[0]
    value_df["INDUSTRY_INTERMEDIATE_CLASSIFICATION"] = value_df["INDUSTRY_INTERMEDIATE_CLASSIFICATION"].iloc[0].split(constants_colums.SpecialChars.COLON.value)[0]

    # 期末を年月までの6桁の日付文字列にする
    value_df["END_PERIOD"].iloc[0] = value_df["END_PERIOD"].iloc[0][:7].replace(HYPHEN, BLANK)
    
    # 記入シートDataFrame構築
    corporate_df = pd.concat([corporate_df, value_df],join="inner",ignore_index=True)

    company_code = value_df["CORPORATE_NUMBER"].iloc[0]
    
    #企業はエリアIDとする
    area_id = company_code + constants_colums.NumberingStartValue.THREE_NUMBER.value
    corporate_df["AREA_ID"] = area_id

    return corporate_df

def set_building_energy_df(conn, sheet_df, value_df, corporate_df, building_df, energy_df,
                    basic_info_df, financialYear, area_id, building_id_counter, building_id_list, creator_name):

    # 建物ID取得
    building_id = area_id + constants_colums.NumberingStartValue.THREE_NUMBER.value
    if conn is not None:
        building_id = get_building_id(value_df, corporate_df, basic_info_df, building_id_counter, building_id_list)
    value_df["BUILDING_ID"] = building_id

    building_df = pd.concat([building_df, value_df],join="inner",ignore_index=True)

    # エネルギー情報格納DF設定
    energy_df = set_energy_df_data(sheet_df, value_df, energy_df, financialYear)

    area_table_name = schema_middle + DOT + constants_colums.MasterTable.AIMST.value

    #エリアマスタ検索条件設定
    condition_list_MITBL = [
        ['CORPORATE_NUMBER', corporate_df["CORPORATE_NUMBER"].iloc[0], '='],
        ['AREA_NAME', building_df["AREA_INFORMATION"].iloc[0], '='],
        ['BUILDING_NAME', building_df["BUILDING_NAME"].iloc[0], '=']
    ]
    result_df = select_data(conn, condition_list_MITBL, None, schema_middle + DOT + constants_colums.MasterTable.AIMST.value)  
    if result_df.empty:
        # エリアマスタ登録するデータ配列
        insert_area_data =[(area_id, area_id, corporate_df["CORPORATE_NUMBER"].iloc[0], building_id, building_df["AREA_INFORMATION"].iloc[0],
                            corporate_df["CORPORATE_NAME"].iloc[0], building_df["BUILDING_NAME"].iloc[0], f"{current_timestamp}",f"{creator_name}", None, None, False)]
        
        insert_data(conn, insert_area_data, constants_colums.AIMST_COLUMNS, None, area_table_name, None)

    return building_df, energy_df

def get_building_id(sheet_df, corporate_df, basic_info_df, building_id_counter, building_id_list):
    '''
    建物ID取得
    params:
        sheet_df  
        corporate_df 
        basic_info_df 
    return:
        building_id  建物ID
    '''
    building_id = BLANK

    # 銀行コード
    bank_code = corporate_df["BANK_CODE"].iloc[0]
    # 法人番号
    corporate_number = corporate_df["CORPORATE_NUMBER"].iloc[0]
    # エリアID
    area_id = corporate_df["AREA_ID"].iloc[0]
    # 事業所名
    building_name = sheet_df["BUILDING_NAME"].iloc[0]

    filtered_rows = basic_info_df[
        (basic_info_df['BANK_CODE'] == bank_code) & 
        (basic_info_df['CORPORATE_NUMBER'] == corporate_number) & 
        (basic_info_df['AREA_ID'] == area_id)
    ]

    if filtered_rows is not None and len(filtered_rows) > 0:
        max_building_id = filtered_rows['BUILDING_ID'].max()
        isexist_building_name = False
        for index, basic_info_row in filtered_rows.iterrows():
            if  building_name == basic_info_row["BUILDING_NAME"]:
                building_id = basic_info_row["BUILDING_ID"]
                isexist_building_name = True
                return building_id
            
        if not isexist_building_name:        
            if len(building_id_list) == 0:
                # 自動採番処理
                building_id = get_new_id(max_building_id)
                building_id_list.append(building_id)
            else:
                # building_id_listを整数に変換
                building_id_list_int = [int(bid) for bid in building_id_list]

                # 最大値を取得
                maxint_building_id = max(building_id_list_int)
                building_id = get_new_id(str(maxint_building_id))
                building_id_list.append(building_id)
            
            return building_id
    else:
        building_id = area_id + str(building_id_counter).zfill(3)
        return building_id

def set_energy_df_data(sheet_df, value_df, energy_df, financialYear):
    '''
    エネルギー情報を格納する辞書を作成する
    params:
        sheet_df   処理対象シート情報格納DataFrame
        column_list カラム情報
    return:
        energy_dic  エネルギー情報辞書
    '''
    # エネルギー辞書作成
    energy_dic = {key: [] for key in constants_colums.energy_column}
    #隠されている列排除
    sheet_df = sheet_df.iloc[:,4:]
    #print (pd.DataFrame(sheet_df))
    # エネルギー情報処理開始
    energy_row = sheet_df[sheet_df.iloc[:, 2].str.contains(constants_colums.StringOfExcelFile.ENERGY_INFO.value)].index.values[0]
    # エネルギー使用情報後のデータ
    energy_value_df = sheet_df.loc[energy_row:]
    #使っていないエネルギー排除
    energy_value_df = energy_value_df[energy_value_df.iloc[:,22] != 0]
    # 入力シートから年月取得
    energyDateList = energy_value_df.iloc[0, 10:22].tolist()
    # 入力シートからエネルギー名称取得
    energyNameDF = energy_value_df.iloc[1:, 4]

    for value in energyNameDF.items():
        for dateValue in energyDateList:
            energy_value = sheet_df.iloc[
                sheet_df[sheet_df.iloc[:, 4] == value[1]].index.values[0], 
                sheet_df.iloc[energy_row].tolist().index(dateValue)]
            # if energy_value != 0 and pd.notna(energy_value) :
            energy_dic['AREA_INFORMATION'].append(value_df['AREA_INFORMATION'].iloc[0])
            energy_dic['BUILDING_ID'].append(value_df['BUILDING_ID'].iloc[0])
            energy_dic['BUILDING_NAME'].append(value_df['BUILDING_NAME'].iloc[0])
            energy_dic['ENERGY_CODE'].append(None),
            energy_dic['CATEGORY'].append(None),
            energy_dic['ENERGY_NAME'].append(value[1])
            energy_dic['ENERGY_NAME_JP'].append(constants_colums.energy_name_jp_map.get(value[1]))
            energy_dic['YEAR'].append(dateValue.year)
            energy_dic['MONTH'].append(dateValue.month)
            energy_dic['FISCAL_YEAR'].append(financialYear)
            energy_dic['ENERGY_QUANTITY'].append(energy_value)
    # エネルギー情報DataFrame作成
    energy_df = pd.concat([energy_df, pd.DataFrame(energy_dic)],join="inner",ignore_index=True)
    return energy_df.fillna(0)

def get_username(user_id):
    '''ユーザーネーム取得'''
    from middle.report_register.register_inputdata.common_main import master_data

    mumst = pd.read_json(master_data[constants_colums.MasterTable.MUMST.value]) #ユーザー情報取得
    #定義名称は大文字にする
    mumst.columns = mumst.columns.str.upper()
    mumst_sub = mumst[mumst['USER_MAIL'] == str(user_id)]

    return mumst_sub['USER_NAME'].iloc[0]