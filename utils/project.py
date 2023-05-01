# Project Manager 
import utils.logger as logger
import os

import zipfile
from utils.configMan2 import ProjectConfigMan

class ProjectManager:
    def __init__(self) -> None:
        self.log = logger.Logger("ProjectMan")
        self.log.calledBy()
        self.resetVariables()

    def resetVariables(self):
        self.log.calledBy()
        self.openned = False
        self.currentProject = ""
        self.configMan = None
        self.config = None
        self.configured = False

    def exists(self, name:str) -> bool:
        self.log.calledBy()
        name = f"{os.path.abspath(os.getcwd())}\\projects\\{name}"
        print(f"Result of checking if {name} exists")
        print(os.path.isdir(name))
        if os.path.isdir(name):
            self.log.warning(f"Project {name} already exists")
            return True
        return False
    
    def new(self, name:str) -> bool:
        self.log.calledBy()
        self.log.info(f"Creating new Project {name}")
        if self.exists:
            return False
        if self.openned:
            self.close()
        os.mkdir(name)
        self.open(name)
        return True

    def open(self, name):
        self.log.calledBy()
        if self.openned:
            self.close()
        if os.path.exists(name):
            self.configFilePath = f"{name}/Project.ini"
            self.currentProject = name
            self.loadConfig()
            self.openned = True
            return True
        else:
            self.log.warning(f"Could not open {name}")
            return False

    def save(self):
        self.configMan.save()

    def close(self):
        self.log.calledBy()
        if self.openned:
            self.save()
            self.resetVariables()

    def loadConfig(self):
        self.configMan = ProjectConfigMan(self.configFilePath)
        self.config = self.configMan.Project
        self.configured = bool(self.config.configured)

