from tkinter import ttk
from utils.logger import Logger

class WelcomeTab(ttk.Frame):
    def __init__(self, master, newProjectFunction, openProjectFunction,  **kw):
        self.notebook = master
        self.newProject = newProjectFunction
        self.openProject = openProjectFunction
        self.width = kw.pop('width', None)
        self.height = kw.pop('height', None)
        super().__init__(master=master, **kw)
        self.log = Logger(__name__)
        self.log.calledBy()
        
        self.frameWelcome = ttk.Frame(self.notebook, width=800, height=400)
        self.frameWelcome.pack(fill="both", expand=True)
        self.notebook.add(self.frameWelcome, text="Welcome")
        self.frameWelcome.columnconfigure(0, weight=1)
        self.frameWelcome.columnconfigure(1, weight=0)
        self.frameWelcome.columnconfigure(2, weight=1)
        self.frameWelcome.rowconfigure(0, weight=1)
        self.frameWelcome.rowconfigure(1, weight=0)
        self.frameWelcome.rowconfigure(2, weight=0)
        self.frameWelcome.rowconfigure(3, weight=3)

        self.welcomeButtonNewProject = ttk.Button(self.frameWelcome, text="Create New Project", command=self.newProject)
        self.welcomeButtonNewProject.grid(column=1,row=1,sticky="ew")
        self.welcomeButtonOpenProject = ttk.Button(self.frameWelcome, text="Open New Project", command=self.openProject)
        self.welcomeButtonOpenProject.grid(column=1,row=2,sticky="ew")
