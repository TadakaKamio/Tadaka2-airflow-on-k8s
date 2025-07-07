import re
import numpy as np
import pandas as pd
import os, traceback
from pyhive.exc import DatabaseError
from airflow.models import Variable
from middle.common.postgre_connect import Psycopg2Singleton
import middle.common.utils as utils
import middle.common.log as log
import middle.common.constants_colums as constants
from middle.common.hive_connect import ImpalaSingleton
from middle.common.hql_processor import execute_delete, execute_hive_update, execute_insert, execute_update

# loogerオブジェクト取得
logger = log.MiddleAppLog()

# "." "" "-"
DOT = constants.SpecialChars.DOT.value
BLANK = constants.SpecialChars.BLANK.value
HYPHEN = constants.SpecialChars.HYPHEN.value

# システム操作時タイムスタンプ取得
current_timestamp = utils.get_current_timestamp()

# データ登録処理実行者
creator_name = utils.get_sysuser()

# データベース名取得する
json_config = utils.get_json_config()
schema_commom = json_config["database_posgre"]["schema_commom"]
schema_middle = json_config["database_posgre"]["schema_middle"]

hive_common_user = json_config["hive_common"]["user"]
hive_common_password = json_config["hive_common"]["password"] 

hive_corp_user = json_config["database_hive"]["user"]
hive_corp_password = json_config["database_hive"]["password"] 

# rootパス取得
project_root_path = utils.get_project_root_path()

