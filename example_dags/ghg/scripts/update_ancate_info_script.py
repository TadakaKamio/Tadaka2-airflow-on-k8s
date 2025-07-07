import pandas as pd
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.utils import get_current_timestamp
from ghg.sql.ancate_info import (
    INSERT_ANCATE_INFO,
    INSERT_OVERWRITE_ANCATE_INFO_BK,
    SELECT_ANCATE_INFO,
    TRUNCATE_ANCATE_INFO,
)
from ghg.sql.non_fossil_ratio_info_mst import SELECT_NON_FOSSIL_RATIO_INFO_MST

logger = MyAppLog()

# Hive接続初期化
hive_connector = HiveConnector()

# 現在日時
current_timestamp = get_current_timestamp()


@log_writer(logger)
def update_non_fossil_ratio(**kwargs):
    """
    関数名：調査表情報の非化石割合情報を更新

    調査表情報へ電気事業者の非化石割合情報を更新する処理
    処理イメージ：
        ■更新前
        ANCATE_INFO DataFrame:
          ANCATE_ID ELECTRICITY_ENTERPRISE1_COMPANY_NM ELECTRICITY_ENTERPRISE1_MENU_NM  NON_FOSSIL_RATIO1 ELECTRICITY_ENTERPRISE2_COMPANY_NM ELECTRICITY_ENTERPRISE2_MENU_NM  NON_FOSSIL_RATIO2
        0       id1                                  A                           Menu1                NaN                                  A                           Menu2                NaN
        1       id2                                  A                           Menu1                NaN                                  A                           Menu3                NaN
        2       id3                                  A                           Menu3                NaN                                  A                           Menu2                NaN
        3       id4                                  A                           Menu3                NaN                                  A                           Menu4                NaN
        4       id5                                  B                            None                NaN                               None                            None                NaN
        5       id6                               None                            None                NaN                                  B                            None                NaN
        6       id7                                  C                           Menu5                NaN                                  C                           Menu5                NaN
        7       id8                                  D                            None                NaN                               None                            None                NaN
        8       id9                               None                            None                NaN                                  D                            None                NaN
        9      id10                                  E                            None                NaN                                  E                            None                NaN

        NON_FOSSIL_RATIO_INFO_MST DataFrame:
          ELECTRICITY_ENTERPRISE_COMPANY_NM ELECTRICITY_ENTERPRISE_MENU_NM  NON_FOSSIL_RATIO DELETE_FLG INSERT_NAME         INSERT_DATE UPDATE_NAME         UPDATE_DATE
        0                                 A                          Menu1                 5          0      TEPSYS  2024/3/28 13:00:00      TEPSYS  2024/3/28 13:00:00
        1                                 A                          Menu2                10          0      TEPSYS  2024/3/28 13:00:00      TEPSYS  2024/3/28 13:00:00
        2                                 B                           None                 5          0      TEPSYS  2024/3/28 13:00:00      TEPSYS  2024/3/28 13:00:00
        3                                 C                           None                10          0      TEPSYS  2024/3/28 13:00:00      TEPSYS  2024/3/28 13:00:00
        4                                 D                          Menu3                 5          0      TEPSYS  2024/3/28 13:00:00      TEPSYS  2024/3/28 13:00:00

        Updates:
        更新済み：調査表ID：id1に電気事業者名称1の非化石割合「5」へ更新しました。マスタに電気事業者名称：A、メニュー名：Menu1
        更新済み：調査表ID：id2に電気事業者名称1の非化石割合「5」へ更新しました。マスタに電気事業者名称：A、メニュー名：Menu1
        更新済み：調査表ID：id1に電気事業者名称2の非化石割合「10」へ更新しました。マスタに電気事業者名称：A、メニュー名：Menu2
        更新済み：調査表ID：id3に電気事業者名称2の非化石割合「10」へ更新しました。マスタに電気事業者名称：A、メニュー名：Menu2
        更新済み：調査表ID：id5に電気事業者名称1の非化石割合「5」へ更新しました。マスタに電気事業者名称：B、メニュー名：None
        更新済み：調査表ID：id6に電気事業者名称2の非化石割合「5」へ更新しました。マスタに電気事業者名称：B、メニュー名：None

        Errors:
        エラー：調査表ID：id7に電気事業者名称1のメニュー名の記載がある、マスタにメニュー名がない、当該データが更新しないです。※ マスタに電気事業者名称：C
        エラー：調査表ID：id7に電気事業者名称2のメニュー名の記載がある、マスタにメニュー名がない、当該データが更新しないです。※ マスタに電気事業者名称：C
        エラー：調査表ID：id8に電気事業者名称1のメニュー名の記載がない、当該データが更新しないです。※ マスタに電気事業者名称：D、メニュー名：Menu3
        エラー：調査表ID：id9に電気事業者名称2のメニュー名の記載がない、当該データが更新しないです。※ マスタに電気事業者名称：D、メニュー名：Menu3

        ■更新後
        df_ancate_info:
          ANCATE_ID ELECTRICITY_ENTERPRISE1_COMPANY_NM ELECTRICITY_ENTERPRISE1_MENU_NM  NON_FOSSIL_RATIO1 ELECTRICITY_ENTERPRISE2_COMPANY_NM ELECTRICITY_ENTERPRISE2_MENU_NM  NON_FOSSIL_RATIO2
        0       id1                                  A                           Menu1                5.0                                  A                           Menu2               10.0
        1       id2                                  A                           Menu1                5.0                                  A                           Menu3                NaN
        2       id3                                  A                           Menu3                NaN                                  A                           Menu2               10.0
        3       id4                                  A                           Menu3                NaN                                  A                           Menu4                NaN
        4       id5                                  B                            None                5.0                               None                            None                NaN
        5       id6                               None                            None                NaN                                  B                            None                5.0
        6       id7                                  C                           Menu5                NaN                                  C                           Menu5                NaN
        7       id8                                  D                            None                NaN                               None                            None                NaN
        8       id9                               None                            None                NaN                                  D                            None                NaN
        9      id10                                  E                            None                NaN                                  E                            None                NaN

        ■試験用insert文
        INSERT INTO ANCATE_INFO (ANCATE_ID, ELECTRICITY_ENTERPRISE1_COMPANY_NM, ELECTRICITY_ENTERPRISE1_MENU_NM, NON_FOSSIL_RATIO1, ELECTRICITY_ENTERPRISE2_COMPANY_NM, ELECTRICITY_ENTERPRISE2_MENU_NM, NON_FOSSIL_RATIO2)
        VALUES
            ('id1', 'A', 'Menu1', NULL, 'A', 'Menu2', NULL),
            ('id2', 'A', 'Menu1', NULL, 'A', 'Menu3', NULL),
            ('id3', 'A', 'Menu3', NULL, 'A', 'Menu2', NULL),
            ('id4', 'A', 'Menu3', NULL, 'A', 'Menu4', NULL),
            ('id5', 'B', NULL, NULL, NULL, NULL, NULL),
            ('id6', NULL, NULL, NULL, 'B', NULL, NULL),
            ('id7', 'C', 'Menu5', NULL, 'C', 'Menu5', NULL),
            ('id8', 'D', NULL, NULL, NULL, NULL, NULL),
            ('id9', NULL, NULL, NULL, 'D', NULL, NULL),
            ('id10', 'E', NULL, NULL, 'E', NULL, NULL);

        INSERT INTO NON_FOSSIL_RATIO_INFO_MST (ELECTRICITY_ENTERPRISE_COMPANY_NM, ELECTRICITY_ENTERPRISE_MENU_NM, NON_FOSSIL_RATIO, DELETE_FLG, INSERT_NAME, INSERT_DATE, UPDATE_NAME, UPDATE_DATE)
        VALUES
            ('A', 'Menu1', 5, '0', 'TEPSYS', '2024/3/28 13:00:00', 'TEPSYS', '2024/3/28 13:00:00'),
            ('A', 'Menu2', 10, '0', 'TEPSYS', '2024/3/28 13:00:00', 'TEPSYS', '2024/3/28 13:00:00'),
            ('B', NULL, 5, '0', 'TEPSYS', '2024/3/28 13:00:00', 'TEPSYS', '2024/3/28 13:00:00'),
            ('C', NULL, 10, '0', 'TEPSYS', '2024/3/28 13:00:00', 'TEPSYS', '2024/3/28 13:00:00'),
            ('D', 'Menu3', 5, '0', 'TEPSYS', '2024/3/28 13:00:00', 'TEPSYS', '2024/3/28 13:00:00');


    パラメータ:
        なし

    戻り値:
        なし
    """
    try:
        logger.info("処理開始")

        # 試験データ作成
        # df_ancate_info, df_non_fossil_ratio_info_mst = create_test_data()

        # 非化石割合情報マスタを検索
        df_non_fossil_ratio_info_mst = execute_select_non_fossil_ratio_info_mst()

        # 調査表情報を検索
        df_ancate_info = execute_select_ancate_info()

        # 調査表情報の非化石割合情報の更新データ作成
        df_ancate_info, updated_msg_list, error_msg_list = create_update_data(
            df_non_fossil_ratio_info_mst, df_ancate_info
        )

        # システム試験により、事前にバックアップ済みなので、該当処理を不要になる。
        # 調査表情報をバックアップ
        # execute_insert_overwrite_ancate_info_bk()

        # 調査表情報をクリア
        execute_truncate_ancate_info()

        # 調査表情報の非化石割合情報を更新（insert文）
        execute_insert_ancate_info(df_ancate_info)

        for msg in updated_msg_list:
            logger.info(f"更新済み：{msg}")

        for msg in error_msg_list:
            logger.error(f"エラー：{msg}")

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        # 接続を閉じる
        hive_connector.close_connection()
        logger.info("処理終了")


