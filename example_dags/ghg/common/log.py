import datetime
import logging
import os


class MyAppLog:
    """
    アプリケーションのロギングを管理するクラス。

    環境変数からログレベルを取得し、設定されたレベルに応じてログ出力を行います。
    INFO, ERROR, WARNING, CRITICAL, DEBUGのログレベルが利用可能です。
    """

    def __init__(self):
        """
        クラスの初期化メソッド。

        環境変数'LOG_LEVEL'からログレベルを読み取り、ログレベルを設定します。
        ログレベルが設定されていない場合は、デフォルトとしてINFOレベルが使用されます。
        """
        log_level = os.environ.get("LOG_LEVEL")
        if log_level is None:
            log_level = logging.INFO
        else:
            if log_level.lower() == "error":
                log_level = logging.ERROR
            elif log_level.lower() == "warning":
                log_level = logging.WARNING
            elif log_level.lower() == "critical":
                log_level = logging.CRITICAL
            elif log_level.lower() == "debug":
                log_level = logging.DEBUG
            else:
                log_level = logging.INFO

        self.logger = logging.getLogger("ghg")
        # ISO8601 Time Format
        logging.Formatter.formatTime = (
            lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(
                record.created, datetime.timezone.utc
            )
            .astimezone()
            .isoformat(sep="T", timespec="milliseconds")
        )
        self.logger.setLevel(log_level)
        self.ch = logging.StreamHandler()
        self.logger.addHandler(self.ch)

    def info(self, msg):
        """
        INFOレベルのログを出力します。

        パラメータ:
            msg (str): ログに出力するメッセージ。
        """
        formatter = logging.Formatter(
            "%(asctime)s "
            "filename:%(filename)s "
            "levelname:%(levelname)s "
            "message:%(message)s"
        )
        self.ch.setFormatter(formatter)
        self.logger.info(msg)

    def warn(self, msg):
        """
        WARNINGレベルのログを出力します。

        パラメータ:
            msg (str): ログに出力するメッセージ。
        """
        formatter = logging.Formatter(
            "%(asctime)s "
            "levelname:%(levelname)s "
            "filename:%(filename)s "
            "lineno:%(lineno)d "
            "modulename:%(module)s "
            "funcname:%(funcName)s "
            "message:%(message)s"
        )
        self.ch.setFormatter(formatter)
        self.logger.warning(msg)

    def error(self, msg):
        """
        ERRORレベルのログを出力します。

        パラメータ:
            msg (str): ログに出力するメッセージ。
        """
        formatter = logging.Formatter(
            "%(asctime)s "
            "levelname:%(levelname)s "
            "filename:%(filename)s "
            "lineno:%(lineno)d "
            "modulename:%(module)s "
            "funcname:%(funcName)s "
            "message:%(message)s"
        )
        self.ch.setFormatter(formatter)
        self.logger.error(msg)

    def critical(self, msg):
        """
        CRITICALレベルのログを出力します。

        パラメータ:
            msg (str): ログに出力するメッセージ。
        """
        formatter = logging.Formatter(
            "%(asctime)s "
            "levelname:%(levelname)s "
            "filename:%(filename)s "
            "lineno:%(lineno)d "
            "modulename:%(module)s "
            "funcname:%(funcName)s "
            "message:%(message)s"
        )
        self.ch.setFormatter(formatter)
        self.logger.critical(msg)

    def debug(self, msg):
        """
        DEBUGレベルのログを出力します。

        パラメータ:
            msg (str): ログに出力するメッセージ。
        """
        formatter = logging.Formatter(
            "%(asctime)s "
            "levelname:%(levelname)s "
            "filename:%(filename)s "
            "lineno:%(lineno)d "
            "modulename:%(module)s "
            "funcname:%(funcName)s "
            "message:%(message)s"
        )
        self.ch.setFormatter(formatter)
        self.logger.debug(msg)


def log_writer(logger):
    """
    ロガーを使用して関数の開始、終了、および引数をデバッグログに記録するデコレータ。

    パラメータ:
        logger (MyAppLog): ログ出力に使用するMyAppLogインスタンス。

    戻り値:
        function: デコレートされた関数。
    """

    def _log_writer(func):

        def wrapper(*args, **kwargs):
            logger.debug("start " + func.__name__)
            for k, v in kwargs.items():
                logger.debug(str(k) + " :" + str(v))

            result = func(*args, **kwargs)

            logger.debug(func.__name__ + " returns :" + str(result))
            logger.debug("end " + func.__name__)
            return result

        return wrapper

    return _log_writer
