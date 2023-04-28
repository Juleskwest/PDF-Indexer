import requests
import base64
from utils.logger import Logger

class UpdateManager():
    def __init__(self) -> None:
        self.log = Logger(__name__)
        self.log.calledBy()
        self.currentVersion = None
        self.remoteVersion = None
        self.newVersionAvaliable = None
        self.files = {}

        self.branch = "dev"
        self.versionURL = f"https://raw.githubusercontent.com/Juleskwest/PDF-Indexer/{self.branch}/version.txt"
        self.githubURL = f"https://api.github.com/repos/Juleskwest/PDF-Indexer/git/trees/{self.branch}?recursive=1"

    def checkLocalVersion(self):
        self.log.calledBy()
        with open("version.txt", "r") as file:
            self.currentVersion = file.readline()
            self.log.info(f"Current Version: {self.currentVersion}")

    def checkRemoteVersion(self):
        self.log.calledBy()
        versionfile = requests.get(self.versionURL)
        self.remoteVersion = versionfile.text
        self.log.info(f"Remote Version: {self.remoteVersion}")

    def checkUpdateAvaliable(self):
        self.log.calledBy()
        if self.currentVersion < self.remoteVersion:
            self.newVersionAvaliable = True
            self.log.info(f"Update Avaliable.")
        else:
            self.newVersionAvaliable = False
            self.log.info(f"Up to date.")

    def getFileURLs(self):
        self.log.calledBy()
        githubRequestFile = requests.get(self.githubURL)
        githubData = githubRequestFile.json()
        for file in githubData["tree"]:
            self.files[file["path"]] = file["url"]
        self.log.info(f"{len(self.files)} files to avaliable.")

    def downloadFile(self, url):
        self.log.calledBy()
        fileRequest = requests.get(url)
        filedata = fileRequest.json()
        bytedata = base64.b64decode(filedata["content"])
        self.log.info(f"Downloading {url}")
        return bytedata

    def update(self):
        self.log.calledBy()
        self.checkLocalVersion()
        self.checkRemoteVersion()
        self.checkUpdateAvaliable()
        if self.newVersionAvaliable:
            self.getFileURLs()
            for file in self.files:
                with open(file, "wb") as filehandle:
                    filehandle.write(self.downloadFile(self.files[file]))
                    self.log.info(f"{file} Updated")

if __name__ == "__main__":
    upman = UpdateManager()
    upman.update()
