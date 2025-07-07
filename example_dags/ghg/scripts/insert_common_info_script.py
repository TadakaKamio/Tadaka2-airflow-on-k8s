import csv

from airflow.models import Variable

import ghg.common.settings as Constants
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.postgres_connector import connect_postgres
from ghg.common.utils import check_install_package, get_file_from_hadoop

logger = MyAppLog()

# Hive接続初期化
hive_connector = HiveConnector()

# PostgreSQLのテーブル名とカラム名のマッピング
# テーブル名 -> カラム名
TABLE_COLUMNS_MAPPING = {
    "organization_info": [
        "SSI_TNS_CD",
        "SSI_KSH_CD",
        "SSI_HSH_FLG",
        "SSI_CKJ_SSK_TNS_CD",
        "SSI_CKJ_SSK_KSH_CD",
        "SSI_SIS_KNJ_UNN_NAM",
        "SSI_CO_CD",
        "SSI_CO_NAM",
    ],
    "user_info": [
        "USI_USR_ID",
        "USI_KJN_NO",
        "USI_KNJ_SMI_SEI",
        "USI_KNJ_SMI_MEI",
        "USI_KNA_SMI_SEI",
        "USI_KNA_SMI_MEI",
        "USI_MIL_ADR",
        "USI_JTM_MIL_ADR",
        "USI_GSZ_TNS_CD",
        "USI_GSZ_KSH_CD",
        "USI_GSZ_PST_CD",
        "USI_KNM_FLG",
        "USI_KNM_SUU",
        "USI_KNM_SHZ_CD1",
        "USI_KNM_SHZ_CD2",
        "USI_KNM_SHZ_CD3",
        "USI_KNM_SHZ_CD4",
        "USI_KNM_SHZ_CD5",
        "USI_GNS_CO_CD",
    ],
    "position_info": ["YSI_PST_CD", "YSI_PST_NAM", "YSI_PST_FLG"],
}

# 表 -> 主キー
# 主キーは、更新時にWHERE句で使用される
TABLE_PRIMARY_KEYS = {
    "organization_info": ["SSI_TNS_CD", "SSI_KSH_CD"],
    "user_info": ["USI_USR_ID"],
    "position_info": ["YSI_PST_CD"],
}

# 対象コード
TARGET_CODES = [
    str(code).zfill(4)
    for code in [
        2021,
        2401,
        2701,
        2706,
        3101,
        3111,
        3121,
        3151,
        3601,
        772,
        1404,
        1421,
        605,
        801,
        901,
        1001,
        1006,
        1205,
        1271,
        1701,
        1706,
        1801,
        2001,
        2006,
        2011,
        3102,
        3103,
        3602,
        3603,
        4101,
        903,
        301,
        303,
        401,
        403,
        591,
        705,
        802,
        803,
        902,
        1002,
        1003,
        1302,
        1303,
        1602,
        1603,
        1702,
        1703,
        1751,
        1802,
        1803,
        1851,
        2002,
        2003,
        2012,
        2013,
        2051,
        2102,
        2103,
        2402,
        2403,
        2502,
        2503,
        2702,
        2703,
        2712,
        2713,
        2802,
        2803,
        3001,
    ]
]