@log.log_writer(logger)
def insert_public_factor(target_sheets=None, *args, **kwargs):
    """指定された公的係数のシートをDWHへ登録する"""

    # 実行モード取得
    run_mode = os.getenv("MIDDLE_RUN_MODE", constants.RunMode.DEV.value) \
        if os.environ.get("MIDDLE_RUN_MODE") is None else os.environ.get("MIDDLE_RUN_MODE")

    # excelファイル処理用ライブラリopenpyxlをインストール
    utils.install_package("openpyxl")

    logger.info("★★★公的係数の登録処理を開始します★★★")
    # hive接続インスタンス
    hive_common_connect_singleton = common_conn = None
    hive_corp_connect_singleton = corp_conn = None
    postgre_connect_singleton = postgre_conn = None  # postgre接続インスタンス

    if run_mode in ( constants.RunMode.PROD.value, constants.RunMode.S2_PROD.value):
        # postgre connect接続
        postgre_connect_singleton = Psycopg2Singleton()
        # コネクション取得
        postgre_conn = postgre_connect_singleton._connection
        # Hive connect接続
        hive_common_connect_singleton = ImpalaSingleton(hive_common_user, hive_common_password)
        # コネクション取得
        common_conn = hive_common_connect_singleton._connection
        # Hive connect接続
        hive_corp_connect_singleton = ImpalaSingleton(hive_corp_user, hive_corp_password)
        # コネクション取得
        corp_conn = hive_corp_connect_singleton._connection

    # 処理する入力シートファイル一覧取得
    excel_files = None
    if run_mode == constants.RunMode.DEV.value:
        # excel_files = utils.get_files("masterfiles")
        excel_files = [r'C:\Users\msduser\cndx_workspace\esg05\dags\middle\files\masterfiles\EEGS_master.xlsx']
    else:
        base_path = Variable.get("middle_download_put_base_path")
        sub_path = Variable.get("middle_download_put_masterfiles_path")

        # Hadoopから対象ファイルのBytesIOを取得
        excel_files = utils.get_file_from_hadoop(base_path, sub_path, None)

    # ファイル存在チェック
    if (excel_files is None or len(excel_files) == 0):
        logger.info("登録・更新するファイルがないため、処理を中止します。")
        return
    
    # ファイル数分処理を繰り返す読み込み
    # for excel_file in excel_files: # 🔥🔥🔥🔥テスト用
    for file_path, excel_file in excel_files.items():
        logger.debug(f"★処理中ファイル名： {excel_file} ★")

        with pd.ExcelFile(excel_file) as file:
            sheet_names = file.sheet_names

        try:
            if run_mode == constants.RunMode.DEV.value:
                # industy_classification_df.to_csv("industy_classification.csv", index=False)
                # electric_supplier_menu_df.to_csv("electric_supplier_menu.csv", index=False)
                # activity_minor_category_df.to_csv("activity_minor_category.csv", index=False)
                pass
            else:
                industry_sheet_flg = False
                # シート数分を繰り返す
                for sheet_name in sheet_names:
                    # target_sheetsが指定されている場合、シート名が対象シートに含まれていないとスキップ
                    # if target_sheets and sheet_name not in target_sheets:
                    #     logger.info(f"シート {sheet_name} は指定されていないため、スキップします。")
                    #     continue

                    if constants.EEGSMasterSheetName.AMCMST_SHEET_NAME.value == sheet_name:
                        execute_delete(postgre_conn, schema_commom + DOT + constants.MasterTable.AMCMST.value)
                        activity_minor_category_df =  get_activity_minor_category_data(excel_file, sheet_name)
                        # PostgreS登録
                        execute_insert(
                            postgre_conn,
                            activity_minor_category_df,
                            constants.AMCMST_COLUMNS,
                            schema_commom + DOT + constants.MasterTable.AMCMST.value,
                        )

                        execute_hive_update(common_conn, 
                                            schema_commom + DOT + constants.MasterTable.AMCMST.value,
                                            constants.AMCMST_COLUMNS, False, True)
                        # Hive登録
                        execute_insert(
                            common_conn,
                            activity_minor_category_df,
                            constants.AMCMST_COLUMNS,
                            schema_commom + DOT + constants.MasterTable.AMCMST.value,
                        )
                    if constants.EEGSMasterSheetName.MECF_SHEET_NAME.value == sheet_name:
                        execute_delete(postgre_conn, schema_middle + DOT + constants.MasterTable.MECF.value)
                        electric_supplier_menu_df =  get_electric_supplier_menu_data(excel_file, sheet_name)
                        # PostgreS登録
                        execute_insert(
                            postgre_conn,
                            electric_supplier_menu_df,
                            constants.MECF_COLUMNS,
                            schema_middle + DOT + constants.MasterTable.MECF.value,
                        )
                        
                        # execute_update(conn, 
                        #                schema_middle + DOT + constants.MasterTable.MECF.value, 
                        #                {"delete_flg":True},
                        #                {"delete_flg":[False, None]})
                        
                        execute_hive_update(corp_conn, 
                                            schema_middle + DOT + constants.MasterTable.MECF.value,
                                            constants.MECF_COLUMNS, False, True)
                        # Hive登録
                        execute_insert(
                            corp_conn,
                            electric_supplier_menu_df,
                            constants.MECF_COLUMNS,
                            schema_middle + DOT + constants.MasterTable.MECF.value,
                        )
                    if not industry_sheet_flg and sheet_name.startswith(constants.EEGSMasterSheetName.MJSIC_SHEET_NAME.value):
                        industry_sheet_flg = True
                        execute_delete(postgre_conn, schema_commom + DOT + constants.MasterTable.MJSIC.value)
                        industy_classification_df = get_industy_classification_mst(excel_file)
                        # PostgreS登録
                        execute_insert(
                            postgre_conn,
                            industy_classification_df,  
                            constants.MJSIC_COLUMNS,
                            schema_commom + DOT + constants.MasterTable.MJSIC.value
                        )
                        
                        execute_hive_update(common_conn, 
                                            schema_commom + DOT + constants.MasterTable.MJSIC.value,
                                           constants.MJSIC_COLUMNS, False, True)
                        # Hive登録
                        execute_insert(
                            common_conn,
                            industy_classification_df,
                            constants.MJSIC_COLUMNS,
                            schema_commom + DOT + constants.MasterTable.MJSIC.value
                        )

        except DatabaseError as e:
            error_message = traceback.format_exc()
            error_line = str(e.__traceback__.tb_lineno) 
            logger.error(f" DatabaseError occurred at line {error_line}: {error_message}")
            raise e
        
        except Exception as e:
            error_message = traceback.format_exc()
            error_line = str(e.__traceback__.tb_lineno) 
            logger.error(f" Error occurred at line {error_line}: {error_message}")
            raise e

        finally:
            # リソースのクリーンアップ
            # connectionをクローズする
            if hive_common_connect_singleton:
                hive_common_connect_singleton.close_connection()
            if hive_corp_connect_singleton:
                hive_corp_connect_singleton.close_connection()
            if postgre_connect_singleton:
                postgre_connect_singleton.close_connection()

