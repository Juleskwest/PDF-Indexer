import io
import zipfile

class fileString:
    def __init__(self) -> None:
        self.stream = io.StringIO()
    
    def write(self, data:str) -> bool:
        self.stream.write(data)
    
    def read(self) -> str:
        return self.stream.getvalue()

    def __del__(self) -> None:
        self.stream.close()

class fileByte:
    def __init__(self) -> None:
        self.stream = io.BytesIO()
    
    def write(self, data) -> bool:
        self.stream.write(data)
    
    def read(self) -> bytearray:
        return self.stream.getvalue()

    def __del__(self) -> None:
        self.stream.close()

class Zip:
    def __init__(self, filename) -> None:
        self.stream = io.BytesIO()
        self.filename = filename

    def open(self):
        with zipfile.ZipFile(self.filename, "r") as zip_archive:
            self.stream.write(zip_archive)
    
    def add(self, file:fileString):
        with zipfile.ZipFile(self.stream, "a") as zip_archive:
            fileInfo = zipfile.ZipInfo(file.stream)
            zip_archive.writestr(fileInfo, file.read())
    
    def save(self):
        with open(zipfile, "bw") as zip_archive:
            zip_archive.write(self.stream.getvalue())

if __name__ == "__main__":
    test = fileString()
    test.write("this is data")
    print(test.read())
    ziptest = Zip("test.zip")
    #ziptest.open()
    ziptest.add(test)
    ziptest.save()