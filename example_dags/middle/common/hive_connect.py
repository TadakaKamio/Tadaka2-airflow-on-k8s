import traceback
from middle.common.log import MiddleAppLog, log_writer
from middle.common.utils import get_json_config
from middle.common.utils import install_package

# log出力用インスタンス
logger = MiddleAppLog()
class ImpalaSingleton:
    _instances = {}

    def __new__(cls, user, password):
        if user not in cls._instances:
            cls._instances[user] = super().__new__(cls)
            cls._instances[user]._connection = cls._create_connection(user, password)
        return cls._instances[user]

    @staticmethod
    def _create_connection(user, password):
        install_package("impyla")
        from impala.dbapi import connect
        config = get_json_config()  # 設定値を取得
        return connect(
            host=config["database_hive"]["host"],
            port=config["database_hive"]["port"],
            use_ssl=True,
            ca_cert=config["database_hive"]["ca_cert"],
            user=user,
            password=password,
            auth_mechanism="PLAIN"
        )
    # @log_writer(logger)
    # def __new__(cls, user=None, password=None):
    #     install_package("impyla")
    #     from impala.dbapi import connect
    #     # 設定値格納用JSONファイルを読み込む
    #     config = get_json_config()
        
    #     if cls._instance is None:
    #         cls._instance = super().__new__(cls)
            
    #         # 引数で受け取ったuserとpasswordを使う
    #         user = user or config["database_hive"]["user"]  # 引数がなければ設定ファイルから取得
    #         password = password or config["database_hive"]["password"]  # 引数がなければ設定ファイルから取得
    #         logger.info(f"★{user}：{password}")
    #         try:
    #             cls._instance._connection = connect(
    #                 host=config["database_hive"]["host"],
    #                 port=config["database_hive"]["port"],
    #                 use_ssl=True,
    #                 ca_cert=config["database_hive"]["ca_cert"],
    #                 user=user,
    #                 password=password,
    #                 auth_mechanism="PLAIN"
    #             )
    #         except Exception as e:
    #             traceback.format_stack()
    #             logger.error(f"Hive接続失敗: {str(e)}")
    #             cls._instance = None
        
    #     return cls._instance

    def _connection(self):
        return self._instance._connection
    
    def close_connection(self):
        """ コネクションを開放する"""
        if self._connection is not None:
            self._connection.close()
            self._connection = None