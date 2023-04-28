from app.gui import GUI
from utils.logger import Logger
from utils.configMan2 import AppConfigMan

class App:
    def __init__(self) -> None:
        self.log = Logger(__name__)
        self.log.calledBy()

        self.config = AppConfigMan("appConfig.ini")
        self.gui = GUI(self, self.config.Gui)

        self.sessionMan = None
        
    def run(self):
        self.log.calledBy()
        self.gui.run()