@log_writer(logger)
def create_update_data(df_master, df_ancate_info):
    updated_msg_list = []
    error_msg_list = []

    logger.debug(f"変更前（df_ancate_info）：{df_ancate_info.columns}")
    logger.debug(f"変更前（df_master）：{df_master.columns}")
    df_ancate_info.columns = [col.upper() for col in df_ancate_info.columns]
    df_master.columns = [col.upper() for col in df_master.columns]
    logger.debug(f"変更後（df_ancate_info）：{df_ancate_info.columns}")
    logger.debug(f"変更後（df_master）：{df_master.columns}")

    for _, master_row in df_master.iterrows():
        # 電気事業者名称により、更新レコード整理
        ancate_info_rows = df_ancate_info[
            (
                df_ancate_info["ELECTRICITY_ENTERPRISE1_COMPANY_NM"]
                == master_row["ELECTRICITY_ENTERPRISE_COMPANY_NM"]
            )
            | (
                df_ancate_info["ELECTRICITY_ENTERPRISE2_COMPANY_NM"]
                == master_row["ELECTRICITY_ENTERPRISE_COMPANY_NM"]
            )
        ]

        for index, ancate_info_row in ancate_info_rows.iterrows():
            for i in range(1, 3):
                enterprise_column_nm = f"ELECTRICITY_ENTERPRISE{i}_COMPANY_NM"
                menu_column_nm = f"ELECTRICITY_ENTERPRISE{i}_MENU_NM"
                non_fossil_column_ratio = f"NON_FOSSIL_RATIO{i}"

                # 電気事業者名称が一致する、かつ（メニュー名が一致する、または両方のメニュー名が空）の場合、更新対象にする
                if master_row["ELECTRICITY_ENTERPRISE_COMPANY_NM"] == ancate_info_row[
                    enterprise_column_nm
                ] and (
                    master_row["ELECTRICITY_ENTERPRISE_MENU_NM"]
                    == ancate_info_row[menu_column_nm]
                    or (
                        pd.isna(master_row["ELECTRICITY_ENTERPRISE_MENU_NM"])
                        and pd.isna(ancate_info_row[menu_column_nm])
                    )
                ):
                    df_ancate_info.at[index, non_fossil_column_ratio] = master_row[
                        "NON_FOSSIL_RATIO"
                    ]

                    updated_msg = (
                        f'調査表ID：{ancate_info_row["ANCATE_ID"]}に電気事業者名称{i}の非化石割合「{master_row["NON_FOSSIL_RATIO"]}」へ更新しました。'
                        f'※ マスタに電気事業者名称：{master_row["ELECTRICITY_ENTERPRISE_COMPANY_NM"]}、'
                        f'メニュー名：{master_row["ELECTRICITY_ENTERPRISE_MENU_NM"]}'
                    )

                    updated_msg_list.append(updated_msg)

                # エラー検出
                elif (
                    ancate_info_row[menu_column_nm]
                    and pd.isna(master_row["ELECTRICITY_ENTERPRISE_MENU_NM"])
                    and master_row["ELECTRICITY_ENTERPRISE_COMPANY_NM"]
                    == ancate_info_row[enterprise_column_nm]
                ):
                    error_msg = (
                        f'調査表ID：{ancate_info_row["ANCATE_ID"]}に電気事業者名称{i}のメニュー名の記載がある、マスタにメニュー名がない、当該データが更新しないです。'
                        f'※ マスタに電気事業者名称：{master_row["ELECTRICITY_ENTERPRISE_COMPANY_NM"]}'
                    )

                    error_msg_list.append(error_msg)

                elif (
                    pd.isna(ancate_info_row[menu_column_nm])
                    and master_row["ELECTRICITY_ENTERPRISE_MENU_NM"]
                    and master_row["ELECTRICITY_ENTERPRISE_COMPANY_NM"]
                    == ancate_info_row[enterprise_column_nm]
                ):
                    error_msg = (
                        f'調査表ID：{ancate_info_row["ANCATE_ID"]}に電気事業者名称{i}のメニュー名の記載がない、当該データが更新しないです。'
                        f'※ マスタに電気事業者名称：{master_row["ELECTRICITY_ENTERPRISE_COMPANY_NM"]}、'
                        f'メニュー名：{master_row["ELECTRICITY_ENTERPRISE_MENU_NM"]}'
                    )

                    error_msg_list.append(error_msg)

    print(f"変更前（df_ancate_info）：{df_ancate_info.head()}")
    # NaN値を""に変換
    df_ancate_info = df_ancate_info.fillna("")
    print(f"変更後（df_ancate_info）：{df_ancate_info.head()}")

    return df_ancate_info, updated_msg_list, error_msg_list


