import configparser
import os
import yaml
from loguru import logger
from constants import DATA_PATH, LOG_PATH, DEFAULT_TEMPLATE

def logging():
    """
    The logging function is used to create a log file in the LOG_PATH directory.\n
    The retention period for this log file is 2 days.
    """
    logger_format = (
        "<green>{time:DD-MM-YYYY HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "{message}"
    )
    logger.add(LOG_PATH/"TopicMaker.log", format=logger_format, retention="2 days")
    logger.info(DATA_PATH)
    logger.info(LOG_PATH)

logging()

class Config:
    config = configparser.ConfigParser()

    def write_config_file(self):
        """
        The write_config_file function writes the config.ini file to disk,
        """
        self.config.write(open(DATA_PATH/'config.ini', 'w', encoding='utf8'))
        self.config.read(DATA_PATH/'config.ini')

    def read_config_file(self):
        """
        The read_config_file function reads the config.ini file and sets the values of\n
        the omdb_api, imgbb_api, dark_mode variables to those found in the config.ini file.
        """
        if not os.path.exists(DATA_PATH/'config.ini'):
            self.config.add_section("SETTINGS")
            self.config.set("SETTINGS", "omdb_api", "")
            self.config.set("SETTINGS", "imgbb_api", "")
            self.config.set("SETTINGS", "dark_mode", "True")
            self.write_config_file()
        if not os.path.exists(DATA_PATH/'list_sources.yaml'):
            list_sources = ['WEB-DL', 'REMUX', 'Full Bluray', 'WEBRip']
            with open(DATA_PATH/'list_sources.yaml', 'w', encoding='utf8') as file:
                yaml.safe_dump(list_sources, file, sort_keys=False)
        if not os.path.exists(DATA_PATH/'template.txt'):
            with open(DATA_PATH/'template.txt', 'w', encoding='utf8') as file:
                file.write(DEFAULT_TEMPLATE)
        else:
            self.config.read(DATA_PATH/'config.ini')