@log_writer(logger)
def insert_common_mst_info(**kwargs):
    """
    関数名：マスタデータ登録

    マスタデータへ登録する処理

    パラメータ:
        なし

    戻り値:
        なし
    """
    pg_conn = None
    pg_cursor = None
    try:
        logger.info("処理開始")

        # PostgreSQL 接続
        pg_conn, pg_cursor = connect_postgres()

        # chardetをインストール
        check_install_package(Constants.PackageName.CHARDET.value)

        # FTPのCSVファイルのパスを取得
        base_path = Variable.get("XO_dtap_path")
        sub_path = Variable.get("XO_hdfs_dir")

        # FTPからファイルを取得
        full_path = get_file_from_hadoop(base_path, sub_path, key="")

        # 取得したファイルがない場合は処理を中止
        if not full_path:
            logger.error("取得したファイルがありません。処理を中止します。")
            return

        logger.info(f"取得したファイルのパス: {list(full_path.keys())}")

        # CSVファイル名を取得
        csv_file_name = get_csv_file_name()
        logger.info(f"対象CSVファイル: {csv_file_name}")

        # CSVファイル名とテーブル名のマッピングを取得
        CSV_TO_TABLE_MAPPING = get_csv_to_table_mapping()

        # CSVファイルを処理
        for file_name, file_io in full_path.items():
            # ファイル名を取得
            file_name = file_name.split("/")[-1]

            # 対応するテーブル名がない場合はスキップ
            if file_name not in csv_file_name:
                logger.warn(
                    f"{file_name} は対応するHiveテーブルがないためスキップします。"
                )
                continue

            # --- プレフィックス取得 ---
            prefix = file_name.split("_")[0]

            # 対応するテーブル名を取得
            table_name = CSV_TO_TABLE_MAPPING.get(prefix)

            # 対応するテーブル名がない場合はスキップ
            if not table_name:
                logger.warn(
                    f"{file_name} に対応するテーブルが見つかりません（prefix: {prefix}）。スキップします。"
                )
                continue

            # --- Encoding 判定 ---
            file_io.seek(0)
            encoding = detect_encoding_from_bytes(file_io.read(100000))
            logger.info(f"{file_name} の推定エンコーディング: {encoding}")

            # --- CSV 読込 ---
            file_io.seek(0)
            csv_data = file_io.read().decode(encoding).splitlines()
            reader = csv.reader(csv_data)

            data_rows = list(reader)
            # 空行を除外した有効なデータだけを取得
            data_rows = [row for row in data_rows if any(cell.strip() for cell in row)]

            if not data_rows:
                logger.warn(f"{file_name} に有効なデータがありません。スキップします。")
                continue

            # --- 处理 PostgreSQL ---
            handle_postgresql(pg_cursor, pg_conn, table_name, data_rows)

            # --- 处理 Hive ---
            handle_hive(table_name, data_rows)

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")
        raise e
    finally:
        # 接続を閉じる
        if pg_cursor:
            pg_cursor.close()
        if pg_conn:
            pg_conn.close()
        hive_connector.close_connection()
        logger.info("処理終了")


def handle_postgresql(pg_cursor, pg_conn, table_name, data_rows):
    """
    PostgreSQLにデータを登録する関数
    """
    try:
        # テーブル名とカラム名のマッピングを取得
        columns = TABLE_COLUMNS_MAPPING[table_name]
        primary_keys = TABLE_PRIMARY_KEYS[table_name]

        # DBのレコード数を取得
        pg_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        record_count = pg_cursor.fetchone()[0]
        # DBが空かどうかを判定
        db_is_empty = record_count == 0

        #  DBにレコードが存在しない場合、全件登録を行う
        if db_is_empty:
            logger.info(f"{table_name}：が空のため、全件登録（INSERT）を実行します。")
            # 全件登録
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({','.join(['%s'] * len(columns))})"

            for row in data_rows:
                # position_infoテーブルの場合、YSI_PST_FLGを追加
                if table_name == "position_info":
                    pst_cd = row[2].zfill(4)
                    ysi_pst_flg = 1 if pst_cd in TARGET_CODES else 0
                    values = row[2:4] + [ysi_pst_flg]
                else:
                    values = row[2:]
                pg_cursor.execute(insert_sql, values)

        else:
            # DBにレコードが存在する場合、INSERT/UPDATE/DELETEを行う
            for row in data_rows:
                status = row[1]
                # position_infoテーブルの場合、YSI_PST_FLGを追加
                if table_name == "position_info":
                    pst_cd = row[2].zfill(4)
                    ysi_pst_flg = 1 if pst_cd in TARGET_CODES else 0
                    values = row[2:4] + [ysi_pst_flg]
                else:
                    values = row[2:]

                if status == "1":  # INSERT
                    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({','.join(['%s'] * len(values))})"
                    pg_cursor.execute(insert_sql, values)

                elif status == "2":  # UPDATE
                    set_clause = ", ".join(
                        [f"{col}=%s" for col in columns[len(primary_keys) :]]
                    )
                    where_clause = " AND ".join([f"{pk}=%s" for pk in primary_keys])
                    update_sql = (
                        f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                    )
                    pg_cursor.execute(
                        update_sql,
                        values[len(primary_keys) :] + values[: len(primary_keys)],
                    )

                elif status == "9":  # DELETE
                    where_clause = " AND ".join([f"{pk}=%s" for pk in primary_keys])
                    delete_sql = f"DELETE FROM {table_name} WHERE {where_clause}"
                    pg_cursor.execute(delete_sql, tuple(values[: len(primary_keys)]))

        pg_conn.commit()
        logger.info(f"PostgreSQL: {table_name} のデータ更新成功")

    except Exception as e:
        logger.error(f"PostgreSQL {table_name} 更新中にエラーが発生しました: {e}")
        raise e


