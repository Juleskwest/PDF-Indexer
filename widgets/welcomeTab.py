from tkinter import ttk
from utils.logger import Logger

class WelcomeTab(ttk.Frame):
    def __init__(self, master, newSessionFunction, openSessionFunction,  **kw):
        self.notebook = master
        self.newSession = newSessionFunction
        self.openSession = openSessionFunction
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

        self.welcomeButtonNewSession = ttk.Button(self.frameWelcome, text="Create New Session", command=self.newSession)
        self.welcomeButtonNewSession.grid(column=1,row=1,sticky="ew")
        self.welcomeButtonOpenSession = ttk.Button(self.frameWelcome, text="Open New Session", command=self.openSession)
        self.welcomeButtonOpenSession.grid(column=1,row=2,sticky="ew")
