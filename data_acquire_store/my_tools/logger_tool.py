import logging
import config


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class loggler_tool:

    def __init__(self, logger_file=config.logger_file, logger_name=config.logger_name,
                 logger_path=config.logger_path,
                 logger_formatter=config.logger_formatter, logger_console_level=config.logger_console_level,
                 logger_file_level=config.logger_file_level):

        self.logger_file = logger_file

        # create logger
        self.logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(level=logger_console_level)

        # create console handler
        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(level=logger_file_level)

        # create file handler
        self.file_handler = logging.FileHandler(filename=logger_path)
        self.file_handler.setLevel(level=logger_file_level)

        # create formatter
        self.formatter = logging.Formatter(fmt=logger_formatter)

        self.console_handler.setFormatter(self.formatter)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.file_handler)

    def debug(self, logger_file=config.logger_file, message=""):
        self.logger.debug("{} => {}".format(logger_file, message))

    def info(self, logger_file=config.logger_file, message=""):
        self.logger.info("{} => {}".format(logger_file, message))

    def warning(self, logger_file=config.logger_file, message=""):
        self.logger.warning("{} => {}".format(logger_file, message))

    def error(self, logger_file=config.logger_file, message=""):
        self.logger.error("{} => {}".format(logger_file, message))

    def critical(self, logger_file=config.logger_file, message=""):
        self.logger.critical("{} => {}".format(logger_file, message))