def extract_supplier_name(menu_name):
    """
    メニュー名称から電気事業者名を抽出する。
    「（株）」の後ろにメニューがある場合、それを削除する。
    """
    match = re.search(r"^((?:（株）|\(株\)|[^\(\)（）]+)+)", menu_name)
    if match:
        supplier_name = match.group(1).strip()
        return re.sub(r"[ 　]*メニュー.*$", "", supplier_name)  # 「メニュー〇〇」を削除
    return menu_name

def set_system_column(result_df, schema_name=None):
    """
    システムカラム情報設定
    """
     # excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)
    result_df["START_DATE"] = '20240401'
    result_df["END_DATE"] = None
    if schema_name is not None:
        result_df["CREATION_DATETIME"] = f"{current_timestamp}"
        result_df["CREATE_BY"] = f"{creator_name}"
        result_df["UPDATE_DATETIME"] = None
        result_df["UPDATE_BY"] = None
        result_df["DELETE_FLG"] = None
    else:
        result_df["CREATED_AT"] = f"{current_timestamp}"
        result_df["CREATED_BY"] = f"{creator_name}"
        result_df["UPDATED_AT"] = None
        result_df["UPDATED_BY"] = None
        result_df["DELETE_FLAG"] = None

def get_electric_supplier_menu_data(excel_file, sheet_name):
    """
    電力会社の排出係数マスタデータ取得
    """
    # Excelファイルを読み込む
    df = pd.read_excel(
        excel_file,
        sheet_name= sheet_name,
        skiprows=2
    )
    
    # nanを空文字に変換
    df.fillna(BLANK, inplace=True)
    # '-'を空文字に変換
    df.replace(HYPHEN, BLANK, inplace=True)

    # カラム名を設定
    df.columns = [
        "電気事業者登録番号", "報告年度", "公表回数", 
        "メニュー番号", "メニュー名称", "調整後排出係数", 
        "非化石証書の使用状況", "削除フラグ", "基礎排出係数"
    ]

    # 余計なスペースを削除
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # 削除フラグが 0 のデータのみ対象
    df = df[df["削除フラグ"] == 0]

    # 「【使用不可】」を含む行を除外
    df = df[~df["メニュー名称"].str.contains("【使用不可】", regex=False, na=False)]

    # 各電気事業者ごとに報告年度ごとの最大公表回数を取得
    max_reports_per_year = df.groupby(["電気事業者登録番号", "報告年度"])["公表回数"].max().reset_index()

    # 最大公表回数に一致するデータのみ抽出
    df_latest = df.merge(max_reports_per_year, on=["電気事業者登録番号", "報告年度", "公表回数"])
    
    # 結果を格納する辞書を用意
    selected_coefficients = {}
    menu_names = {}

    # 電気事業者登録番号ごとに処理
    for (business_id, report_year), group in df_latest.groupby(["電気事業者登録番号", "報告年度"]):
        # 「（残差）」を含む行を取得
        residual_row = group[group["メニュー名称"].str.contains("残差", regex=True, na=False)]
        
        if len(group) == 1:
            # 1つのデータしかない場合
            selected_coefficients[(business_id, report_year)] = group.iloc[0]["調整後排出係数"]
            menu_names[(business_id, report_year)] = group.iloc[0]["メニュー名称"]
        elif not residual_row.empty:
            # 「残差」がある場合
            selected_coefficients[(business_id, report_year)] = residual_row.iloc[0]["調整後排出係数"]
            menu_names[(business_id, report_year)] = residual_row.iloc[0]["メニュー名称"]
        else:
            # 「（参考値）」を含む行を取得
            reference_row = group[group["メニュー名称"].str.contains("参考値", regex=True, na=False)]
            if not reference_row.empty:
                selected_coefficients[(business_id, report_year)] = reference_row.iloc[0]["調整後排出係数"]
                menu_names[(business_id, report_year)] = reference_row.iloc[0]["メニュー名称"]
            else:
                # どれも該当しない場合は最初のデータを採用
                selected_coefficients[(business_id, report_year)] = group.iloc[0]["調整後排出係数"]
                menu_names[(business_id, report_year)] = group.iloc[0]["メニュー名称"]

    # タプルキーを展開して DataFrame を作成
    result_df = pd.DataFrame(
        [(key[0], key[1], value) for key, value in selected_coefficients.items()],
        columns=["電気事業者登録番号", "報告年度", "調整後排出係数"]
    )

    # メニュー名称を追加
    result_df["メニュー名称"] = result_df.set_index(["電気事業者登録番号", "報告年度"]).index.map(menu_names)

    # 電気事業者名を取得（extract_supplier_name() 関数が必要）
    result_df["メニュー名称"] = result_df["メニュー名称"].apply(extract_supplier_name)

    # カラム名を英字に変換
    result_df = result_df.rename(columns={
        "電気事業者登録番号": "REGISTRATION_NUMBER",
        "メニュー名称": "ELECTRICITY_SUPPLIER_NAME",
        "報告年度": "FISCAL_YEAR",
        "調整後排出係数": "ADJUSTED_EMISSION_FACTOR"
    })

    # 出力順番を指定
    result_df = result_df[[
        "REGISTRATION_NUMBER",
        "ELECTRICITY_SUPPLIER_NAME",
        "FISCAL_YEAR",
        "ADJUSTED_EMISSION_FACTOR"
    ]]

    # excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)
    set_system_column(result_df, schema_middle)

    # CSVに出力
    result_df.to_csv("electric_supplier_menu.csv", index=False)

    return result_df

