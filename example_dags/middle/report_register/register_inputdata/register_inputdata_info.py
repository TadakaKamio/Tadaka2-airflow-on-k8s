import traceback
import threading
# from airflow.models import Variable
import middle.common.constants_colums as constants
import middle.common.utils as utils
import middle.common.log as log
from middle.common.hql_processor import (
    insert_data, 
    select_data, 
    get_new_id
)
from middle.report_register.common.CommonMasterDataLoader import CommonMasterDataLoader

# ▼▼▼▼▼▼▼▼▼符号定数群▼▼▼▼▼▼▼▼▼
DOT = constants.SpecialChars.DOT.value
BLANK = constants.SpecialChars.BLANK.value
HYPHEN = constants.SpecialChars.HYPHEN.value
SLASH = constants.SpecialChars.LINUX_PATH_DELIMITER.value

# ▼▼▼▼▼▼▼▼▼識別用文字列群▼▼▼▼▼▼▼▼▼
# "事業所"
OFFICE_STRING = constants.StringOfExcelFile.OFFICE.value
# "入力シート"
INPUT_SHEET_STRING = constants.StringOfExcelFile.INPUT_SHEET.value
# "設定"
SETTING_STRING = constants.StringOfExcelFile.SETTING.value

# ▼▼▼▼▼▼▼▼▼共通オブジェクト群▼▼▼▼▼▼▼▼▼
# 設定ファイルからDB情報取得する
json_config = utils.get_json_config()
schema_middle = json_config["database_posgre"]["schema_middle"]
# 実行モード
run_mode = constants.RunMode.DEV.value
# log出力用オブジェクト
logger = log.MiddleAppLog()
# システム操作時タイムスタンプ取得
current_timestamp = utils.get_current_timestamp()
# データ登録処理実行者
creator_name = utils.get_sysuser()
# 発行する建物ID格納用リスト
building_id_list = []
# エラーファイル対象格納リスト
error_filenames = {}

@log.log_writer(logger)
def register_input_data(conn, register_df_dic):
    # TDH登録処理
    try:
        if register_df_dic is None or len(register_df_dic) <= 0 : 
            logger.error("処理する対象データは取得されていないため、処理を中止する。")
            return
        #生データ登録
        basic_df, corporate_df, building_df, energy_df, file_name = register_into_tdh(conn, register_df_dic)
        return basic_df, corporate_df, building_df, energy_df, file_name
        
    except Exception as e:
        logger.error("postegreへの生データ登録が失敗しました。")
        logger.error(traceback.format_exc())
        raise e

@utils.check_time
def register_into_tdh(conn_postgre, register_df_dic):
    '''
    TDH HIVE登録
        入力基本情報
        集計情報
        ファイル処理ステータス
    params:
        conn  接続し
        register_df_dic 登録するデータ格納用辞書
    '''
    global error_filenames
    
    complete_filenames = {}
    # TDH登録処理
    for df_key, file_list in register_df_dic.items():
        basic_df, corporate_df, building_df, energy_df, file_name = \
                None, None, None, None, None
        # 行員向け入力シートと簡易診断入力シートがセットで処理する場合
        for file_info in file_list:
                    
            for input_file_name, dfs in file_info.items():
                complete_filenames[input_file_name] = constants.FileProcessStatus.COMPELETED.value
                # dfsは辞書なので、それぞれのDataFrameに名前を付与する
                if len(dfs) > 1:
                                
                    basic_df = dfs['basic_df']
                    corporate_df = dfs['corporate_df']
                    building_df = dfs['building_df']
                    energy_df = dfs['energy_df']

        #step2追加処理　登録回数処理追加
        registration_seq(conn_postgre, basic_df)

        #postgreへ生データ登録
        insert_input_info_postgre(conn_postgre, basic_df, file_name)
        
        return basic_df, corporate_df, building_df, energy_df, file_name

def get_file_status_df(conn):
    '''
    ファイル処理ステータス取得
    params:
        conn   Hive接続し
    return:
        file_status  ファイル処理ステータス
    '''
    # ファイル処理ステータステーブル追加対応
    result_df = None
    try:
        status_table_name = schema_middle + DOT + constants.BusinessTable.FPSTBL.value
        result_df = select_data(conn, [], None, status_table_name)
    except Exception as e:
        logger.error(f"{status_table_name}のファイルステータス取得処理が失敗しました。")
        raise e
    
    return result_df

