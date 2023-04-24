import requests
import base64
from logger import Logger

class UpdateManager():
    def __init__(self) -> None:
        self.currentVersion = None
        self.remoteVersion = None
        self.newVersionAvaliable = None
        self.files = {}
        self.logger = Logger("Updater")

        self.versionURL = "https://raw.githubusercontent.com/Juleskwest/PDF-Indexer/dev/version.txt"
        self.githubURL = "https://api.github.com/repos/Juleskwest/PDF-Indexer/git/trees/dev?recursive=1"

    def checkLocalVersion(self):
        with open("version.txt", "r") as file:
            self.currentVersion = file.readline()
            self.logger.info(f"Current Version: {self.currentVersion}")

    def checkRemoteVersion(self):
        versionfile = requests.get(self.versionURL)
        self.remoteVersion = versionfile.text
        self.logger.info(f"Remote Version: {self.remoteVersion}")

    def checkUpdateAvaliable(self):
        if self.currentVersion < self.remoteVersion:
            self.newVersionAvaliable = True
            self.logger.info(f"Update Avaliable.")
        else:
            self.newVersionAvaliable = False
            self.logger.info(f"Up to date.")

    def getFileURLs(self):
        githubRequestFile = requests.get(self.githubURL)
        githubData = githubRequestFile.json()
        for file in githubData["tree"]:
            self.files[file["path"]] = file["url"]
        self.logger.info(f"{len(self.files)} files to avaliable.")

    def downloadFile(self, url):
        fileRequest = requests.get(url)
        filedata = fileRequest.json()
        bytedata = base64.b64decode(filedata["content"])
        self.logger.info(f"Downloading {url}")
        return bytedata

    def update(self):
        self.checkLocalVersion()
        self.checkRemoteVersion()
        self.checkUpdateAvaliable()
        if self.newVersionAvaliable:
            self.getFileURLs()
            for file in self.files:
                with open(file, "wb") as filehandle:
                    filehandle.write(self.downloadFile(self.files[file]))
                    self.logger.info(f"{file} Updated")

if __name__ == "__main__":
    upman = UpdateManager()
    upman.update()
