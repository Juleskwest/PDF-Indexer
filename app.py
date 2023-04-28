from gui import GUI
from logger import Logger
from configMan2 import AppConfigMan

class App:
    def __init__(self) -> None:
        self.log = Logger(__name__)
        self.log.calledBy()

        self.config = AppConfigMan("appConfig.ini")
        self.gui = GUI(self, self.config.Gui)

        self.sessionMan 
        
    def run(self):
        self.log.calledBy()
        self.gui.run()
