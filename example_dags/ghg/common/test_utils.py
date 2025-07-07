import sqlite3

from ghg.common.log import MyAppLog, log_writer

logger = MyAppLog()


@log_writer(logger)
def test_query(query, operation=""):
    local_db_path = r"C:\ws\db_ghg.db"
    with sqlite3.connect(local_db_path) as conn:
        try:
            cursor = conn.cursor()
            cursor.execute(query)

            if operation == "fetchall":
                results = cursor.fetchall()
                return results
            elif operation == "fetchone":
                return cursor.fetchone()
        finally:
            cursor.close()