@log_writer(logger)
def execute_select_ancate_info():
    """
    関数名：調査表情報の検索

    調査表情報の検索処理

    パラメータ:
        なし

    戻り値:
        調査表情報情報
    """
    select_sql = SELECT_ANCATE_INFO()
    logger.debug(select_sql)

    df = hive_connector.get_dataframe(select_sql)

    if df.empty:
        msg = "テーブル：ancate_infoにデータがありません。"
        logger.error(msg)
        raise Exception(msg)

    return df


@log_writer(logger)
def execute_select_non_fossil_ratio_info_mst():
    """
    関数名：非化石割合情報マスタの検索

    非化石割合情報マスタの検索処理

    パラメータ:
        なし

    戻り値:
        非化石割合情報
    """
    select_sql = SELECT_NON_FOSSIL_RATIO_INFO_MST()
    logger.debug(select_sql)

    df = hive_connector.get_dataframe(select_sql)

    if df.empty:
        msg = "テーブル：non_fossil_ratio_info_mstにデータがありません。"
        logger.error(msg)
        raise Exception(msg)

    return df


@log_writer(logger)
def execute_insert_overwrite_ancate_info_bk():
    """
    関数名：調査表情報をバックアップ

    調査表情報のデータをバックアップする処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    insert_sql = INSERT_OVERWRITE_ANCATE_INFO_BK()
    logger.debug(insert_sql)
    hive_connector.execute_query(insert_sql)


@log_writer(logger)
def execute_truncate_ancate_info():
    """
    関数名：調査表情報のデータをクリア

    調査表情報のデータをクリアする処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    delete_sql = TRUNCATE_ANCATE_INFO()
    logger.debug(delete_sql)
    hive_connector.execute_query(delete_sql)


