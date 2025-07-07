from middle.common.log import MiddleAppLog, log_writer
from middle.common.utils import get_json_config
from middle.common.utils import install_package

# log出力用インスタンス
logger = MiddleAppLog()

class Psycopg2Singleton:
    _instance = None

    @log_writer(logger)
    def __new__(cls):
        install_package("psycopg2")
        import psycopg2
        # 設定値格納用JSONファイルを読み込む
        config = get_json_config()
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = psycopg2.connect(
                host = config["database_posgre"]["host"],
                port = config["database_posgre"]["port"],
                database = config["database_posgre"]["database"],
                user = config["database_posgre"]["user"],
                password = config["database_posgre"]["password"])
        return cls._instance

    def _connection(self):
        return self._instance._connection
    
    def close_connection(self):
        """ コネクションを開放する"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None