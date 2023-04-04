import logging

class Logger:
    def __init__(self, logfile="file.log") -> None:
        self.logfile = logfile
        self.logger = logging.getLogger(__name__)

        # Handlers
        self.c_handler = logging.StreamHandler()
        self.f_handler = logging.FileHandler(self.logfile)
        self.c_handler.setLevel(logging.INFO)
        self.f_handler.setLevel(logging.ERROR)

        # Formats
        self.c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        self.f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.c_handler.setFormatter(self.c_format)
        self.f_handler.setFormatter(self.f_format)

        self.logger.addHandler(self.c_handler)
        self.logger.addHandler(self.f_handler)
    
    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)
            
    def warning(self, message):
        self.logger.warning(message)
            
    def error(self, message):
        self.logger.error(message)
            
    def critical(self, message):
        self.logger.critical(message)
            
    def exception(self, message):
        self.logger.exception(message)