@log_writer(logger)
def format_record(record):
    formatted_record = []
    for r in record:
        if isinstance(r, str):
            formatted_record.append(f"'{r}'")
        # elif r is None:
        #     formatted_record.append("NULL")
        else:
            formatted_record.append(str(r))
    record_str = "(" + ", ".join(formatted_record) + ")"
    return record_str


@log_writer(logger)
def execute_insert_ancate_info(pandas_df):
    """
    関数名：調査表情報の登録

    「基本情報_登録用」シートのデータは調査表情報テーブルへ登録する処理

    パラメータ:
        pandas_df:pandas DataFrameタイプのデータ

    戻り値:
        なし
    """
    record_list = []
    for index, row in pandas_df.iterrows():
        record = (
            row["ANCATE_ID"],
            row["REPORT_NENDO"],
            row["COMPANY_ID"],
            row["COMPANY_NM"],
            row["BUILDING_ID"],
            row["BUILDING_NM"],
            row["DEPT_NM"],
            row["REP_NM"],
            row["EXTENSION"],
            row["INDUSTRIAL_CLASS_CD"],
            row["POWER_AREA_CD"],
            row["POWER_AREA_NM"],
            row["POSTAL_CD"],
            row["PREFECTURE"],
            row["CITY"],
            row["CHOME_BEYOND"],
            row["COMPANY_OWNER_CD"],
            row["COMPANY_OWNER_NM"],
            row["POWER_DR_JOKO_CD"],
            row["DR_DATE"],
            row["GAS_COMPANY_ID"],
            row["GAS_COMPANY_NM"],
            row["HEAT_COMPANY_ID"],
            row["HEAT_COMPANY_NM"],
            row["LEASABLE_AREA_PG"],
            row["LEASABLE_AREA_HD"],
            row["LEASABLE_AREA_FP"],
            row["LEASABLE_AREA_EP"],
            row["LEASABLE_AREA_RP"],
            row["ANBUN_RATE_PG"],
            row["ANBUN_RATE_HD"],
            row["ANBUN_RATE_FP"],
            row["ANBUN_RATE_EP"],
            row["ANBUN_RATE_RP"],
            row["LAST_YEAR_CRUDE_OIL_EQUIVALENT"],
            row["LAST_YEAR_WATER_AMOUNT"],
            row["DENOMINATOR_TYPE"],
            row["DENOMINATOR_VALUE"],
            row["DAY_NIGHT_POWER_GRASP_FLAG"],
            row["SUBSTATION_EXIST_FLG"],
            row["SUBSTATION_ENERGY_GRASP_FLAG"],
            row["SUBSTATION_WATER_GRASP_FLAG"],
            row["SUBSTATION_FLOOR_AREA"],
            row["BUILDING_FLOOR_AREA"],
            row["SUBSTATION_FLOOR_RATE"],
            row["POWER_GENERATION_AMOUNT"],
            row["POWER_TRANSMISSION_AMOUNT"],
            row["ANCATE_COMMENT"],
            row["ENERGY_AMOUNT_DIFF_REASON"],
            row["WATER_AMOUNT_DIFF_REASON"],
            row["INFLOW_OUTFLOW_DIFF_REASON"],
            row["ENERGY_AMOUNT_RATE"],
            row["WATER_AMOUNT_RATE"],
            row["ELECTRICITY_ENTERPRISE1_COMPANY_ID"],
            row["ELECTRICITY_ENTERPRISE1_COMPANY_NM"],
            row["ELECTRICITY_ENTERPRISE1_MENU_CD"],
            row["ELECTRICITY_ENTERPRISE1_MENU_NM"],
            row["ELECTRICITY_ENTERPRISE1_CO2_CD"],
            row["NON_FOSSIL_RATIO1"],
            row["ELECTRICITY_ENTERPRISE2_COMPANY_ID"],
            row["ELECTRICITY_ENTERPRISE2_COMPANY_NM"],
            row["ELECTRICITY_ENTERPRISE2_MENU_CD"],
            row["ELECTRICITY_ENTERPRISE2_MENU_NM"],
            row["ELECTRICITY_ENTERPRISE2_CO2_CD"],
            row["NON_FOSSIL_RATIO2"],
            row["DELETE_FLG"],
            "TEPSYS",
            current_timestamp,
            "TEPSYS",
            current_timestamp,
        )

        logger.debug(f"■format前のrecord{index + 1}:{record}")
        record_str = format_record(record)
        logger.debug(f"■format後のrecord{index + 1}:{record_str}")
        record_list.append(record_str)

    insert_values = ", ".join(record_list)
    insert_sql = INSERT_ANCATE_INFO(insert_values)
    logger.debug(insert_sql)

    hive_connector.execute_query(insert_sql)


