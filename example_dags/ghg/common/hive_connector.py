import json

from airflow.models import Variable

import ghg.common.settings as Constants
from ghg.common.log import MyAppLog, log_writer
from ghg.common.utils import check_install_package, get_relative_path

logger = MyAppLog()


class HiveConnector:
    """
    Hiveデータベースへの接続を管理するクラス。

    設定ファイルからHiveの接続設定を読み込み、接続、切断、トランザクションの管理を行います。
    """

    @log_writer(logger)
    def __init__(self):
        """
        コンストラクタ。設定ファイルからHiveの接続設定を読み込み、初期化します。
        """
        # impylaパッケージがインストールされていることを確認する
        check_install_package(Constants.PackageName.IMPYLA.value)

        # AirflowのVariableから実行モードを取得
        # run_mode = Variable.get("GHG_RUN_MODE")
        # logger.info(f"■run_mode: {run_mode}")

        hive_config = get_relative_path("conf/hive_config_for_prod.json")

        with open(hive_config, "r") as f:
            config = json.load(f)["hive_common"]

        self.host = config["host"]
        self.port = config["port"]
        self.database = config["database"]
        self.use_ssl = config["use_ssl"]
        self.ca_cert = config["ca_cert"]
        self.user = config["user"]
        self.password = config["password"]
        self.auth_mechanism = config["auth_mechanism"]
        self.conn = None

    @log_writer(logger)
    def hive_connect(self):
        """
        Hiveデータベースへの接続を確立します。

        既に接続が存在する場合は、その接続を返します。
        新たに接続を確立する場合は、接続設定を使用して接続を行い、その接続を返します。

        戻り値:
            接続オブジェクト。
        """
        if self.conn:
            logger.debug("既にHive接続されています。")
            return self.conn

        from impala.dbapi import connect

        self.conn = connect(
            host=self.host,
            port=self.port,
            database=self.database,
            use_ssl=self.use_ssl,
            ca_cert=self.ca_cert,
            user=self.user,
            password=self.password,
            auth_mechanism=self.auth_mechanism,
        )
        logger.info("Hive新たに接続しました。")
        return self.conn

    @log_writer(logger)
    def close_connection(self):
        """
        Hiveデータベースへの接続を閉じます。
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Hive接続を閉じました。")

    @log_writer(logger)
    def rollback(self):
        """
        現在のトランザクションをロールバックします。

        ロールバック操作がサポートされていないデータベースではエラーメッセージをログに出力します。
        """
        if self.conn:
            try:
                self.conn.rollback()
                logger.info("トランザクションをロールバックしました。")
            except NotImplementedError:
                logger.error(
                    "このデータベースではロールバック操作はサポートされていません。"
                )

    @log_writer(logger)
    def commit(self):
        """
        現在のトランザクションをコミットします。

        コミット操作がサポートされていないデータベースではエラーメッセージをログに出力します。
        """
        if self.conn:
            try:
                self.conn.commit()
                logger.info("トランザクションをコミットしました。")
            except AttributeError:
                logger.error(
                    "このデータベースではコミット操作はサポートされていません。"
                )

    @log_writer(logger)
    def execute_query(self, query, operation=Constants.DBoperation.NONE):
        """
        Hiveデータベースへ接続を行う、
        指定されたSQLクエリを実行し、オプションでクエリの全結果を取得します。

        パラメータ:
            query (str): 実行するSQLクエリ。
            operation (str): クエリ実行後に実行する操作の種類。
                             現在は "fetchall" のみをサポートしており、クエリの全結果を取得します。

        戻り値:
            list: operation が "fetchall" に指定された場合、クエリの全結果をリストとして返します。
                  それ以外の場合は何も返しません。
        """
        # Hiveデータベースへの接続
        self.hive_connect()

        with self.conn.cursor() as cursor:
            cursor.execute(query)

            if operation == Constants.DBoperation.FETCHALL:
                return cursor.fetchall()
            elif operation == Constants.DBoperation.FETCHONE:
                return cursor.fetchone()
            return None

    @log_writer(logger)
    def get_dataframe(self, query):
        """
        Hiveデータベースへ接続を行う、
        指定されたSQLクエリを実行し、オプションでクエリの全結果を取得します。
        実行結果をPandas DataFrameに変換する。

        パラメータ:
            query (str): 実行するSQLクエリ。

        戻り値:
            DataFrame: クエリの全結果をPandas DataFrameに変換して返します。
        """

        from impala.util import as_pandas

        # Hiveデータベースへの接続
        self.hive_connect()

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            return as_pandas(cursor)
