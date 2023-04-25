import configparser
import os
from logger import Logger

class ConfigManager:
    def __init__(self, configfilePath) -> None:
        self.configFilePath = configfilePath
        self.log = Logger(__name__)
        self.log.stack()
        self.config = configparser.RawConfigParser()
        if os.path.isfile(self.configFilePath):
            self.load()
        else:
            self.default()
    
    def load(self):
        self.log.stack()
        self.config.read(self.configFilePath)
        self.log.info(f"{self.configFilePath} Loaded")

    def default(self):
        self.log.stack()
        self.log.info("Default Config Created")
        self.save()
    
    def edit(self, cat, option, value):
        self.log.stack()
        self.config[cat][option] = value

    def save(self):
        self.log.stack()
        try:
            with open(self.configFilePath, 'w') as configfile:
                self.config.write(configfile)
                self.log.info(f"{self.configFilePath} Saved")
        except FileNotFoundError:
            self.log.exception(f"{self.configFilePath} cannot be saved")

class AppConfig(ConfigManager):
    def __init__(self, configfilePath) -> None:
        super().__init__(configfilePath)
    
    def default(self):
        self.log.stack()
        self.config["APP"] = {"lastSession": ""}
        self.config["SETTINGS"] = {"fontSize": 14}
        self.log.info("App Config Created")
        self.save()

class SessionConfig(ConfigManager):
    def __init__(self, configfilePath) -> None:
        super().__init__(configfilePath)
    
    def default(self):
        self.log.stack()
        self.config["PDF"] = {"filePath": "", "password": "", "bookSetName": "", "numberOfBooks": "", "pdfsize": ""}
        self.config["DETAILS"] = {"lastPage":"1", "lastBook":"1", "zoomMain": "1.0", "zoomPDF": "1.0"}
        self.config["INDEX"] = {"filePath": ""}
        self.config["BOOKS"] = {}
        self.log.info("Session Config Created")
        self.save()
