import logging
import os
import datetime

class MiddleAppLog():

    def __init__(self):
        log_level = os.environ.get('LOG_LEVEL')
        if log_level == None:
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

        self.logger = logging.getLogger(__name__)
        # ISO8601 Time Format
        logging.Formatter.formatTime = (
            lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(
                record.created, datetime.timezone.utc
            ).astimezone(datetime.timezone(datetime.timedelta(hours=9))).isoformat(
                sep="T", timespec="milliseconds"
            )
        )
        self.logger.setLevel(log_level)
        handler = None
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            self.logger.addHandler(handler)
        else:
            handler = self.logger.handlers[0]
        self.ch = handler
        self.log_box = []

    def info(self, msg):
        formatter = logging.Formatter('[%(asctime)s]'
                                      '[%(levelname)s]'
                                      '[%(filename)s]'
                                      ' : %(message)s')
        self.ch.setFormatter(formatter)
        self.logger.info(msg, stacklevel=2)
        # log_message = f"{log_entry['time']} filename:{filename} levelname:{level} message:{message}"
        
        self.log_box.append(msg)

    def warn(self, msg):
        formatter = logging.Formatter('%(asctime)s '
                                      'levelname:%(levelname)s '
                                      'filename:%(filename)s '
                                      'lineno:%(lineno)d '
                                      'modulename:%(module)s '
                                      'funcname:%(funcName)s '
                                      'message:%(message)s')
        self.ch.setFormatter(formatter)
        self.logger.warning(msg)

    def error(self, msg):
        formatter = logging.Formatter('%(asctime)s '
                                      'levelname:%(levelname)s '
                                      'filename:%(filename)s '
                                      'lineno:%(lineno)d '
                                      'modulename:%(module)s '
                                      'funcname:%(funcName)s '
                                      'message:%(message)s')
        self.ch.setFormatter(formatter)
        self.logger.error(msg)

    def critical(self, msg):
        formatter = logging.Formatter('%(asctime)s '
                                      'levelname:%(levelname)s '
                                      'filename:%(filename)s '
                                      'lineno:%(lineno)d '
                                      'modulename:%(module)s '
                                      'funcname:%(funcName)s '
                                      'message:%(message)s')
        self.ch.setFormatter(formatter)
        self.logger.critical(msg)

    def debug(self, msg):
        formatter = logging.Formatter('%(asctime)s '
                                      'levelname:%(levelname)s '
                                      'filename:%(filename)s '
                                      'lineno:%(lineno)d '
                                      'modulename:%(module)s '
                                      'funcname:%(funcName)s '
                                      'message:%(message)s')
        self.ch.setFormatter(formatter)
        self.logger.debug(msg)

def log_writer(logger):

    def _log_writer(func):

        def wrapper(*args, **kwargs):
            logger.debug('start ' + func.__name__)
            for k, v in kwargs.items():
                logger.debug(str(k) + ' :' + str(v))

            result = func(*args, **kwargs)

            logger.debug(func.__name__ + ' returns :' + str(result))
            logger.debug('end ' + func.__name__)
            return result

        return wrapper

    return _log_writer