def get_activity_minor_category_data(excel_file, sheet_name):
    """
    活動項目小分類（事業者）マスタデータ取得
    """

    # Excelファイルを読み込む
    df = pd.read_excel(
        excel_file,
        sheet_name= sheet_name,
        skiprows=2,
        dtype={"活動項目大分類ID": str, 
               "活動項目中分類ID": str, 
               "活動項目小分類ID": str,
               "表示順": str,
                "補助画面表示区分": "Int64", } # 99.0になってしまうため
    )
    columns_to_fix = ["排出係数（CH4）", "排出係数（N2O）", "排出係数（HFC）", 
                  "排出係数（PFC）", "排出係数（SF6）", "排出係数（NF3）"]
    # 指数表記防ぐため
    df[columns_to_fix] = df[columns_to_fix].applymap(lambda x: f"{x:.10f}" if isinstance(x, float) else x)

    # nanを空文字に変換
    df.fillna(np.nan, inplace=True)
    # '-'を空文字に変換
    df.replace(HYPHEN, BLANK, inplace=True)
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    # カラム名を設定
    df.columns = [
        "報告年度",
        "活動項目大分類ID",
        "活動項目中分類ID",
        "活動項目小分類ID",
        "活動項目小分類名",
        "単位",
        "換算係数",
        "非化石エネルギー転換換算係数",
        "非化石重み付け係数",
        "電気需要最適化換算係数",
        "排出係数（エネ起CO2）",
        "排出係数（非エネ起CO2）",
        "排出係数（CH4）",
        "排出係数（N2O）",
        "排出係数（HFC）",
        "排出係数（PFC）",
        "排出係数（SF6）",
        "排出係数（NF3）",
        "変換値１",
        "変換値２",
        "非エネルギー区分",
        "温対法フラグ",
        "省エネ法フラグ",
        "活動項目選択画面表示フラグ",
        "補助画面表示区分",
        "単位入力可否フラグ",
        "換算係数入力可否フラグ",
        "使用量入力可否フラグ",
        "販売副生入力可否フラグ",
        "購入未利用熱入力可否フラグ",
        "活動量最大値",
        "活動量最小値",
        "活動項目コメント",
        "熱関係補助画面表示フラグ",
        "電気関係補助画面表示フラグ",
        "化石・非化石区分",
        "自家発電（他事業所からの供給）画面表示フラグ",
        "表示順",
        "削除フラグ"
    ]

    # 余計なスペースを削除
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # 削除フラグが 0 のデータのみ対象
    df = df[df["削除フラグ"] == 0]

    # カラム名を英字に変換
    result_df = df.rename(columns={
        "報告年度": "REPORT_YEAR",
        "活動項目大分類ID": "MAJOR_CATEGORY_ID",
        "活動項目中分類ID": "MIDDLE_CATEGORY_ID",
        "活動項目小分類ID": "MINOR_CATEGORY_ID",
        "活動項目小分類名": "MINOR_CATEGORY_NM",
        "単位": "UNIT",
        "換算係数": "CONVERSION_COEF",
        "非化石エネルギー転換換算係数": "NON_FOSSIL_CONV_COEF",
        "非化石重み付け係数": "NON_FOSSIL_WEIGHT_COEF",
        "電気需要最適化換算係数": "ELECTRIC_DEMAND_OPT_COEF",
        "排出係数（エネ起CO2）": "ENERGY_CO2_EMISSION_COEF",
        "排出係数（非エネ起CO2）": "NON_ENERGY_CO2_EMISSION_COEF",
        "排出係数（CH4）": "CH4_EMISSION_COEF",
        "排出係数（N2O）": "N2O_EMISSION_COEF",
        "排出係数（HFC）": "HFC_EMISSION_COEF",
        "排出係数（PFC）": "PFC_EMISSION_COEF",
        "排出係数（SF6）": "SF6_EMISSION_COEF",
        "排出係数（NF3）": "NF3_EMISSION_COEF",
        "変換値１": "CONVERSION_VALUE1",
        "変換値２": "CONVERSION_VALUE2",
        "非エネルギー区分": "NON_ENERGY_KBN",
        "温対法フラグ": "GLOBAL_WARMING_LAW_FLAG",
        "省エネ法フラグ": "ENERGY_EFFICIENCY_LAW_FLAG",
        "活動項目選択画面表示フラグ": "ACTIVITY_ITEM_SCREEN_FLAG",
        "補助画面表示区分": "SUPPORT_SCREEN_KBN",
        "単位入力可否フラグ": "UNIT_INPUT_ENABLED_FLAG",
        "換算係数入力可否フラグ": "CONVERSION_COEF_INPUT_FLAG",
        "使用量入力可否フラグ": "USAGE_INPUT_ENABLED_FLAG",
        "販売副生入力可否フラグ": "BY_PRODUCT_INPUT_ENABLED_FLAG",
        "購入未利用熱入力可否フラグ": "UNUSED_HEAT_INPUT_ENABLED_FLAG",
        "活動量最大値": "ACTIVITY_MAX_LIMIT",
        "活動量最小値": "ACTIVITY_MIN_LIMIT",
        "活動項目コメント": "ACTIVITY_ITEM_COMMENT",
        "熱関係補助画面表示フラグ": "HEAT_SUPPORT_SCREEN_FLAG",
        "電気関係補助画面表示フラグ": "ELECTRICITY_SUPPORT_SCREEN_FLAG",
        "化石・非化石区分": "NON_FOSSIL_KBN",
        "自家発電（他事業所からの供給）画面表示フラグ": "SELF_GENERATION_SCREEN_FLAG",
        "表示順": "DISPLAY_ORDER"
    })
    # MINOR_CATEGORY_NMが「都市ガス」かつCONVERSION_COEFが空（NaN）の場合、40.00を設定
    result_df.loc[
        (result_df["MINOR_CATEGORY_NM"] == "都市ガス") & (result_df["CONVERSION_COEF"].isna()),
        "CONVERSION_COEF"
    ] = 40
    # "削除フラグ" 列を削除
    result_df = result_df.drop(columns=["削除フラグ"])
    # excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)
    set_system_column(result_df)

    # CSVに出力
    # result_df.to_csv("activity_minor_category.csv", index=False)

    return result_df

