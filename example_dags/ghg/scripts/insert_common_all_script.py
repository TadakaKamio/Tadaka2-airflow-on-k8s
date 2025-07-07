import csv
from datetime import datetime, timedelta

from airflow.models import Variable

import ghg.common.settings as Constants
from ghg.common.hive_connector import HiveConnector
from ghg.common.log import MyAppLog, log_writer
from ghg.common.postgres_connector import connect_postgres
from ghg.common.utils import (
    check_install_package,
    get_current_tokyo_timestamp,
    get_file_from_hadoop,
)

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
def insert_common_mst_info_all(**kwargs):
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

        # today_str = datetime.today().strftime("%Y%m%d")
        today_str = get_current_tokyo_timestamp()

        # FTPからファイルを取得
        all_files = get_file_from_hadoop(base_path, sub_path, key="")

        full_path = {
            fname: fobj for fname, fobj in all_files.items() if today_str in fname
        }

        # 取得したファイルがない場合は処理を中止
        if not full_path:
            logger.error("取得したファイルがありません。処理を中止します。")
            return

        logger.info(f"当日対象ファイル: {list(full_path.keys())}")

        # CSVファイル名とテーブル名のマッピングを取得
        CSV_TO_TABLE_MAPPING = get_csv_to_table_mapping()

        # CSVファイルを処理
        for file_name, file_io in full_path.items():
            # ファイル名を取得
            file_name = file_name.split("/")[-1]

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

            if len(data_rows) >= 3:
                data_rows = data_rows[1:-1]
            else:
                logger.warn(f"{file_name} の行数が少なすぎるためスキップされます。")
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

        if not db_is_empty:
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
    Hiveにデータを登録する関数（BATCH_SIZEで分割処理、appendを使用しない）
    """
    try:
        BATCH_SIZE = 1000

        columns = TABLE_COLUMNS_MAPPING[table_name]
        primary_keys = TABLE_PRIMARY_KEYS[table_name]

        count_sql = f"SELECT COUNT(*) FROM {table_name}"
        result = hive_connector.execute_query(count_sql, Constants.DBoperation.FETCHONE)
        hive_count = result[0] if isinstance(result, tuple) else 0
        db_is_empty = hive_count == 0

        logger.info(
            f"{db_is_empty}の件数を確認しました。 Hive: {table_name} の件数は {hive_count} 件です。"
        )
        if not db_is_empty:
            # INSERT 処理
            logger.info(f"{table_name}のINSERT 処理を開始します。")
            insert_rows = [row for row in data_rows if row[1] == "1"]
            for i in range(0, len(insert_rows), BATCH_SIZE):
                batch = insert_rows[i : i + BATCH_SIZE]

                # 各バッチのVALUESを構築する
                value_list = []
                for row in batch:
                    values = process_values(row, table_name)
                    value_clause = "(" + ", ".join([f"'{v}'" for v in values]) + ")"
                    value_list.append(value_clause)

                # 構造化された一括INSERT SQL
                insert_sql = f"""
                INSERT INTO TABLE {table_name} ({', '.join(columns)})
                VALUES {', '.join(value_list)}
                """
                hive_connector.execute_query(insert_sql)
            logger.info(f"{table_name}のINSERT 処理が完了しました。")

            # UPDATE 処理
            logger.info("UPDATE 処理を開始します。")
            TEMP_UPDATE_TABLE = f"{table_name}_update_tmp"

            # 1. ステータス=2 の更新データを抽出する
            update_rows = [row for row in data_rows if row[1] == "2"]
            if not update_rows:
                logger.info("UPDATE 対象データが存在しません。")
            else:
                logger.info(
                    f"UPDATE 対象は {len(update_rows)} 件、TEMP テーブルを作成します。"
                )

                # 2. 一時テーブルを作成（元のテーブルと同じ構造）
                create_temp_table_sql = f"""
                CREATE TABLE IF NOT EXISTS {TEMP_UPDATE_TABLE} LIKE {table_name}
                """
                hive_connector.execute_query(create_temp_table_sql)
                logger.info(f"CREATE TABLE {TEMP_UPDATE_TABLE} を実行しました。")

                # 3. 古い一時テーブルのデータを削除する
                hive_connector.execute_query(f"TRUNCATE TABLE {TEMP_UPDATE_TABLE}")
                logger.info(f"TRUNCATE TABLE {TEMP_UPDATE_TABLE} を実行しました。")
                # 4. 更新データを一括で一時テーブルに挿入する
                logger.info(f"{TEMP_UPDATE_TABLE} にデータを挿入します。")
                for i in range(0, len(update_rows), BATCH_SIZE):
                    batch = update_rows[i : i + BATCH_SIZE]
                    value_list = []
                    for row in batch:
                        values = process_values(row, table_name)
                        value_clause = "(" + ", ".join([f"'{v}'" for v in values]) + ")"
                        value_list.append(value_clause)

                    insert_sql = f"""
                    INSERT INTO TABLE {TEMP_UPDATE_TABLE} ({', '.join(columns)})
                    VALUES {', '.join(value_list)}
                    """
                    hive_connector.execute_query(insert_sql)
                    logger.info(
                        f"INSERT INTO {TEMP_UPDATE_TABLE} のバッチ挿入を実行しました。"
                    )

                # 5. MERGE INTO を使用して更新対象テーブルを更新する
                logger.info("MERGE INTO を使用して更新処理を実行します。")
                set_clause = ", ".join(
                    [f"{col} = s.{col}" for col in columns if col not in primary_keys]
                )

                join_condition = " AND ".join(
                    [f"t.{pk} = s.{pk}" for pk in primary_keys]
                )
                merge_sql = f"""
                MERGE INTO {table_name} t
                USING {TEMP_UPDATE_TABLE} s
                ON {join_condition}
                WHEN MATCHED THEN UPDATE SET {set_clause}
                """
                hive_connector.execute_query(merge_sql)
                logger.info(
                    f"MERGE INTO による UPDATE「{table_name}」 処理が完了しました。"
                )
            logger.info("UPDATE 処理が完了しました。")

            delete_keys = []
            for row in data_rows:
                if row[1] != "9":
                    continue

                if table_name == "user_info":
                    delete_keys.append((row[2],))  # 主キー：USI_USR_ID
                elif table_name == "organization_info":
                    delete_keys.append((row[2], row[3]))  # 主キー：ORG_CD, ORG_SUB_CD
                elif table_name == "position_info":
                    delete_keys.append((row[2],))  # 主キー：YSI_PST_CD
            logger.info(f"{table_name}のDELETE処理のKEYは {delete_keys} 。")

            # 主キーがある場合だけ削除SQLを実行
            logger.info("DELETE 処理を開始します。")
            if delete_keys:
                if table_name == "user_info":
                    logger.info("user_infoのDELETE 処理を開始します。")
                    ids = "', '".join(key[0] for key in delete_keys)
                    delete_sql = (
                        f"DELETE FROM {table_name} WHERE USI_USR_ID IN ('{ids}')"
                    )
                elif table_name == "organization_info":
                    # 複合主キーは OR 結合
                    logger.info("organization_infoのDELETE 処理を開始します。")
                    conditions = [
                        f"(ORG_CD = '{k[0]}' AND ORG_SUB_CD = '{k[1]}')"
                        for k in delete_keys
                    ]
                    delete_sql = f"DELETE FROM {table_name} WHERE " + " OR ".join(
                        conditions
                    )
                elif table_name == "position_info":
                    logger.info("position_infoのDELETE 処理を開始します。")
                    ids = "', '".join(key[0] for key in delete_keys)
                    delete_sql = (
                        f"DELETE FROM {table_name} WHERE YSI_PST_CD IN ('{ids}')"
                    )

                hive_connector.execute_query(delete_sql)
                logger.info(f"Hive: {table_name} のDELETE処理を実行しました。")
            logger.info("DELETE 処理が完了しました。")

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


def process_values(row, table_name):
    """
    テーブル名に応じて値を処理する関数
    position_infoテーブルの場合、YSI_PST_FLGを追加
    """
    if table_name == "position_info":
        pst_cd = row[2].zfill(4)
        ysi_pst_flg = 1 if pst_cd in TARGET_CODES else 0
        return row[2:4] + [ysi_pst_flg]
    else:
        return row[2:]


def detect_encoding_from_bytes(byte_data):
    import chardet

    """BytesIO のデータからエンコーディングを判定"""
    result = chardet.detect(byte_data)
    encoding = result["encoding"]
    return encoding if encoding else "utf-8"


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
    insert_common_mst_info_all()
