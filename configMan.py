import configparser
import os

class ConfigManager:
    def __init__(self, configfilePath) -> None:
        self.configFilePath = configfilePath
        self.config = configparser.RawConfigParser()
        if os.path.isfile(self.configFilePath):
            self.load()
        else:
            self.default()
    
    def load(self):
        self.config.read(self.configFilePath)
        print(f"C - INFO  - {self.configFilePath} Loaded")

    def default(self):
        print("C - INFO  - Default Config Created")
        self.save()
    
    def edit(self, cat, option, value):
        self.config[cat][option] = value

    def save(self):
        try:
            with open(self.configFilePath, 'w') as configfile:
                self.config.write(configfile)
                print(f"C - INFO  - {self.configFilePath} Saved")
        except FileNotFoundError:
            print(f"C - ERROR - {self.configFilePath} cannot be saved")

class AppConfig(ConfigManager):
    def __init__(self, configfilePath) -> None:
        super().__init__(configfilePath)
    
    def default(self):
        self.config["APP"] = {"lastSession": ""}
        self.config["SETTINGS"] = {"fontSize": 14}
        print("C - INFO  - App Config Created")
        self.save()

class SessionConfig(ConfigManager):
    def __init__(self, configfilePath) -> None:
        super().__init__(configfilePath)
    
    def default(self):
        self.config["PDF"] = {"filePath": "", "password": "", "bookSetName": "", "numberOfBooks": "", "pdfsize": ""}
        self.config["DETAILS"] = {"lastPage":"1", "lastBook":"1", "zoomMain": "1.0"}
        self.config["INDEX"] = {"filePath": ""}
        self.config["BOOKS"] = {}
        print("C - INFO  - Session Config Created")
        self.save()
