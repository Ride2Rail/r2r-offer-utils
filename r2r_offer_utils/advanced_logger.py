import logging
import configparser as cp
import sys
from os import path

# name of the main module
main_module_name = path.splitext(path.basename(sys.modules["__main__"].__file__))[0]
# logger
logger = logging.getLogger(main_module_name)


class MyLogger:
    """
    class to obtain the logger for errors into a file
    """

    # initiates config logging error to the log which name is specified in the error_file parameter
    def __init__(self, error_file="error"):
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                           datefmt='%Y-%m-%d %H:%M:%S')
        fh = logging.FileHandler(f'{error_file}.log')
        logger.setLevel(logging.DEBUG)
        fh.setLevel(logging.ERROR)
        fh.setFormatter(self.formatter)
        logger.addHandler(fh)
        self.verboseConsole = 0

    # adds logger that logs INFO into console (terminal)
    def addConsoleLogger(self, logging_level=logging.INFO):
        ch = logging.StreamHandler()
        ch.setLevel(logging_level)
        ch.setFormatter(self.formatter)
        logger.addHandler(ch)
        self.verboseConsole = 1


class ConfigLoader:
    """
    class serving to load the confing
    if it fails it loggs the error into error_logger
    """

    # loads the config, writes error if config not found
    def __init__(self, my_logger):
        self.config = cp.ConfigParser()
        out = self.config.read(f'{main_module_name}.conf')
        self.loaded = True
        if len(out) == 0:
            self.loaded = False
            logger.error(f'Config {main_module_name}.conf was not found')
        elif int(self.config.get('running', 'verbose')):
            my_logger.addConsoleLogger()
            logger.info("config loaded successfully")


my_logger = MyLogger()
my_configLoader = ConfigLoader(my_logger)
