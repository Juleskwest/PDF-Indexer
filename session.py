# Session Manager 
import logger
import os
from configMan import SessionConfig

class SessionManager:
    def __init__(self) -> None:
        self.log = logger.Logger("SessionMan")
        self.log.calledBy()
        self.resetVariables()

    def resetVariables(self):
        self.log.calledBy()
        self.currentSession = ""
        self.configMan = None
        self.configured = False
    
    def new(self, name:str) -> bool:
        self.log.calledBy()
        self.log.info(f"Creating new session {name}")
        if os.path.exists(name):
            return False
        if self.currentSession != "":
            self.close()
        os.mkdir(name)
        self.open(name)

    def open(self, name):
        self.log.calledBy()
        self.resetVariables()
        if os.path.exists(name):
            self.configFilePath = f"{name}/index.ini"
            self.currentSession = name
            self.loadConfig()

    def close(self):
        self.log.calledBy()
        if self.currentSession != "":
            self.saveConfig()
            self.resetVariables()

    def loadConfig(self):
        self.configMan = SessionConfig(self.configFilePath)
        self.configured = self.configMan.config["SESSION"]["Configured"]

    def saveConfig(self):
        self.configMan = SessionConfig(self.configFilePath)
        self.configMan.config["SESSION"]["Configured"] = self.configured
        self.configMan.save()

        pass



if __name__ == "__main__":
    ses = SessionManager()
    ses.new("test")