def get_industy_classification_mst(excel_file):
    """
    日本標準産業分類マスタデータ取得
    """
    # Excelファイルのパス（適宜変更）
    file_path = excel_file

    dtype_mapping = {
        "産業分類大コード": str,
        "産業分類中コード": str,
        "産業分類小コード": str,
        "産業分類細コード": str
    }
    
    # 各シートをデータフレームとして読み込む
    df_large = pd.read_excel(file_path, sheet_name="産業分類大", skiprows=2, dtype=dtype_mapping)
    df_medium = pd.read_excel(file_path, sheet_name="産業分類中", skiprows=2, dtype=dtype_mapping)
    df_small = pd.read_excel(file_path, sheet_name="産業分類小", skiprows=2, dtype=dtype_mapping)
    df_detailed = pd.read_excel(file_path, sheet_name="産業分類細", skiprows=2, dtype=dtype_mapping)

    # 削除フラグが 0 のものだけ対象
    df_large = df_large[df_large["削除フラグ"] == 0].drop(columns=["削除フラグ"])
    df_medium = df_medium[df_medium["削除フラグ"] == 0].drop(columns=["削除フラグ"])
    df_small = df_small[df_small["削除フラグ"] == 0].drop(columns=["削除フラグ"])
    df_detailed = df_detailed[df_detailed["削除フラグ"] == 0].drop(columns=["削除フラグ"])

    # 各データフレームを結合
    df_merged = df_detailed.merge(df_small, on=["産業分類大コード", "産業分類中コード", "産業分類小コード"], how="left") \
                        .merge(df_medium, on=["産業分類大コード", "産業分類中コード"], how="left") \
                        .merge(df_large, on=["産業分類大コード"], how="left")

    df_result = df_merged.rename(columns={
        "産業分類大コード": "DIVISION_CODE",
        "産業分類中コード": "MAJOR_GROUP_CODE",
        "産業分類小コード": "GROUP_CODE",
        "産業分類細コード": "INDUSTRY_CODE",
        "産業分類大名": "DIVISION_NAME",
        "産業分類中名": "MAJOR_GROUP_NAME",
        "産業分類小名": "GROUP_NAME",
        "産業分類細名": "INDUSTRY_NAME"
    })
    
    # 必要なカラムを選択
    df_result = df_result[[
        "DIVISION_CODE", "MAJOR_GROUP_CODE", "GROUP_CODE", "INDUSTRY_CODE",
        "DIVISION_NAME", "MAJOR_GROUP_NAME", "GROUP_NAME", "INDUSTRY_NAME"
    ]]

    # excel上含まれていない情報を設定する (有効開始日,有効終了日,作成日時,作成者,更新日時,更新者,削除フラグ)
    set_system_column(df_result)

    # CSVに出力
    # df_result.to_csv("industy_classification.csv", index=False)

    return df_result
