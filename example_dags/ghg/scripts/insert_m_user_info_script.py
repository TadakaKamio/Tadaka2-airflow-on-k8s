import csv
from datetime import datetime

from airflow.models import Variable

import ghg.common.settings as Constants
from ghg.common.log import MyAppLog, log_writer
from ghg.common.postgres_connector import connect_postgres
from ghg.common.utils import (
    check_install_package,
    get_current_tokyo_timestamp,
    get_current_tokyo_timestamp2,
    get_file_from_hadoop,
)

logger = MyAppLog()


@log_writer(logger)
def insert_m_user_info(**kwargs):
    """
    関数名：マスタデータ登録
    マスタデータへ登録する処理
    """
    pg_conn = None
    pg_cursor = None
    try:
        logger.info("処理開始")

        # 現在日時
        current_timestamp = get_current_tokyo_timestamp2()

        # PostgreSQL 接続
        pg_conn, pg_cursor = connect_postgres()
        check_install_package(Constants.PackageName.CHARDET.value)

        # HDFSからファイルを取得
        base_path = Variable.get("XO_dtap_path")
        sub_path = Variable.get("XO_hdfs_dir")

        # logger.info(f"取得するHDFSパス: {base_path}/{sub_path}")
        full_path = get_file_from_hadoop(base_path, sub_path, key="")

        if not full_path:
            logger.error("取得したファイルがありません。処理を中止します。")
            return

        logger.info(f"取得したファイルのパス: {list(full_path.keys())}")

        # CSVファイル名のプレフィックスとテーブル名のマッピングを取得
        CSV_TO_TABLE_MAPPING = get_csv_to_table_mapping()

        # CSVファイルをループして処理
        for file_name, file_io in full_path.items():
            file_name = file_name.split("/")[-1]

            # 対象ファイル名がマッピングに存在しない場合はスキップ
            # today = datetime.today().strftime("%Y%m%d")  # 例：20250528
            today = get_current_tokyo_timestamp()
            logger.info(f"当日の日付: {today}")
            # ファイル名のプレフィックスを取得
            target_prefix = f"User_Dif_{today}"

            if not file_name.startswith(target_prefix):
                logger.warn(f"{file_name} は対象外ファイルのためスキップします。")
                continue

            # プレフィックスを取得してテーブル名を決定
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

            # データ行が空の場合はスキップ
            if not data_rows:
                logger.warn(f"{file_name} にデータがありません。スキップします。")
                continue

            # -------- m_user 専用処理 -----------
            if table_name == "user_info":
                for row in data_rows:
                    try:

                        if len(row) < 21:
                            row.extend([""] * (21 - len(row)))
                            logger.warn(
                                f"行データが21列に満たない、現在の行のデータは: {row}"
                            )

                        # データのステータスを取得
                        # ステータスは1:新規登録、2:更新、9:削除
                        status = row[1].strip()
                        # csvファイルのuser_idは2列目にあるため、インデックスは2

                        user_id = row[2].strip()
                        # csvファイルのstaff_nameは4列目と5列目にあるため、インデックスは4, 5

                        staff_name = (
                            f"{row[4].strip()}　{row[5].strip()}"  # 全角スペース
                        )

                        # csvファイルのmail_addressは9列目にあるため、インデックスは9
                        mail_address = row[9].strip() if row[9].strip() else ""

                        # csvファイルのrole_codeは20列目にあるため、インデックスは20
                        role_code = row[20].strip() if row[20].strip() else ""

                        # role_codeが空の場合はスキップ
                        if not role_code:
                            logger.warn(
                                f"{file_name} の user_id: {user_id} のrole_codeが空です。ログイン処理をスキップします。"
                            )
                            continue

                        if status == "1":
                            if role_code in ["00010008", "00050009", "00040002"]:
                                user_pw = "TEPCOghg2024"
                            elif role_code == "00030004":
                                user_pw = "PGghg2024"
                            else:
                                continue

                            pg_cursor.execute(
                                """
                                INSERT INTO m_user 
                                (user_id, staff_name, mail_address, user_pw, first_flg, delete_flag, created_by, created_at, updated_by, updated_at)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """,
                                (
                                    user_id,
                                    staff_name,
                                    mail_address,
                                    user_pw,
                                    "0",
                                    0,
                                    "0000",
                                    current_timestamp,
                                    "0000",
                                    current_timestamp,
                                ),
                            )

                        elif status == "2":
                            pg_cursor.execute(
                                "UPDATE m_user SET staff_name = %s, mail_address =  %s, updated_by = %s, updated_at  = %s WHERE user_id = %s",
                                (
                                    staff_name,
                                    mail_address,
                                    "0000",
                                    current_timestamp,
                                    user_id,
                                ),
                            )

                        elif status == "9":
                            pg_cursor.execute(
                                "DELETE FROM m_user WHERE user_id = %s", (user_id,)
                            )

                        pg_conn.commit()
                    except Exception as e:
                        logger.error(
                            f"{file_name} の user_id: {row[2]} の処理中にエラーが発生しました: {e}"
                        )
                        logger.error(f"エラー発生時の行データ: {row}")
                        pg_conn.rollback()
                continue

    except Exception as e:
        logger.error(f"全体処理中にエラーが発生しました: {e}")
        raise e
    finally:
        if pg_cursor:
            pg_cursor.close()
        if pg_conn:
            pg_conn.close()
        logger.info("処理終了")


def detect_encoding_from_bytes(byte_data):
    import chardet

    result = chardet.detect(byte_data)
    return result["encoding"] if result["encoding"] else "utf-8"


def get_csv_to_table_mapping():
    """
    CSVファイル名のプレフィックスとテーブル名のマッピングを取得する関数
    """
    return {
        "User": "user_info",
    }


if __name__ == "__main__":
    insert_m_user_info()
