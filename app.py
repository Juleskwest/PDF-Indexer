from gui import GUI
from logger import Logger
from configMan2 import ConfigMan

class App:
    def __init__(self) -> None:
        self.log = Logger()
        self.log.stack()
        self.gui = GUI()
        self.sessionMan 
        self.configMan = ConfigMan
        
    def run(self):
        self.log.stack()
        self.gui.run()