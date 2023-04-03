import fitz
import configMan
import os
import csv

class Backend:
    def __init__(self) -> None:
        self.resetVariables()

        print("A - INFO  - Starting")

        self.appConfigManager = configMan.AppConfig("config.ini")
        
        self.openLastSession()
        
    def resetVariables(self):
        self.pdf:fitz.Document
        self.isPDFLoaded:bool = False
        self.offsets = {}
        self.currentSession:str = ""
        self.index = []
        self.currentPage = None
        self.currentBook = None
        self.sessionConfigManager:configMan.SessionConfig

    def __del__(self) -> None:
        self.closeSession()
        try:
            self.closePDF()
        except AttributeError:
            print("P - ERROR - Error on closing PDF on program exit Att ERROR")
        except ValueError as err:
            if err.__str__() != "document closed":
                print("P - ERROR - Error on closing PDF on program exit VAL EEROR")
                print(err)
        print("A - INFO  - Exited")
    
    def newSession(self, sessionName) -> None:
        print(f"S - INFO  - Creating Session {sessionName}")
        if os.path.exists(sessionName): ## This will only work once then will error need try except eventually
            print("S - WARN  - Session already exists adding -new")
            sessionName += "-new"
        if self.currentSession != "":
            self.closeSession()
        self.resetVariables()
        os.mkdir(sessionName)
        self.openSession(sessionName)
        self.sessionConfigManager.config["DETAILS"]["lastPage"] = str(1)
        self.sessionConfigManager.config["DETAILS"]["lastBook"] = str(1)

    def openSession(self, sessionName) -> None:
        self.resetVariables()
        if os.path.exists(sessionName):
            configFilePath = f"{sessionName}/index.ini"
            self.sessionConfigManager = configMan.SessionConfig(configFilePath)
            self.currentSession = sessionName
            self.currentPage = int(self.sessionConfigManager.config["DETAILS"]["lastPage"])
            self.currentBook = int(self.sessionConfigManager.config["DETAILS"]["lastBook"])
            self.openPDF()
            self.loadIndex()
            print(f"current Page and Book: {self.currentPage}, {self.currentBook}")
            print(f"S - INFO  - Session {sessionName} Openned")
        else:
            print(f"S - WARN  - Session {sessionName} Does not exist")
            self.appConfigManager.config["APP"]["lastSession"] = ""
            self.appConfigManager.save()
            self.currentSession = ""

    def openLastSession(self):
        if self.currentSession == "":
            lastSession = self.appConfigManager.config["APP"]["lastSession"]
            if lastSession != "":
                self.openSession(lastSession)

    def closeSession(self) -> None:
        if self.currentSession != "":
            print(f"current Page and Book: {self.currentPage}, {self.currentBook}")
            self.sessionConfigManager.config["DETAILS"]["lastPage"] = str(self.currentPage)
            self.sessionConfigManager.config["DETAILS"]["lastBook"] = str(self.currentBook)
            self.sessionConfigManager.save()
            self.appConfigManager.config["APP"]["lastSession"] = self.currentSession
            self.appConfigManager.save()
            self.saveIndex()
            print(f"S - INFO  - Session {self.currentSession} closed")
            self.resetVariables()
    
    def addPDFPath(self, path) -> None:
        self.sessionConfigManager.config["PDF"]["filePath"] = path
        self.sessionConfigManager.save()
        print("P - INFO  - PDF path added to session")

    def addPDFPassword(self, password) -> None:
        self.sessionConfigManager.config["PDF"]["password"] = password
        self.sessionConfigManager.save()
        print(password)
        print("P - INFO  - PDF password added to session")

    def openPDF(self) -> None:
        self.pdf = fitz.Document(self.sessionConfigManager.config["PDF"]["filePath"])
        print( f"Pasword to use: {self.sessionConfigManager.config['PDF']['password']} ")
        self.pdf.authenticate(self.sessionConfigManager.config["PDF"]["password"])
        self.isPDFLoaded = True
        print("P - INFO  - PDF Opened")

    def closePDF(self) -> None:
        if self.isPDFLoaded:
            self.pdf.close()
            self.isPDFLoaded = False
            print("P - INFO  - PDF Closed")
    
    def prepPDF(self) -> None:
        if self.isPDFLoaded:
            print("P - INFO  - Processing PDF")
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
            print("p - INFO  - Processed PDF")
        else:
            print("p - WARN  - Need to open a PDF 1st")
    
    def newIndex(self, indexName=None) -> None:
        if indexName == None:
            indexName = self.sessionConfigManager.config["PDF"]["bookSetName"]
        if ".csv" not in indexName:
            indexName = f"{indexName}.csv"
        if f"{self.currentSession}/" not in indexName:
            indexName = f"{self.currentSession}/{indexName}"
        print(f"I - INFO  - {indexName} Created")
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
            print(f"I - INFO  - {csvpath} openned")
        else:
            print(f"I - WARN  - {csvpath} Does not exist making now")
            self.newIndex(csvpath)
    
    def saveIndex(self) -> None:
        csvpath = self.sessionConfigManager.config["INDEX"]["filePath"]
        if csvpath != None or csvpath != "":
            if not os.path.exists(csvpath):
                print(f"I - WARN  - {csvpath} Does not exist making now. this is weird")
            with open(csvpath, "w", newline="") as file:
                writer = csv.writer(file, quoting=csv.QUOTE_ALL)
                writer.writerow(["Title", "Desc", "Page", "Book"])
                writer.writerows(self.index)
            print(f"I - INFO  - {csvpath} Saved")

    def addToIndex(self, title, desc, page, book):
        title = ''.join(i for i in title if ord(i)<128)
        desc = ''.join(i for i in desc if ord(i)<128)
        self.index.append([title, desc, page, book])
        print(f"I - INFO  - {book}/{page} {title} added to index")

    def getEntriesRefBook(self, book) -> list:
        print(f"I - INFO  - Search for Entries in book:{book}")
        tmp = []
        for line in self.index:
            if book == line[3]:
                tmp.append(line)
        return tmp
    
    def getEntriesRefBookAndPage(self, book, page) -> list:
        print(f"I - INFO  - Search for Entries in book:{book} page:{page}")
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
        print(f"P - INFO  - Getting Page {convertedNumber + 1} from pdf")
        page:fitz.Page = self.pdf.load_page(convertedNumber)
        return page.get_text()
    
    def getPagePixmap(self, bookNum=None, pageNum=None) -> str:
        if bookNum == None and pageNum == None:
            bookNum = self.currentBook
            pageNum = self.currentPage
        bookName = self.sessionConfigManager.config["BOOKS"][str(bookNum)]
        convertedNumber = int(self.sessionConfigManager.config[bookName]["offset"]) + pageNum
        print(f"P - INFO  - Getting Page Pixmap {convertedNumber + 1} from pdf")
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
        print(f"ZOOM PDF to be save: {zoom}")
        self.sessionConfigManager.config["DETAILS"]["zoomPDF"] = str(zoom)
        self.sessionConfigManager.save()
    def saveMAINzoom(self, zoom):
        print(f"ZOOM Main to be save: {zoom}")
        self.sessionConfigManager.config["DETAILS"]["zoomMain"] = str(zoom)
        self.sessionConfigManager.save()
