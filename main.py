import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
import readonlytext
import os
import backend
from pdfviewer import PDFViewer
from indexrow import IndexRow
from logger import Logger
from update import UpdateManager

class App:
    def __init__(self) -> None:
        self.log = Logger("App")
        self.log.stack()
        self.log.info("App Started")

        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.__del__) # Defintily needed or doesn't capture close
        self.root.bind("<Configure>", self.resize)
        self.root.minsize(800,400)

        self.resetVariables()
        self.backend = backend.Backend()
        self.updateManager = UpdateManager()

        ## Style Seclection
        self.style = ttk.Style()
        #self.changestyle()
        #self.root.call("source", "arc.tcl")
        #self.style.theme_use("arc")

        self.createWidgets()
        
        self.root.title("PDF Indexer.")
        if self.backend.currentSession != "":
            #self.root.title(f"PDF Indexer. Current Session: {self.backend.currentSession}")
            #self.notebook.select(1)
            #self.PDFpdfviewer.zoomlevel = self.backend.getPDFzoom()
            #self.Mainpdfviewer.zoomlevel = self.backend.getMAINzoom()
            pass
        
        if self.backend.currentSession == "":
            self.openWelcomeTab()
        else:
            self.openSessionTab()
            #self.openMainTab()
            #self.openPDFTab()
            #self.openIndex()

    def resetVariables(self):
        self.openTabs = {}
        self.width:int=None
        self.height:int=None
        self.mainPixmap = None
        self.PDFPathStrVar = tkinter.StringVar(self.root, "")
        self.PDFPasswordStrVar = tkinter.StringVar(self.root, "")
        self.IndexPathStrVar = tkinter.StringVar(self.root, "")

    def __del__(self) -> None:
        self.log.stack()    
        if self.backend.currentSession != "":
            self.closeSession()
        try:
            self.root.destroy()
        except tkinter.TclError as err:
            if err.__str__() != "can't invoke \"destroy\" command: application has been destroyed":
                self.log.exception("Tcl Error on exit")
        finally:
            self.log.info("Exited from __del__")

    def run(self) -> None:
        self.log.stack()
        self.log.info("Mainloop Running")
        self.root.mainloop()

    def exit(self, event=None):
        self.log.stack()
        self.root.quit()
        self.log.info("Exited from exit()")

    def changestyle(self) -> None:
        self.log.stack()
        self.log.info("Change Style")
        ## Will need to clean the colours up
        MainBGColor = "#2d2d2d"
        subBGColor = "#252526"
        SelectedTabBGColour = "#1e1e1e"
        HoverColor = "Orange"
        textColor = "#eeeeee"

        self.style.theme_create( "dark", parent = "default", settings ={
                "TNotebook": {
                    "configure": {"background":subBGColor, "tabmargins":[0, 0, 0, 0], "borderwidth":0} # tab margines are around the tabs at the top 
                },
                "TNotebook.Tab": {
                    "configure": {"background": MainBGColor, "foreground": textColor, "bordercolor": subBGColor, "padding":[10, 5], "borderwidth":[0]}, ## padding is around the title in the tab, border width of the tab bar
                    "map":       {"background": [("selected", SelectedTabBGColour), ('!active', MainBGColor), ('active', HoverColor)], "expand": [("selected", [0, 0, 0, 0])]} # expand is the movemnt of the tab box when selected
                },
                "TFrame":{
                    "configure": {"background":SelectedTabBGColour, "relief":tkinter.FLAT, "borderwidth":[0]}
                }
            })
        self.style.theme_use("dark")
        # the layout removes the focus dotted box from selected tab
        self.style.layout("Tab",
                    [('Notebook.tab', {'sticky': 'nswe', 'children':
                        [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                            #[('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
                                [('Notebook.label', {'side': 'top', 'sticky': ''})],
                            #})],
                        })],
                    })]
                 )

    def createWidgets(self) -> None:
        self.log.stack()
        self.log.info("Create Widgets")
        ####### Menu Bar ############
        self.menu = tkinter.Menu(self.root)
        self.root.config(menu=self.menu)

        ## Sub menus
        # File
        self.menuFile = tkinter.Menu(self.menu, title="File", tearoff=False)
        self.menu.add_cascade(label="File", menu=self.menuFile)
        self.menuFile.add_command(label="Open Text File", command=self.openTXTFile)

        # Session
        self.menuSession = tkinter.Menu(self.menu, title="Session", tearoff=False)
        self.menu.add_cascade(label="Session", menu=self.menuSession)
        self.menuSession.add_command(label="New", command=self.newSession)
        self.menuSession.add_command(label="Open", command=self.openSession)
        self.menuSession.add_command(label="Close", command=self.closeSession)
        self.menuSession.add_separator()
        self.menuSession.add_command(label="Exit", command=self.exit)
        # PDF
        self.menuPDF = tkinter.Menu(self.menu, title="PDF", tearoff=False)
        self.menu.add_cascade(label="PDF", menu=self.menuPDF)
        self.menuPDF.add_command(label="Add PDF", command=self.addPDF)
        self.menuPDF.add_command(label="Add password", command=self.addPDFPassword)
        self.menuPDF.add_separator()
        self.menuPDF.add_command(label="Open PDF", command=self.openPDF)
        self.menuPDF.add_command(label="Process PDF", command=self.proccessPDF)
        self.menuPDF.add_command(label="PDF Page", command=self.pdfSetup)
        self.menuPDF.add_separator()
        self.menuPDF.add_command(label="Test Add", command=self.testAdd)
        # INDEX
        self.menuIndex = tkinter.Menu(self.menu, title="Index", tearoff=False)
        self.menu.add_cascade(label="Index", menu=self.menuIndex)
        self.menuIndex.add_command(label="New", command=self.newIndex)
        self.menuIndex.add_command(label="Save", command=self.saveIndex)
        self.menuIndex.add_command(label="Open", command=self.openIndex)
        self.menuIndex.add_command(label="Close", command=self.closeIndex)
        self.menuIndex.add_separator()
        self.menuIndex.add_command(label="Edit", command=self.test)
        # View
        self.menuView = tkinter.Menu(self.menu, title="View", tearoff=False)
        self.menu.add_cascade(label="View", menu=self.menuView)
        self.menuView.add_command(label="Test", command=self.test)
        # Help
        self.menuHelp = tkinter.Menu(self.menu, title="Help", tearoff=False)
        self.menu.add_cascade(label="Help", menu=self.menuHelp)
        # Will add a update check button
        self.menuHelp.add_command(label="Latest Version")
        self.menuHelp.add_command(label="Check for update", command=self.checkVersion)
        self.checkVersion()
        self.menuHelp.add_command(label="Update", command=self.updateManager.update)

        ####### Notebook ############
        self.notebook = ttk.Notebook(self.root)
        self.notebook.bind('<<NotebookTabChanged>>', self.notebookTABChange)
        self.notebook.pack(fill="both", expand=True)


    def checkVersion(self, event=None):
        self.log.stack()
        self.updateManager.checkRemoteVersion()
        self.updateManager.checkLocalVersion()
        self.updateManager.checkUpdateAvaliable()
        if self.updateManager.newVersionAvaliable:
            self.menuHelp.entryconfigure(0, label="Update Avaliable!")
        else:
            self.menuHelp.entryconfigure(0, label="Latest Version")


    def openWelcomeTab(self):
        self.log.stack()
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
        self.welcomeButtonOpenSession = ttk.Button(self.frameWelcome, text="Open Session", command=self.openSession)
        self.welcomeButtonOpenSession.grid(column=1,row=2,sticky="ew")

    def openSessionTab(self):
        self.log.stack()
        self.frameSession = ttk.Frame(self.notebook)
        self.frameSession.pack(fill="both", expand=True)
        self.notebook.add(self.frameSession, text="Session")
        self.frameSession.columnconfigure(0, weight=1)
        self.frameSession.columnconfigure(1, weight=0)
        self.frameSession.columnconfigure(2, weight=0)
        self.frameSession.columnconfigure(3, weight=0)
        self.frameSession.columnconfigure(4, weight=1)
        self.frameSession.rowconfigure(0, weight=1)
        self.frameSession.rowconfigure(1, weight=0)
        self.frameSession.rowconfigure(2, weight=0)
        self.frameSession.rowconfigure(3, weight=0)
        self.frameSession.rowconfigure(4, weight=0)
        self.frameSession.rowconfigure(5, weight=0)
        self.frameSession.rowconfigure(6, weight=0)
        self.frameSession.rowconfigure(7, weight=0)
        self.frameSession.rowconfigure(8, weight=0)
        self.frameSession.rowconfigure(9, weight=3)
        ## Need to now create the page that asks the user to check all details etc or enter details
        # Open a PDF
        # Assign a password if needed
        # Create a Index or add to an existing one
        self.PDFPathStrVar.set(self.backend.checkPDFPath())
        self.PDFPasswordStrVar.set(self.backend.checkPDFPassword())
        self.IndexPathStrVar.set(self.backend.checkIndexPath())

        self.sessionTabPDFLabel = ttk.Label(self.frameSession, text=" PDF ", relief=tkinter.GROOVE, padding=2)
        self.sessionTabPDFLabel.grid(column=1,row=1, sticky="ew", columnspan=3)

        self.sessionTabPDFPathLabel = ttk.Label(self.frameSession, text=" Path ", relief=tkinter.GROOVE, padding=2)
        self.sessionTabPDFPathLabel.grid(column=1,row=2, sticky="ew")
        if not self.backend.checkPDFPath():
            self.PDFPathStrVar.set(" ...")
        self.sessionTabPDFPathValLabel = ttk.Label(self.frameSession, textvariable=self.PDFPathStrVar, relief=tkinter.GROOVE, width=60, padding=2)
        self.sessionTabPDFPathValLabel.grid(column=2,row=2, sticky="ew")
        self.sessionTabPDFButton = ttk.Button(self.frameSession, text="Add", command=self.addPDF)
        self.sessionTabPDFButton.grid(column=3,row=2, sticky="ew")

        self.sessionTabPDFPassLabel = ttk.Label(self.frameSession, text=" Password ", relief=tkinter.GROOVE, padding=2)
        self.sessionTabPDFPassLabel.grid(column=1,row=3, sticky="ew")
        if not self.backend.checkPDFPassword():
            self.PDFPasswordStrVar.set(" ...")
        self.sessionTabPDFPassValLabel = ttk.Label(self.frameSession, textvariable=self.PDFPasswordStrVar, relief=tkinter.GROOVE, width=20, padding=2)
        self.sessionTabPDFPassValLabel.grid(column=2,row=3, sticky="ew")
        self.sessionTabPDFPassButton = ttk.Button(self.frameSession, text="Add", command=self.addPDFPassword)
        self.sessionTabPDFPassButton.grid(column=3,row=3, sticky="ew")

        ttk.Label(self.frameSession, text="").grid(column=1,row=4, sticky="ew", columnspan=3)

        self.sessionTabIndexLabel = ttk.Label(self.frameSession, text=" Index ", relief=tkinter.GROOVE, padding=2)
        self.sessionTabIndexLabel.grid(column=1,row=5, sticky="ew", columnspan=3)
        
        self.sessionTabIndexPathLabel = ttk.Label(self.frameSession, text=" Path ", relief=tkinter.GROOVE, padding=2)
        self.sessionTabIndexPathLabel.grid(column=1,row=6, sticky="ew")
        if not self.backend.checkIndexPath():
            self.IndexPathStrVar.set(" ...")
        self.sessionTabIndexPathValLabel = ttk.Label(self.frameSession, textvariable=self.IndexPathStrVar, relief=tkinter.GROOVE, width=20, padding=2)
        self.sessionTabIndexPathValLabel.grid(column=2,row=6, sticky="ew")
        self.sessionTabIndexButton = ttk.Button(self.frameSession, text="Add", command=self.newIndex)
        self.sessionTabIndexButton.grid(column=3,row=6, sticky="ew")

        ttk.Label(self.frameSession, text="").grid(column=1,row=7, sticky="ew", columnspan=3)

        self.sessionTabFinishButton = ttk.Button(self.frameSession, text=" Finish Config ", command=self.openCheckSession)
        self.sessionTabFinishButton.grid(column=2,row=8, sticky="ew")

    def openMainTab(self):
        self.log.stack()
        self.frameMain = ttk.Frame(self.notebook, width=400, height=280)
        self.frameMain.pack(fill="both", expand=True)
        self.notebook.add(self.frameMain, text="Main")
        self.frameMain.columnconfigure(0, weight=0)
        self.frameMain.columnconfigure(1, weight=2)
        self.frameMain.columnconfigure(2, weight=3)
        self.frameMain.columnconfigure(3, weight=0)
        self.frameMain.rowconfigure(0, weight=0)
        self.frameMain.rowconfigure(1, weight=1)

        self.Mainpdfviewer = PDFViewer(self.frameMain)
        self.Mainpdfviewer.grid(column=1, row=0, rowspan=2, sticky="news")
        self.Mainpdfviewer.addSaveSettingFunc(self.backend.saveMAINzoom)

        self.textMain = readonlytext.ReadOnlyText(self.frameMain, font=('TkFixedFont bold', self.backend.appConfigManager.config["SETTINGS"]["fontSize"]))
        self.textMain.grid(column=2, row=1, sticky="news")
        
        self.MainControlsFrame = ttk.Frame(self.frameMain)
        self.MainPrevPage = ttk.Button(self.MainControlsFrame, text="Prev Page", command=self.prevPageMain)
        self.MainPrevPage.pack(fill="x", expand=True, side=tkinter.LEFT)
        self.MainNextPage = ttk.Button(self.MainControlsFrame, text="Next Page", command=self.nextPageMain)
        self.MainNextPage.pack(fill="x", expand=True, side=tkinter.LEFT)
        self.MainControlsFrame.grid(column=2, row=0, sticky="ew")

        self.indexrow = IndexRow(self.frameMain)
        self.indexrow.grid(column=3, row=0, rowspan=2, sticky="news")
        self.indexrow.addFunc(self.backend.addToIndex) # Binds the save to the right button

        self.menuPDF.add_command(label="Test Save", command=self.indexrow.save)
        self.textMain.bind("<e>", self.addTitleToIndexRow)
        self.textMain.bind("<q>", self.addDescToIndexRow)
        self.textMain.bind("<a>", self.prevPageMain)
        self.textMain.bind("<d>", self.nextPageMain)
        self.textMain.bind("<s>", self.indexrow.save)

    def openIndexTab(self):
        self.log.stack()
        self.frameIndex = ttk.Frame(self.notebook, width=400, height=280)
        self.frameIndex.pack(fill="both", expand=True)
        self.notebook.add(self.frameIndex, text="Index")

        self.indexText = tkinter.Text(self.frameIndex)
        self.indexText.pack(expand=True, fill="both")

    def openPDFTab(self):
        self.log.stack()
        self.framePDF = ttk.Frame(self.notebook)#, width=400, height=280)
        self.framePDF.pack(fill="both", expand=True)
        self.notebook.add(self.framePDF, text="PDF")
        
        self.PDFpdfviewer = PDFViewer(self.framePDF)
        self.PDFpdfviewer.pack(fill="both",expand=True)
        self.PDFpdfviewer.addSaveSettingFunc(self.backend.savePDFzoom)

    def openSearchTab(self):
        self.log.stack()
        self.frameSearch = ttk.Frame(self.notebook, width=400, height=280)
        self.frameSearch.pack(fill="both", expand=True)
        self.notebook.add(self.frameSearch, text="Search")
        self.button5 = ttk.Button(self.frameSearch, text="change Title", command=self.test)
        self.button5.pack()

    def openConfigTab(self):
        self.log.stack()
        self.frameConfig = ttk.Frame(self.notebook, width=400, height=280)
        self.frameConfig.pack(fill="both", expand=True)
        self.notebook.add(self.frameConfig, text="Config")
        self.button6 = ttk.Button(self.frameConfig, text="change Title", command=self.test)
        self.button6.pack()

    def closeTab(self, tabName):
        self.log.stack()
        total = self.notebook.index("end")
        for i in range(0, total):
            id = self.notebook.index(i)
            name = self.notebook.tab(id, "text")
            if name == tabName:
                self.notebook.forget(id)
                self.log.info(f"{tabName} Tab closed")
                return
        self.log.warning("No Tab matched to close")
    
    def checkTabOpen(self, tabName):
        self.log.stack()
        total = self.notebook.index("end")
        for i in range(0, total):
            id = self.notebook.index(i)
            name = self.notebook.tab(id, "text")
            if name == tabName:
                return True
        return False

    def openCheckSession(self):
        self.log.stack()
        ## Check if PDF has already been proccessed if so don't need to process again
        if self.backend.sessionConfigManager.config["PDF"]["numberOfBooks"] == "":
            self.openNewValidSession()
        else:
            self.openValidSession()

    def openNewValidSession(self):
        self.log.stack()
        if self.backend.checkSessionDetails():
            if self.checkTabOpen("Session"):
                self.closeTab("Session")
            self.openPDF()
            self.proccessPDF()
            self.backend.currentBook = 1
            self.backend.currentPage = 1
            self.openMainTab()
            self.openPDFTab()
            self.openIndexTab()

    def openValidSession(self):
        self.log.stack()
        if self.backend.checkSessionDetails():
            if self.checkTabOpen("Session"):
                self.closeTab("Session")
            self.openPDF()
            self.openMainTab()
            self.openPDFTab()
            self.openIndexTab()

    def openTXTFile(self, event=None) -> None:
        self.log.stack()
        self.log.info("Open a Text file")
        with filedialog.askopenfile(mode="r") as file:
            fileName = os.path.basename(file.name)
            self.openTabs[fileName] = [ttk.Frame(self.notebook, width=400, height=280), None, None]
            self.openTabs[fileName][0].pack(fill="both", expand=True)
            self.notebook.add(self.openTabs[fileName][0], text=fileName)
            self.openTabs[fileName][1] = tkinter.Text(self.openTabs[fileName][0], bg="#26242f", fg="white", font=('TkFixedFont bold', 12))
            self.openTabs[fileName][1].pack(side=tkinter.LEFT, fill="both", expand=True)
            self.openTabs[fileName][1].insert(0.0, file.read())
            self.openTabs[fileName][2] = ttk.Scrollbar(self.openTabs[fileName][0], orient=tkinter.VERTICAL, command=self.openTabs[fileName][1].yview)
            self.openTabs[fileName][2].pack(side=tkinter.LEFT, fill="y", expand=True)
            self.openTabs[fileName][1]["yscrollcommand"] = self.openTabs[fileName][2].set

    def openSession(self, event=None) -> None:
        self.log.stack()
        self.log.info("Openning a Session")
        session = filedialog.askdirectory(mustexist=True, title="Select A Session Folder")
        if session != "":
            sessionName = os.path.basename(session)
            self.backend.openSession(sessionName)
            self.root.title(f"PDF Indexer. Current Session: {self.backend.currentSession}")
            self.PDFPathStrVar.set(self.backend.checkPDFPath())
            self.PDFPasswordStrVar.set(self.backend.checkPDFPassword())
            self.IndexPathStrVar.set(self.backend.checkIndexPath())
            if self.checkTabOpen("Welcome"):
                self.closeTab("Welcome")
            self.openSessionTab()

    def closeSession(self, event=None) -> None:
        self.log.stack()
        self.log.info("Closing a Session")
        self.backend.closeSession()
        try:
            self.root.title("PDF Indexer.")
        except:
            self.log.exception("Ignore if on close")

    def newSession(self, event=None) -> None: ############# Look at this then calling open session or a 3rd function both call to reduce duplicate code
        self.log.stack()
        self.log.info("New Session")
        sessionName = simpledialog.askstring(title="New Session", prompt="New Session Name:")
        if sessionName != None:
            self.backend.closeSession()
            self.backend.newSession(sessionName)
            self.root.title(f"PDF Indexer. Current Session: {self.backend.currentSession}")
            self.PDFPathStrVar.set(self.backend.checkPDFPath())
            self.PDFPasswordStrVar.set(self.backend.checkPDFPassword())
            self.IndexPathStrVar.set(self.backend.checkIndexPath())
            if self.checkTabOpen("Welcome"):
                self.closeTab("Welcome")
            self.openSessionTab()

    def addPDF(self, event=None) -> None:
        self.log.stack()
        self.log.info("Add a PDF file to session")
        filePath:str = filedialog.askopenfilename()
        self.backend.addPDFPath(filePath)
        self.PDFPathStrVar.set(self.backend.checkPDFPath())
        ## Add info the PDF TAB here

    def addPDFPassword(self, event=None) -> None:
        self.log.stack()
        self.log.info("Ask for PDF Password Session")
        password = simpledialog.askstring(title="PDF Password", prompt="PDF Password:")
        self.backend.addPDFPassword(password)
        self.PDFPasswordStrVar.set(self.backend.checkPDFPassword())

    def openPDF(self, event=None) -> None:
        self.log.stack()
        if self.backend.currentSession == "":
            self.log.error("No Open Session can't open PDF")
            return
        elif self.backend.sessionConfigManager.config["PDF"]["filepath"] == "":
            self.log.error("No PDF to open")
            return
        self.backend.openPDF()

    def proccessPDF(self, event=None) -> None:
        self.log.stack()
        if self.backend.currentSession == "":
            self.log.error("No Open Session can't open PDF")
            return
        elif self.backend.sessionConfigManager.config["PDF"]["filepath"] == "":
            self.openPDF()
        self.log.info("Proccess PDF")
        self.backend.prepPDF()

    def updateMain(self, event=None) -> None:
        self.log.stack()
        self.textMain.delete("1.0", tkinter.END)
        self.textMain.insert(tkinter.END, self.backend.getPageText())
        self.Mainpdfviewer.addPixmap(self.backend.getPagePixmap())
        self.log.info("Update Main Tab")

    def updateIndex(self, event=None):
        self.log.stack()
        self.log.info("Changed to Index")
        self.indexText.delete(0.0, tkinter.END)
        tmp = ""
        for line in self.backend.index:
            tmp += f"{line}\n"
        self.indexText.insert(tkinter.END, tmp)
    
    def notebookTABChange(self, event=None) -> None:
        self.log.stack()
        currentTab = self.getCurrentTab()
        match currentTab:
            case "Welcome":
                pass
            case "Main":
                self.updateMain()
            case "Index":
                self.updateIndex()
            case _:
                self.log.info(f"Switched to {currentTab}")

    def resize(self, event=None) -> None:
        #self.log.stack() #too many calls
        if(event.widget == self.root and
           (self.width != event.width or self.height != event.height)):
            self.width, self.height = event.width, event.height
            currentTab = self.getCurrentTab()
            match currentTab:
                case "Welcome":
                    pass
                case "Main":
                    #self.updateMainImage()
                    pass
                case _:
                    self.log.info(f"Resized")

    def getCurrentTab(self) -> str:
        self.log.stack()
        return self.notebook.tab(self.notebook.select(), "text")

    def pdfSetup(self, event=None):
        self.log.stack()
        self.openPDF()
        if self.mainPixmap == None:
            self.mainPixmap = self.backend.getPagePixmap()
        self.PDFpdfviewer.addPixmap(self.mainPixmap)

    def nextPageMain(self, event=None):
        self.log.stack()
        self.backend.nextPage()
        self.updateMain()

    def prevPageMain(self, event=None):
        self.log.stack()
        self.backend.prevPage()
        self.updateMain()

    def test(self, event=None):
        self.log.stack()
        self.log.info("Test Run")
        self.indexrow.save()
    
    def testAdd(self, event=None):
        self.log.stack()
        self.indexrow.addInfo(1,1,"Testing")
        self.indexrow.addDesc("Test Desc")

    def addTitleToIndexRow(self, event=None):
        self.log.stack()
        tmp = self.textMain.selection_get()
        if not self.indexrow.bookAdded:
            self.indexrow.addBook(self.backend.currentBook)
            self.indexrow.addPage(self.backend.currentPage)
            self.indexrow.bookAdded = True
        self.indexrow.addTitle(tmp)

    def addDescToIndexRow(self, event=None):
        self.log.stack()
        tmp = self.textMain.selection_get()
        self.indexrow.addDesc(tmp)

    def newIndex(self, event=None):
        self.log.stack()
        indexName = simpledialog.askstring(title="Index Name", prompt="Title for index:")
        self.backend.newIndex(indexName)
        self.IndexPathStrVar.set(self.backend.checkIndexPath())
        pass # Create a dialog to make a new index
    def saveIndex(self, event=None):
        self.log.stack()
        self.backend.saveIndex()
    def openIndex(self, event=None):
        self.log.stack()
        pass # Create a dialog to open a index
    def closeIndex(self, event=None):
        self.log.stack()
        pass # close the current index
    
if __name__ == "__main__":
    app = App()
    app.run()