def handle_hive(table_name, data_rows):
    """
    Hiveにデータを登録する関数
    """
    try:
        # テーブル名とカラム名のマッピングを取得
        columns = TABLE_COLUMNS_MAPPING[table_name]
        primary_keys = TABLE_PRIMARY_KEYS[table_name]

        # DBのレコード数を取得
        count_sql = f"SELECT COUNT(*) FROM {table_name}"
        result = hive_connector.execute_query(count_sql, Constants.DBoperation.FETCHONE)
        hive_count = result[0] if isinstance(result, tuple) else 0
        db_is_empty = hive_count == 0

        if db_is_empty:
            logger.info(f"{table_name}:が空のため、全件登録（INSERT）を実行します。")

            BATCH_SIZE = 1000
            for i in range(0, len(data_rows), BATCH_SIZE):
                batch = data_rows[i : i + BATCH_SIZE]
                values_clause_list = []

                for row in batch:
                    # position_infoテーブルの場合、YSI_PST_FLGを追加
                    if table_name == "position_info":
                        pst_cd = row[2].zfill(4)
                        ysi_pst_flg = 1 if pst_cd in TARGET_CODES else 0
                        values = row[2:4] + [ysi_pst_flg]
                    else:
                        values = row[2:]
                    quoted_values = ", ".join([f"'{v}'" for v in values])
                    values_clause_list.append(f"({quoted_values})")

                values_clause = ", ".join(values_clause_list)
                insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES {values_clause}"
                hive_connector.execute_query(insert_sql)
            hive_connector.close_connection()
        else:
            for row in data_rows:
                status = row[1]
                # position_infoテーブルの場合、YSI_PST_FLGを追加
                if table_name == "position_info":
                    pst_cd = row[2].zfill(4)
                    ysi_pst_flg = 1 if pst_cd in TARGET_CODES else 0
                    values = row[2:4] + [ysi_pst_flg]
                else:
                    values = row[2:]

                if status == "1":
                    value_clause = ", ".join([f"'{v}'" for v in values])
                    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({value_clause})"
                    hive_connector.execute_query(insert_sql)

                elif status == "2":
                    set_clause = ", ".join(
                        [
                            f"{col}='{val}'"
                            for col, val in zip(
                                columns[len(primary_keys) :],
                                values[len(primary_keys) :],
                            )
                        ]
                    )
                    where_clause = " AND ".join(
                        [
                            f"{pk}='{val}'"
                            for pk, val in zip(
                                primary_keys, values[: len(primary_keys)]
                            )
                        ]
                    )
                    update_sql = (
                        f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
                    )
                    hive_connector.execute_query(update_sql)

                elif status == "9":
                    where_clause = " AND ".join(
                        [
                            f"{pk}='{val}'"
                            for pk, val in zip(
                                primary_keys, values[: len(primary_keys)]
                            )
                        ]
                    )
                    delete_sql = f"DELETE FROM {table_name} WHERE {where_clause}"
                    logger.info(delete_sql)

                    hive_connector.execute_query(delete_sql)

        logger.info(f"Hive: {table_name} のデータ更新成功")

    except Exception as e:
        logger.error(f"Hive {table_name} 更新中にエラーが発生しました: {e}")
        raise e
    finally:
        try:
            hive_connector.close_connection()
            logger.info("Hive connection closed successfully.")
        except Exception as e:
            logger.error(f"Failed to close Hive connection: {e}")


def detect_encoding_from_bytes(byte_data):
    import chardet

    """BytesIO のデータからエンコーディングを判定"""
    result = chardet.detect(byte_data)
    encoding = result["encoding"]
    return encoding if encoding else "utf-8"


def get_csv_file_name():
    """
    CSVファイル名を取得する関数
    """
    return Variable.get("XO_file_name")


def get_csv_to_table_mapping():
    """
    CSVファイル名のプレフィックスとテーブル名のマッピングを取得する関数
    """
    return {
        "Soshiki": "organization_info",
        "User": "user_info",
        "Yakusyoku": "position_info",
    }


if __name__ == "__main__":
    insert_common_mst_info()
