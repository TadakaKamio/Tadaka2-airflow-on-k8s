import json
import os

import psycopg2

from ghg.common.log import MyAppLog, log_writer

logger = MyAppLog()


@log_writer(logger)
def load_postgres_config(config_path=None):
    """
    PostgreSQL の接続情報を JSON から読み込む
    """
    try:
        if not config_path:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(base_dir, "conf", "postgres_config.json")
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config
    except Exception as e:
        logger.error(f"PostgreSQL の設定ファイル読み込みに失敗しました: {e}")
        raise e


def connect_postgres(config_path=None):
    """
    PostgreSQL に接続して connection と cursor を返す
    """
    try:
        config_all = load_postgres_config(config_path)
        config = config_all["postgre"]
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        logger.info("PostgreSQL 接続成功")
        return conn, cursor
    except Exception as e:
        logger.error(f"PostgreSQL 接続失敗: {e}")
        raise e
