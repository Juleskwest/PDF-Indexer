import fitz
import configMan
import os
import csv
from logger import Logger

class Backend:
    def __init__(self) -> None:
        self.resetVariables()
        self.logger = Logger(__name__)
        self.logger.info("Starting backend")

        self.appConfigManager = configMan.AppConfig("config.ini")
        
        self.openLastSession()
        
    def resetVariables(self):
        self.pdf:fitz.Document = None
        self.isPDFLoaded:bool = False
        self.offsets = {}
        self.currentSession:str = ""
        self.index = []
        self.currentPage = None
        self.currentBook = None
        self.sessionConfigManager:configMan.SessionConfig = None

    def __del__(self) -> None:
        self.closeSession()
        try:
            self.closePDF()
        except AttributeError:
            self.logger.info("Error on closing PDF on program exit Att ERROR")
        except ValueError as err:
            if err.__str__() != "document closed":
                self.logger.exception("Error on closing PDF on program exit VAL EEROR")
        self.logger.info("Backend Exited")
    
    def newSession(self, sessionName) -> None:
        self.logger.info(f"Creating Session {sessionName}")
        if os.path.exists(sessionName): ## This will only work once then will error need try except eventually
            self.logger.info("Session already exists adding -new")
            sessionName += "-new"
        if self.currentSession != "":
            self.closeSession()
        os.mkdir(sessionName)
        #self.openSession(sessionName) # Might need to do what we want here not try open etc
        configFilePath = f"{sessionName}/index.ini"
        self.sessionConfigManager = configMan.SessionConfig(configFilePath)
        self.currentSession = sessionName
        self.sessionConfigManager.config["DETAILS"]["lastPage"] = str(1)
        self.sessionConfigManager.config["DETAILS"]["lastBook"] = str(1)
        #self.newIndex()

    def openSession(self, sessionName) -> None:
        self.resetVariables()
        if os.path.exists(sessionName):
            configFilePath = f"{sessionName}/index.ini"
            self.sessionConfigManager = configMan.SessionConfig(configFilePath)
            self.currentSession = sessionName
            if self.checkSessionDetails():
                self.currentPage = int(self.sessionConfigManager.config["DETAILS"]["lastPage"])
                self.currentBook = int(self.sessionConfigManager.config["DETAILS"]["lastBook"])
                self.openPDF()
                self.loadIndex()
                self.logger.info(f"current Page and Book: {self.currentPage}, {self.currentBook}")
                self.logger.info(f"Session {sessionName} Openned")
        else:
            self.logger.warning(f"Session {sessionName} Does not exist")
            self.appConfigManager.config["APP"]["lastSession"] = ""
            self.appConfigManager.save()
            self.currentSession = ""

    def openLastSession(self):
        if self.currentSession == "":
            lastSession = self.appConfigManager.config["APP"]["lastSession"]
            if lastSession != "":
                self.openSession(lastSession)

    def closeSession(self) -> None:
        if self.currentSession != "" and self.checkSessionDetails():
            self.logger.info(f"current Page and Book: {self.currentPage}, {self.currentBook}")
            self.sessionConfigManager.config["DETAILS"]["lastPage"] = str(self.currentPage)
            self.sessionConfigManager.config["DETAILS"]["lastBook"] = str(self.currentBook)
            self.sessionConfigManager.save()
            self.appConfigManager.config["APP"]["lastSession"] = self.currentSession
            self.appConfigManager.save()
            self.saveIndex()
            self.logger.info(f"Session {self.currentSession} closed")
            self.resetVariables()
    
    def addPDFPath(self, path) -> None:
        self.sessionConfigManager.config["PDF"]["filePath"] = path
        self.sessionConfigManager.save()
        self.logger.info("PDF path added to session")

    def addPDFPassword(self, password) -> None:
        self.sessionConfigManager.config["PDF"]["password"] = password
        self.sessionConfigManager.save()
        self.logger.info("PDF password added to session")

    def openPDF(self) -> None:
        self.pdf = fitz.Document(self.sessionConfigManager.config["PDF"]["filePath"])
        self.logger.info( f"Pasword to use: {self.sessionConfigManager.config['PDF']['password']} ")
        self.pdf.authenticate(self.sessionConfigManager.config["PDF"]["password"])
        self.isPDFLoaded = True
        self.logger.info("PDF Opened")

    def closePDF(self) -> None:
        if self.isPDFLoaded:
            self.pdf.close()
            self.isPDFLoaded = False
            self.logger.info("PDF Closed")
    
    def prepPDF(self) -> None:
        if self.isPDFLoaded:
            self.logger.info("Processing PDF")
            bookslist = []
            tmp = self.pdf.get_toc()
            for line in tmp:
                if "Book" in line[1]:
                    bookslist.append(line)
            self.sessionConfigManager.config["PDF"]["numberOfBooks"] = str(len(bookslist))
            for i, line in enumerate(bookslist):
                bookinfo = line[1].split()[1]
                self.sessionConfigManager.config["PDF"]["bookSetName"] = bookinfo.split('.')[0]
                self.sessionConfigManager.config["BOOKS"][str(i+1)] = bookinfo
                self.sessionConfigManager.config[bookinfo] = {}
                if i != (len(bookslist) - 1):
                    self.sessionConfigManager.config[bookinfo]["pages"] = str(bookslist[i+1][2] - line[2])
                else:
                    self.sessionConfigManager.config[bookinfo]["pages"] = str(self.pdf.page_count - line[2])
                self.sessionConfigManager.config[bookinfo]["offset"] = str(line[2])
            self.sessionConfigManager.save()
            self.logger.info("Processed PDF")
        else:
            self.logger.info("Need to open a PDF 1st")
    
    def newIndex(self, indexName=None) -> None:
        if indexName == None:
            indexName = self.sessionConfigManager.config["PDF"]["bookSetName"]
        if ".csv" not in indexName:
            indexName = f"{indexName}.csv"
        if f"{self.currentSession}/" not in indexName:
            indexName = f"{self.currentSession}/{indexName}"
        self.logger.info(f"{indexName} Created")
        self.sessionConfigManager.config["INDEX"]["filePath"] = indexName
        self.sessionConfigManager.save()
        with open(self.sessionConfigManager.config["INDEX"]["filePath"], "w", newline="") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow(["Title", "Desc", "Page", "Book"])

    def loadIndex(self) -> None:
        csvpath = self.sessionConfigManager.config["INDEX"]["filePath"]
        if os.path.exists(csvpath):
            self.index = []
            with open(csvpath, "r") as file:
                reader = csv.reader(file)
                for line in reader:
                    if line[0] != "Title" and line[1] != "Desc":
                        line = [line[0], line[1], int(line[2]), int(line[3])]
                        self.index.append(line)
            self.logger.info(f"{csvpath} openned")
        else:
            self.logger.info(f"{csvpath} Does not exist making now")
            if csvpath != "":
                self.newIndex(csvpath)
            else:
                self.newIndex()
    
    def saveIndex(self) -> None:
        csvpath = self.sessionConfigManager.config["INDEX"]["filePath"]
        if csvpath != None or csvpath != "":
            if not os.path.exists(csvpath):
                self.logger.info(f"{csvpath} Does not exist making now. this is weird")
            with open(csvpath, "w", newline="") as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                writer.writerow(["Title", "Desc", "Page", "Book"])
                writer.writerows(self.index)
            self.logger.info(f"{csvpath} Saved")

    def addToIndex(self, title, desc, page, book):
        title = ''.join(i for i in title if ord(i)<128)
        desc = ''.join(i for i in desc if ord(i)<128)
        self.index.append([title, desc, page, book])
        self.logger.info(f"{book}/{page} {title} added to index")

    def getEntriesRefBook(self, book) -> list:
        self.logger.info(f"Search for Entries in book:{book}")
        tmp = []
        for line in self.index:
            if book == line[3]:
                tmp.append(line)
        return tmp
    
    def getEntriesRefBookAndPage(self, book, page) -> list:
        self.logger.info(f"Search for Entries in book:{book} page:{page}")
        tmp = []
        for line in self.index:
            if book == line[3] and page == line[2]:
                tmp.append(line)
        return tmp
    
    def getPageText(self, bookNum=None, pageNum=None) -> str:
        if bookNum == None and pageNum == None:
            bookNum = self.currentBook
            pageNum = self.currentPage
        bookName = self.sessionConfigManager.config["BOOKS"][str(bookNum)]
        convertedNumber = int(self.sessionConfigManager.config[bookName]["offset"]) + pageNum
        self.logger.info(f"Getting Page {convertedNumber + 1} from pdf")
        page:fitz.Page = self.pdf.load_page(convertedNumber)
        return page.get_text()
    
    def getPagePixmap(self, bookNum=None, pageNum=None) -> str:
        if bookNum == None and pageNum == None:
            bookNum = self.currentBook
            pageNum = self.currentPage
        bookName = self.sessionConfigManager.config["BOOKS"][str(bookNum)]
        convertedNumber = int(self.sessionConfigManager.config[bookName]["offset"]) + pageNum
        self.logger.info(f"Getting Page Pixmap {convertedNumber + 1} from pdf")
        page:fitz.Page = self.pdf.load_page(convertedNumber)
        zoom = 2    # zoom factor
        mat = fitz.Matrix(zoom, zoom)
        return page.get_pixmap(matrix=mat)
    
    def getCurrentPage(self):
        return self.currentPage
    
    def getCurrentBook(self):
        return self.currentBook
    
    def nextPage(self):
        self.currentPage += 1

    def prevPage(self):
        self.currentPage -= 1

    def getMAINzoom(self):
        return float(self.sessionConfigManager.config["DETAILS"]["zoomMain"])
    def getPDFzoom(self):
        return float(self.sessionConfigManager.config["DETAILS"]["zoomPDF"])
    def savePDFzoom(self, zoom):
        self.logger.info(f"ZOOM PDF to be save: {zoom}")
        self.sessionConfigManager.config["DETAILS"]["zoomPDF"] = str(zoom)
        self.sessionConfigManager.save()
    def saveMAINzoom(self, zoom):
        self.logger.info(f"ZOOM Main to be save: {zoom}")
        self.sessionConfigManager.config["DETAILS"]["zoomMain"] = str(zoom)
        self.sessionConfigManager.save()

    def checkSessionDetails(self):
        if self.checkPDFPath() and self.checkIndexPath():
            print("True The details etc")
            return True
        return False
    
    def checkPDFPath(self):
        potentialPath = self.sessionConfigManager.config["PDF"]["filePath"]
        if potentialPath != "" and potentialPath != None:
            print(f"PDF path: {potentialPath}")
            return potentialPath
        return False
    
    def checkPDFPassword(self):
        potentialPassword = self.sessionConfigManager.config["PDF"]["password"]
        if potentialPassword != "":
            return potentialPassword
        return False
    
    def checkIndexPath(self):
        potentialPath = self.sessionConfigManager.config["INDEX"]["filePath"]
        if potentialPath != "" and potentialPath != None:
            print(f"Index path: {potentialPath}")
            return potentialPath
        return False