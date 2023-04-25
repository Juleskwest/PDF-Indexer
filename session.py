# Session Manager 
import logger

class SessionManager:
    def __init__(self) -> None:
        currentSession = None
        config = None
        self.log = logger.Logger("SessionMan")
        self.log.stack()

    def resetVariables(self):
        self.log.stack()
        pass
    
    def new(self, name:str):
        self.log.stack()

    def open(self):
        self.log.stack()
        pass

    def close(self):
        self.log.stack()
        pass


if __name__ == "__main__":
    ses = SessionManager()
    ses.new("test")