def insert_area_info(corporate_df, basic_info_df):
    '''
    エリアID取得とエリア登録
    params:
        data_list   登録データリスト
        column_list カラム情報
    return:
        new_area_id  採番エリアID
    '''
    area_id = BLANK
    area_table_name = schema_middle + DOT + constants.MasterTable.AIMST.value
    try:
        # 銀行コード
        bank_code = corporate_df["BANK_CODE"].iloc[0]
        # 法人番号
        corporate_number = corporate_df["CORPORATE_NUMBER"].iloc[0]
        isexit_area_id = False
        for index, basic_info_row in basic_info_df.iterrows():
            if bank_code == basic_info_row["BANK_CODE"] and \
                corporate_number ==  basic_info_row["CORPORATE_NUMBER"]:
                area_id = basic_info_row["AREA_ID"]
                isexit_area_id = True
                break
        
        if isexit_area_id: 
            # 既に登録済みのエリアIDのであれば、当該ID返す
            return area_id
        else:
            # 登録されていないのであれば、エリアIDを発行してエリアマスタにデータ登録

            # 本社住所を取得する
            # area_info = corporate_df["OFFICE_ADDRESS"].iloc[0]
            area_id = corporate_number + constants.NumberingStartValue.THREE_NUMBER.value

            corporate_df["AREA_ID"] = area_id
            return area_id
    except Exception as e:
        logger.error(f"{area_table_name}のデータ登録が失敗しました。")
        raise e

@utils.check_time
def insert_input_info_postgre(conn, basic_df, file_name):
    '''
    企業カルテ用生データ
    params:
        sheet_df   処理対象シート情報格納DataFrame
        column_list カラム情報
    return:
        energy_dic  エネルギー情報辞書
    '''
    # 入力情報をTDH DWHへ登録する
    input_data_table_name_CAITBL = schema_middle + DOT + constants.BusinessTable.CAITBL.value
    input_data_table_name_CBBITBL = schema_middle + DOT + constants.BusinessTable.CBBITBL.value
    input_data_table_name_BBITBL = schema_middle + DOT + constants.BusinessTable.BBITBL.value
    input_data_table_name_BSITBL = schema_middle + DOT + constants.BusinessTable.BSITBL.value
    input_data_table_name_CBITBL = schema_middle + DOT + constants.BusinessTable.CBITBL.value
    input_data_table_name_RSITBL = schema_middle + DOT + constants.BusinessTable.RSITBL.value

    try:
        #CN対策実施申込情報
        insert_data(conn, basic_df, constants.caitbl_columns, None, input_data_table_name_CAITBL, file_name)
        #レポート格納情報
        basic_df_filtered = basic_df.drop_duplicates(subset=['BANK_CODE', 'BRANCH_CODE','CORPORATE_NUMBER',
                                                               'FISCAL_YEAR','REPORT_TYPE','REGISTRATION_SEQ'], keep='first')
        insert_data(conn, basic_df_filtered, constants.rsitbl_columns, None, input_data_table_name_RSITBL, file_name)

        #契約先金融機関基本情報マスタ検索条件設定
        condition_list_CBBITBL = [
            ['BANK_CODE', basic_df["BANK_CODE"].iloc[0], '=']
        ]
        result_df = select_data(conn, condition_list_CBBITBL, None, input_data_table_name_CBBITBL)
        if result_df.empty:
            df_unique = basic_df.drop_duplicates(subset=constants.mCustomerBankBasicInfo_colums)
            #契約先金融機関基本情報マスタ
            insert_data(conn, df_unique, constants.mCustomerBankBasicInfo_colums, None, input_data_table_name_CBBITBL, file_name)

        #支店マスタ検索条件設定
        condition_list_BBITBL = [
            ['BANK_CODE', basic_df["BANK_CODE"].iloc[0], '='],
            ['BRANCH_CODE', basic_df["BRANCH_CODE"].iloc[0], '=']
        ]
        result_df = select_data(conn, condition_list_BBITBL, None, input_data_table_name_BBITBL)
        if result_df.empty:
            df_unique = basic_df.drop_duplicates(subset=constants.mBankBranchInfo_colums)
            #支店マスタ
            insert_data(conn, df_unique, constants.mBankBranchInfo_colums, None, input_data_table_name_BBITBL, file_name)

        #金融機関担当者マスタ検索条件設定
        condition_list_BSITBL = [
            ['CONTACT_PERSON_NAME_LOCAL_BANK', basic_df["CONTACT_PERSON_NAME_LOCAL_BANK"].iloc[0], '=']
        ]
        result_df = select_data(conn, condition_list_BSITBL, None, input_data_table_name_BSITBL)
        if result_df.empty:
            df_unique = basic_df.drop_duplicates(subset=constants.mBankStaffInfo_colums)
            user_cd = get_next_user_cd(conn, "BANK_USER_SEQ_001")
            df_unique["USER_CD"] = user_cd

            #金融機関担当者マスタ
            insert_data(conn, df_unique, constants.mBankStaffInfo_colums, None, input_data_table_name_BSITBL, file_name)

        #企業基本情報マスタ検索条件設定
        condition_list_CBITBL = [
            ['CORPORATE_NUMBER', basic_df["CORPORATE_NUMBER"].iloc[0], '=']
        ]
        result_df = select_data(conn, condition_list_CBITBL, None, input_data_table_name_CBITBL)  
        if result_df.empty:
            df_unique = basic_df.drop_duplicates(subset=constants.mCorporateBasicInfo_colums)
            #企業基本情報マスタ
            insert_data(conn, df_unique, constants.mCorporateBasicInfo_colums, None, input_data_table_name_CBITBL, file_name)

    except Exception as e:
        logger.error(f"{file_name}のデータ登録が失敗しました。")
        conn.rollback()
        raise e