def create_test_data():
    import numpy as np

    # ANCATE_INFO
    results_ancate_info = [
        ["id1", "A", "Menu1", np.nan, "A", "Menu2", np.nan],
        ["id2", "A", "Menu1", np.nan, "A", "Menu3", np.nan],
        ["id3", "A", "Menu3", np.nan, "A", "Menu2", np.nan],
        ["id4", "A", "Menu3", np.nan, "A", "Menu4", np.nan],
        ["id5", "B", None, np.nan, None, None, np.nan],
        ["id6", None, None, np.nan, "B", None, np.nan],
        ["id7", "C", "Menu5", np.nan, "C", "Menu5", np.nan],
        ["id8", "D", None, np.nan, None, None, np.nan],
        ["id9", None, None, np.nan, "D", None, np.nan],
        ["id10", "E", None, np.nan, "E", None, np.nan],
    ]

    columns_ancate_info = [
        "ANCATE_ID",
        "ELECTRICITY_ENTERPRISE1_COMPANY_NM",
        "ELECTRICITY_ENTERPRISE1_MENU_NM",
        "NON_FOSSIL_RATIO1",
        "ELECTRICITY_ENTERPRISE2_COMPANY_NM",
        "ELECTRICITY_ENTERPRISE2_MENU_NM",
        "NON_FOSSIL_RATIO2",
    ]

    df_ancate_info = pd.DataFrame(results_ancate_info, columns=columns_ancate_info)

    # NON_FOSSIL_RATIO_INFO_MST
    results_non_fossil_ratio_info_mst = [
        [
            "A",
            "Menu1",
            5,
            "0",
            "TEPSYS",
            "2024/3/28 13:00:00",
            "TEPSYS",
            "2024/3/28 13:00:00",
        ],
        [
            "A",
            "Menu2",
            10,
            "0",
            "TEPSYS",
            "2024/3/28 13:00:00",
            "TEPSYS",
            "2024/3/28 13:00:00",
        ],
        [
            "B",
            None,
            5,
            "0",
            "TEPSYS",
            "2024/3/28 13:00:00",
            "TEPSYS",
            "2024/3/28 13:00:00",
        ],
        [
            "C",
            None,
            10,
            "0",
            "TEPSYS",
            "2024/3/28 13:00:00",
            "TEPSYS",
            "2024/3/28 13:00:00",
        ],
        [
            "D",
            "Menu3",
            5,
            "0",
            "TEPSYS",
            "2024/3/28 13:00:00",
            "TEPSYS",
            "2024/3/28 13:00:00",
        ],
    ]

    columns_non_fossil_ratio_info_mst = [
        "ELECTRICITY_ENTERPRISE_COMPANY_NM",
        "ELECTRICITY_ENTERPRISE_MENU_NM",
        "NON_FOSSIL_RATIO",
        "DELETE_FLG",
        "INSERT_NAME",
        "INSERT_DATE",
        "UPDATE_NAME",
        "UPDATE_DATE",
    ]

    df_non_fossil_ratio_info_mst = pd.DataFrame(
        results_non_fossil_ratio_info_mst, columns=columns_non_fossil_ratio_info_mst
    )

    logger.debug("ANCATE_INFO DataFrame:")
    logger.debug(df_ancate_info)
    logger.debug("NON_FOSSIL_RATIO_INFO_MST DataFrame:")
    logger.debug(df_non_fossil_ratio_info_mst)

    return df_ancate_info, df_non_fossil_ratio_info_mst


if __name__ == "__main__":
    update_non_fossil_ratio()
