import tkinter
from tkinter import ttk
from logger import Logger


class IndexRow(ttk.Frame):
    def __init__(self, master=None, **kw):
        self.width = kw.pop('width', None)
        self.height = kw.pop('height', None)
        super(IndexRow, self).__init__(master=master, **kw)
        self.logger = Logger(__name__)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=0)

        self.bookLabel = ttk.Label(self, text="Book:")
        self.bookLabel.grid(column=0, row=0, sticky="ew")
        self.bookText = tkinter.Text(self, width=15, height=1)
        self.bookText.grid(column=1, row=0, sticky="ew")

        self.pageLabel = ttk.Label(self, text="Page:")
        self.pageLabel.grid(column=2, row=0, sticky="ew")
        self.pageText = tkinter.Text(self, width=15, height=1)
        self.pageText.grid(column=3, row=0, sticky="ew")

        self.titleLabel = ttk.Label(self, text="Title:")
        self.titleLabel.grid(column=0,columnspan=4,row=1, sticky="ew")
        self.titleText = tkinter.Text(self, width=30, height=3)
        self.titleText.grid(column=0,columnspan=4,row=2, sticky="news")

        self.descLabel = ttk.Label(self, text="Desc:")
        self.descLabel.grid(column=0,columnspan=4,row=3, sticky="ew")
        self.descText = tkinter.Text(self, width=30)
        self.descText.grid(column=0,columnspan=4,row=4, sticky="news")

        self.saveButton = ttk.Button(self, text="Save", command=self.save)
        self.saveButton.grid(column=0,columnspan=2, row=5, sticky="ew")
        self.clearButton = ttk.Button(self, text="Clear", command=self.clear)
        self.clearButton.grid(column=2,columnspan=2, row=5, sticky="ew")

        self.func = None
        self.bookAdded = False

    def addFunc(self, func):
        self.func = func

    def save(self, event=None):
        #title, desc, page, book
        title = self.titleText.get(0.0, tkinter.END).replace("\n", " ")
        desc = self.descText.get(0.0, tkinter.END).replace("\n", " ")
        page = self.pageText.get(0.0, tkinter.END).replace("\n", " ")
        book = self.bookText.get(0.0, tkinter.END).replace("\n", " ")
        self.func(title, desc, page, book)
        self.clear()
        
    def clear(self, event=None):
        self.bookText.delete(0.0, tkinter.END)
        self.pageText.delete(0.0, tkinter.END)
        self.titleText.delete(0.0, tkinter.END)
        self.descText.delete(0.0, tkinter.END)
        self.bookAdded = False
        
    def addBook(self, book):
        self.bookText.insert(tkinter.END, str(book))
    def addPage(self, page):
        self.pageText.insert(tkinter.END, str(page))
    def addTitle(self, title:str):
        tmp = title.replace("\n", " ")
        self.titleText.insert(tkinter.END, tmp)

    def addDesc(self, desc:str):
        tmp = desc.replace("\n", " ")
        self.descText.insert(tkinter.END, tmp)

    def addInfo(self, book, page, title):
        print(f"self.boodAdded = False: {self.bookAdded}")
        if not self.bookAdded:
            print(f"self.boodAdded = False: {self.bookAdded}")
            self.addBook(book)
            self.addPage(page)
            self.bookAdded = True
        self.addTitle(title)