def get_next_user_cd(db_connection, sequence_id):
    """
    採番テーブル（t_numbering）から次のuser_cdを取得し、カウントを更新する
    :param db_connection: PostgreSQLのDBコネクション
    :param contact_person_name: 採番基準となる担当者名
    :return: 採番されたuser_cd
    """
    cursor = db_connection.cursor()
    
    # 採番テーブルからデータを取得
    select_query = """
        SELECT sequence_id, current_value, increment_step, min_value, max_value, prefix, suffix, padding_length 
        FROM db_corp.t_numbering 
        WHERE sequence_id  = %s 
        FOR UPDATE
    """
    cursor.execute(select_query, (sequence_id,))
    row = cursor.fetchone()

    if row:
        sequence_id, current_value, increment_step, min_value, max_value, prefix, suffix, padding_length = row
        next_value = current_value + increment_step

        if max_value and next_value > max_value:
            raise ValueError("Maximum value exceeded in numbering sequence")

        # user_cdのフォーマット
        user_cd = f"{prefix}{str(next_value).zfill(padding_length)}{suffix or ''}"

        # 採番テーブルを更新
        update_query = """
        UPDATE db_corp.t_numbering 
        SET current_value = %s 
        WHERE sequence_id = %s
        """
        cursor.execute(update_query, (next_value, row[0]))
        db_connection.commit()

        return user_cd

    else:
        raise ValueError(f"Numbering record not found for contact person: {contact_person_name}")


@utils.check_time
def insert_input_info_hive(hive_conn, basic_df, file_name):
    '''
    企業カルテ用生データ
    params:
        sheet_df   処理対象シート情報格納DataFrame
        column_list カラム情報
    return:
        energy_dic  エネルギー情報辞書
    '''

    # 入力情報をTDH DWHへ登録する
    input_data_table_name_CAITBL = schema_middle + DOT + constants.BusinessTable.CAITBL.value
    input_data_table_name_CBBITBL = schema_middle + DOT + constants.BusinessTable.CBBITBL.value
    input_data_table_name_BBITBL = schema_middle + DOT + constants.BusinessTable.BBITBL.value
    input_data_table_name_BSITBL = schema_middle + DOT + constants.BusinessTable.BSITBL.value
    input_data_table_name_CBITBL = schema_middle + DOT + constants.BusinessTable.CBITBL.value

    try:
        #
        partition_values_CAITBL = (basic_df["BANK_CODE"].iloc[0],
                        basic_df["CORPORATE_NUMBER"].iloc[0],
                        basic_df["BUILDING_ID"].iloc[0],
                        basic_df["FISCAL_YEAR"].iloc[0])
        # basic_df["REGISTRATION_NUMBER"].iloc[0],
        # basic_df["AREA_ID"].iloc[0], 
        partiontion_dict_CAITBL = dict(zip(constants.PARTITION_COLUMNS_CAITBL, partition_values_CAITBL))

        #CN対策実施申込情報
        insert_data(hive_conn, basic_df, constants.caitbl_hive_columns, partiontion_dict_CAITBL, input_data_table_name_CAITBL, file_name)

        #契約先金融機関基本情報マスタ検索条件設定
        condition_list_CBBITBL = [
            ['BANK_CODE', basic_df["BANK_CODE"].iloc[0], '=']
        ]
        result_df = select_data(hive_conn, condition_list_CBBITBL, None, input_data_table_name_CBBITBL)
        if result_df.empty:
            df_unique = basic_df.drop_duplicates(subset=constants.mCustomerBankBasicInfo_colums)

            #契約先金融機関基本情報マスタ
            insert_data(hive_conn, df_unique, constants.mCustomerBankBasicInfo_colums, None, input_data_table_name_CBBITBL, file_name)

        #支店マスタ検索条件設定
        condition_list_BBITBL = [
            ['BANK_CODE', basic_df["BANK_CODE"].iloc[0], '='],
            ['BRANCH_CODE', basic_df["BRANCH_CODE"].iloc[0], '=']
        ]
        result_df = select_data(hive_conn, condition_list_BBITBL, None, input_data_table_name_BBITBL)
        if result_df.empty:
            df_unique = basic_df.drop_duplicates(subset=constants.mBankBranchInfo_colums)
            #支店マスタ
            insert_data(hive_conn, df_unique, constants.mBankBranchInfo_colums, None, input_data_table_name_BBITBL, file_name)

        #金融機関担当者マスタ検索条件設定
        condition_list_BSITBL = [
            ['USER_CD', basic_df["USER_CD"].iloc[0], '=']
        ]
        result_df = select_data(hive_conn, condition_list_BSITBL, None, input_data_table_name_BSITBL)
        if result_df.empty:
            df_unique = basic_df.drop_duplicates(subset=constants.mBankStaffInfo_colums)
            #金融機関担当者マスタ
            insert_data(hive_conn, df_unique, constants.mBankStaffInfo_colums, None, input_data_table_name_BSITBL, file_name)

        #企業基本情報マスタ検索条件設定
        condition_list_CBITBL = [
            ['CORPORATE_NUMBER', basic_df["CORPORATE_NUMBER"].iloc[0], '=']
        ]
        result_df = select_data(hive_conn, condition_list_CBITBL, None, input_data_table_name_CBITBL)  
        if result_df.empty:
            df_unique = basic_df.drop_duplicates(subset=constants.mCorporateBasicInfo_colums)
            #企業基本情報マスタ
            insert_data(hive_conn, df_unique, constants.mCorporateBasicInfo_colums, None, input_data_table_name_CBITBL, file_name)

    except Exception as e:
        logger.error(f"{file_name}のHiveデータ登録が失敗しました。")
        hive_conn.rollback() 
        raise e
    
