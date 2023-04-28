import configparser
import os
from logger import Logger

class Section:
    def __init__(self, section:str, parent, values:dict) -> None:
        self.parent:ConfigMan
        self.section:str
        self.values:dict
        self.__dict__["section"] = section
        self.__dict__["parent"] = parent
        self.__dict__["values"] = values
        for key in values:
            setattr(self, key, values[key])

    def __setattr__(self, __name: str, __value: any) -> None:
        self.__dict__[__name] = __value
        if __name in self.values:
            self.parent.edit(self.section, __name, __value)


class ConfigMan:
    def __init__(self, filepath:str="config.ini") -> None:
        self.log = Logger(__name__)
        self.log.calledBy()

        self.filepath = filepath
        self.sections:list = []
        self.configParser:configparser.RawConfigParser
        self.reset()
        if self.checkFilePath():
            self.load()
        else:
            self.new()
    
    def reset(self) -> None:
        self.log.calledBy()
        self.configParser = configparser.RawConfigParser()
        for section in self.sections:
            del(self.__dict__[section])
        self.sections = []
    
    def new(self) -> None:
        self.log.calledBy()
        self.reset()
        self.default()
        self.addToClass()
        self.save()

    def load(self) -> None:
        self.log.calledBy()
        self.reset()
        if self.checkFilePath():
            self.configParser.read(self.filepath)
            self.addToClass()
            self.log.info(f"Config file: {self.filepath} loaded")
        else:
            self.log.warning(f"Config file: {self.filepath} does not exist!")

    def save(self) -> None:
        self.log.calledBy()
        try:
            with open(self.filepath, "w") as configfile:
                self.configParser.write(configfile)
                self.log.info(f"Config file: {self.filepath} saved!")
        except:
            self.log.error(f"Config file: {self.filepath} not saved!")
            self.log.exception()
    
    def addToClass(self) -> None:
        self.log.calledBy()
        self.sections = self.configParser.sections()
        for section in self.sections:
            setattr(self, section, Section(section, self, dict(self.configParser.items(section))))

    def edit(self, section:str, key:str, value:any) -> None:
        self.log.calledBy()
        self.configParser[section][key] = str(value)

    def checkFilePath(self) -> bool:
        self.log.calledBy()
        return os.path.isfile(self.filepath)
    
    def default(self):
        self.configParser["DEFAULT"] = {"Replace": "me"}

class AppConfigMan(ConfigMan):
    def __init__(self, filepath: str = "config.ini") -> None:
        super().__init__(filepath)
    
    def default(self):
        self.configParser["App"] = {}
        self.configParser["Gui"] = {"width":"800", "height":"600"}