import logging
import configparser as cp
import sys
import inspect
from os import path

# name of the main module
# main_module_name = path.splitext(path.basename(sys.modules["__main__"].__file__))[0]
# main_module_name = path.splitext(path.basename(inspect.stack()[0].filename))[0]
# main_module_name = path.splitext(path.basename(__file__))[0]
# logger = logging.getLogger(main_module_name)


class LoggerFormatter:
    """
    class to obtain the logger for errors into a file
    """

    # initiates config logging error to the log which name is specified in the error_file parameter
    def __init__(self, logger, error_file="error"):
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler(f'{error_file}.log')
        self.logger = logger
        self.logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.ERROR)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        self.verboseConsole = 0

    # adds logger that logs INFO into console (terminal)
    def addConsoleLogger(self, logging_level=logging.INFO):
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)
        self.verboseConsole = 1


class ConfigLoader:
    """
    class serving to load the config
    if it fails it logs the error into error_logger
    """

    # loads the config, writes error if config not found
    def __init__(self, logger_formatter, main_module_name):
        self.config = cp.ConfigParser()
        out = self.config.read(f'{main_module_name}.conf')
        self.loaded = True
        if len(out) == 0:
            self.loaded = False
            logger_formatter.logger.error(f'Config {main_module_name}.conf was not found')
        else:
            self.loadVerbose(logger_formatter)
            logger_formatter.logger.info("config loaded successfully")

    # loads verbose option from the config
    def loadVerbose(self, logger_formatter):
        if int(self.config.get('running', 'verbose')):
            logger_formatter.addConsoleLogger()


# load the config with anonymous instances
# config = ConfigLoader(LoggerFormatter()).config
