import tkinter
from tkinter import ttk
from PIL import Image, ImageTk

class PDFViewer(ttk.Frame):
    def __init__(self, master=None, **kw):
        self.pixmap = kw.pop('pixmap', None)
        self.image = kw.pop('image', None)
        self.width = kw.pop('width', None)
        self.height = kw.pop('height', None)
        self.zoomlevel = kw.pop('zoom', None)
        super(PDFViewer, self).__init__(master=master, **kw)
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
        self.func = func

    def saveSettings(self):
        self.func(self.zoomlevel)

    def proccessPixmap(self):
        print(self.zoomlevel)
        mode = "RGBA" if self.pixmap.alpha else "RGB"
        img = Image.frombytes(mode, [self.pixmap.width, self.pixmap.height], self.pixmap.samples)
        width = int(self.pixmap.width * self.zoomlevel)
        height = int(self.pixmap.height * self.zoomlevel)
        size = (width, height)
        resizedImage = img.resize(size, Image.LANCZOS)
        self.image = ImageTk.PhotoImage(resizedImage)

    def _bindMouseWheel(self, event):
        print("Bound")
        self.bind_all("<MouseWheel>", self._onMouseWheelVert)
        self.bind_all("<Shift-MouseWheel>", self._onMouseWheelHori)
        self.bind_all("<Control-MouseWheel>", self._onMouseWheelZoom)
    
    def _unbindMouseWheel(self, event):
        print("unBound")
        self.unbind_all("<MouseWheel>")
        self.unbind_all("<Shift-MouseWheel>")
        self.unbind_all("<Control-MouseWheel>")
    
    def _onMouseWheelVert(self, event=None):
        val = -1*(event.delta/120)
        self.pdfCanvas.yview_scroll(int(val), "units")
    
    def _onMouseWheelHori(self, event=None):
        val = -1*(event.delta/120)
        self.pdfCanvas.xview_scroll(int(val), "units")

    def _onMouseWheelZoom(self, event=None):
        val = -1*(event.delta/120)
        if val > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def test(self):
        print("from pdf viewer class")

    def addImage(self, image):
        self.image = ImageTk.PhotoImage(image)
        self.update()
        
    def addPixmap(self, pixmap):
        self.pixmap = pixmap
        self.proccessPixmap()
        self.update()
    
    def update(self, width=None, height=None):
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
        if(event.widget == self and (self.rewidth != event.width or self.reheight != event.height)):
            print(f'T - INFO  - Canvas {event.widget}: {event.height}, {event.width}')
            self.rewidth, self.reheight = event.width, event.height
            self.update(event.width, event.height)
            # resize here
            # if size is smaller than canvas cut canvas to image size else cut canvas to match view port and move image to center
        
    def zoomIn(self, event=None):
        self.zoomlevel += 0.1
        self.proccessPixmap()
        self.update()
        pass #will have to resize the image will pillow and update label/selection box

    def zoomOut(self, event=None):
        self.zoomlevel -= 0.1
        self.proccessPixmap()
        self.update()
        pass # will have to resize the image with pillow and update label


class App:
    def __init__(self) -> None:
        print("T - INFO  - App Started")

        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.__del__)
        #self.root.bind("<Configure>", self.resize)
        self.width:int=None
        self.height:int=None
        
        self.mainPixmap = None

        self.width = 300
        self.height = 300

        ## Style Seclection
        #self.style = ttk.Style()
        #self.changestyle()
        #self.root.call("source", "arc.tcl")
        #self.style.theme_use("arc")


        #self.createWidgets()

        self.setup()

        self.root.title("PDF Indexer.")
    
    def __del__(self) -> None:
        try:
            self.root.destroy()
        except tkinter.TclError as err:
            if err.__str__() != "can't invoke \"destroy\" command: application has been destroyed":
                print(f"T - ERROR - Tcl Error on exit")
                print(err)
        finally:
            print("T - INFO  - Exited from __del__")

    def run(self) -> None:
        print("T - INFO  - Running")
        self.root.mainloop()

    def exit(self, event=None):
        self.root.quit()
        print("T - INFO  - Exited from exit()")

    def setup(self):
        self.framePDF = PDFViewer(self.root)
        self.framePDF.pack()

    
    def test(self, event=None):
        print("test")

if __name__ == "__main__":
    app = App()
    app.run()

'''
    if self.mainPixmap == None:
        self.mainPixmap = self.backend.getPagePixmap(1, 3)
    mode = "RGBA" if self.mainPixmap.alpha else "RGB"
    img = Image.frombytes(mode, [self.mainPixmap.width, self.mainPixmap.height], self.mainPixmap.samples)
    ## have a setting here to check if user had set a zoom level

    #width = self.pdfRender.winfo_width() - 4 # Stop weird movement
    height  = self.pdfRender.winfo_height() - 10 # Stop weird movement
    # set ratio here to lock width to height avaliable
    width = int(height // (self.mainPixmap.height/self.mainPixmap.width))

    size = (width, height)
    resizedImage = img.resize(size, Image.LANCZOS)
    frame_image = ImageTk.PhotoImage(resizedImage)

    self.pdfRender.config(image=frame_image)
    self.pdfRender.image = frame_image
    
'''