from app.gui import GUI
from utils.logger import Logger
from utils.configMan2 import AppConfigMan
from utils.project import ProjectManager

class App:
    def __init__(self) -> None:
        self.log = Logger(__name__)
        self.log.calledBy()

        self.config = AppConfigMan("appConfig.ini")
        self.project = ProjectManager()
        self.gui = GUI(self, self.config.Gui)
        
    def run(self):
        self.log.calledBy()
        self.gui.run()

    def setup(self):
        self.log.calledBy()
        if self.openlast():
            if self.project.configured:
                self.gui.fullLoad()
            else:
                self.gui.openProjectConfigTab()
        else:
            self.gui.openWelcomeTab()

    def openlast(self):
        self.log.calledBy()
        if self.config.Session.last != "":
            self.project.open(self.config.Session.last)
            return True
        return False
    
    def fullLoad(self):
        self.log.calledBy()
        # self.pdf.open()
        # self.index.open()

    def newProject(self):
        name = self.gui.newProject()
        if name != False:
            self.project.new(name)
            self.gui.closeTab("Welcome")
            self.gui.openProjectConfigTab()

    def openProject(self):
        pass