@utils.check_time
def insert_file_status_info(conn, file_dic):
    '''
    ファイルステータス管理登録
    params:
        conn Hive接続し
        file_name ファイル名
    '''
    try:
        insert_file_status_data = []
        for file_name, file_status in file_dic.items():
            row_data = (file_name, None, None, file_status, 
                        f"{current_timestamp}",f"{creator_name}")
            insert_file_status_data.append(row_data)
        # ファイル処理状況テーブルデータ登録
        insert_data(conn, insert_file_status_data, constants.FPSTBL_COLUMNS, None, 
                    schema_middle + DOT + constants.BusinessTable.FPSTBL.value, file_name)
    except Exception as e:
        logger.error(f"データ登録が失敗しました。{e.__traceback__}")
        raise e

def get_mst_data(conn):
    '''
    マスタデータ取得
    params:
        conn Hive接続し
    return:
        jic_mst  業種マスタ
        ec_mst   電力会社排出係数マスタ
    '''
    jic_mst = ec_mst = None

    # masterデータ格納オブジェクト
    master_data = CommonMasterDataLoader(conn)
    # 区分マスタ
    # kbn_mst = master_data.kbnmst_list
    # 業種マスタ
    jic_mst = master_data.jicmst_list
    # 電力会社の排出係数マスタ
    ec_mst = master_data.ecmst_list

    cal_mst = master_data.calmst_list
    
    return jic_mst, ec_mst, cal_mst
    
def registration_seq(conn, basic_df):
    """
    登録回数取得
    """
    #検索条件設定
    condition_list = [
        ['BANK_CODE', basic_df["BANK_CODE"].iloc[0], '='],
        ['BRANCH_CODE', basic_df["BRANCH_CODE"].iloc[0], '='],
        ['CORPORATE_NUMBER', basic_df["CORPORATE_NUMBER"].iloc[0], '='],
        ['FISCAL_YEAR', basic_df["FISCAL_YEAR"].iloc[0], '=']
    ]

    result_df = select_data(conn, condition_list, None, schema_middle + DOT + "T_CN_APPLICATION_INFO")

    insert_registration_seq = None
    if result_df.empty:
        insert_registration_seq = 1
    else:
        insert_registration_seq = result_df["REGISTRATION_SEQ"].max() + 1
    
    # 年度のインデスク取得
    col_index = basic_df.columns.get_loc("FISCAL_YEAR")
    # 登録回数の項目と値の差込
    basic_df.insert(col_index + 1, "REGISTRATION_SEQ", insert_registration_seq)