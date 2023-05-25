import tkinter
from tkinter import ttk
from PIL import Image, ImageTk
from logger import Logger

class PDFViewer(ttk.Frame):
    def __init__(self, master=None, **kw):
        self.pixmap = kw.pop('pixmap', None)
        self.image = kw.pop('image', None)
        self.width = kw.pop('width', None)
        self.height = kw.pop('height', None)
        self.zoomlevel = kw.pop('zoom', None)
        super(PDFViewer, self).__init__(master=master, **kw)
        self.log = Logger(__name__)
        self.log.stack()
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=0)
        self.columnconfigure(3, weight=0)
        self.columnconfigure(4, weight=0)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)

        if self.pixmap != None:
            self.proccessPixmap()

        self.pdfButtonZoomIn = ttk.Button(self, text="Zoom In", command=self.zoomIn)
        self.pdfButtonZoomIn.grid(column=1,row=0, sticky="news")
        self.pdfButtonZoomOut = ttk.Button(self, text="Zoom Out", command=self.zoomOut)
        self.pdfButtonZoomOut.grid(column=2,row=0, sticky="news")
        self.pdfButtonZoomLevel = ttk.Button(self, text="Zoom Level")
        self.pdfButtonZoomLevel.grid(column=3,row=0, columnspan=2, sticky="news")

        self.pdfCanvas = tkinter.Canvas(self, relief=tkinter.SUNKEN)
        if self.width != None and self.height != None:
            self.pdfCanvas.config(width=self.width, height=self.height)
        self.pdfCanvas.config(highlightthickness=0)
        self.pdfCanvas.grid(column=0,row=1,columnspan=4, sticky="news")

        self.pdfScrollVert = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        self.pdfScrollVert.config(command=self.pdfCanvas.yview)
        self.pdfCanvas.config(yscrollcommand=self.pdfScrollVert.set)
        self.pdfScrollVert.grid(column=4,row=1, sticky="ns")

        self.pdfScrollHori = tkinter.Scrollbar(self, orient=tkinter.HORIZONTAL)
        self.pdfScrollHori.config(command=self.pdfCanvas.xview)
        self.pdfCanvas.config(xscrollcommand=self.pdfScrollHori.set)
        self.pdfScrollHori.grid(column=0,row=2,columnspan=4, sticky="ew")

        self.pdfLabel = ttk.Label(self, text="PDF Viewer")
        self.pdfLabel.grid(column=0,row=3,columnspan=5, sticky="news")

        if self.image != None:
            self.image = ImageTk.PhotoImage(self.image)
            self.update()

        self.bind("<Enter>", self._bindMouseWheel)
        self.bind("<Leave>", self._unbindMouseWheel)

        self.bind("<Configure>", self.resize)
        self.rewidth, self.reheight = 0,0

        self.zoomlevel = 1.0

    def addSaveSettingFunc(self, func):
        self.log.stack()
        self.func = func

    def saveSettings(self):
        self.log.stack()
        self.func(self.zoomlevel)

    def proccessPixmap(self):
        self.log.stack()
        self.log.info(self.zoomlevel)
        mode = "RGBA" if self.pixmap.alpha else "RGB"
        img = Image.frombytes(mode, [self.pixmap.width, self.pixmap.height], self.pixmap.samples)
        width = int(self.pixmap.width * self.zoomlevel)
        height = int(self.pixmap.height * self.zoomlevel)
        size = (width, height)
        resizedImage = img.resize(size, Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resizedImage)

    def _bindMouseWheel(self, event):
        #self.log.stack() # Too many messages
        #self.log.info("Bound")
        self.bind_all("<MouseWheel>", self._onMouseWheelVert)
        self.bind_all("<Shift-MouseWheel>", self._onMouseWheelHori)
        self.bind_all("<Control-MouseWheel>", self._onMouseWheelZoom)
    
    def _unbindMouseWheel(self, event):
        #self.log.stack() # Too many messages
        #self.log.info("unBound")
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Shift-MouseWheel>")
        self.unbind_all("<Control-MouseWheel>")
    
    def _onMouseWheelVert(self, event=None):
        self.log.stack()
        val = -1*(event.delta/120)
        self.pdfCanvas.yview_scroll(int(val), "units")
    
    def _onMouseWheelHori(self, event=None):
        self.log.stack()
        val = -1*(event.delta/120)
        self.pdfCanvas.xview_scroll(int(val), "units")

    def _onMouseWheelZoom(self, event=None):
        self.log.stack()
        val = -1*(event.delta/120)
        if val > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def test(self):
        self.log.stack()
        self.log.info("from pdf viewer class")

    def addImage(self, image):
        self.log.stack()
        self.image = ImageTk.PhotoImage(image)
        self.update()
        
    def addPixmap(self, pixmap):
        self.log.stack()
        self.pixmap = pixmap
        self.proccessPixmap()
        self.update()
    
    def update(self, width=None, height=None):
        self.log.stack()
        self.pdfCanvas.delete("all")
        if width == None and height == None:
            width = self.pdfCanvas.winfo_width()
            height = self.pdfCanvas.winfo_height()
        width = int(width/2)
        height = int(height/2)
        self.pdfCanvas.create_image(width,height, anchor=tkinter.CENTER, image=self.image)
        self.pdfCanvas.config(scrollregion=self.pdfCanvas.bbox(tkinter.ALL))
        self.saveSettings()
    
    def resize(self, event=None):
        self.log.stack()
        if(event.widget == self and (self.rewidth != event.width or self.reheight != event.height)):
            self.log.info(f'T - INFO  - Canvas {event.widget}: {event.height}, {event.width}')
            self.rewidth, self.reheight = event.width, event.height
            self.update(event.width, event.height)
        
    def zoomIn(self, event=None):
        self.log.stack()
        self.zoomlevel += 0.1
        self.proccessPixmap()
        self.update()

    def zoomOut(self, event=None):
        self.log.stack()
        self.zoomlevel -= 0.1
        self.proccessPixmap()
        self.update()