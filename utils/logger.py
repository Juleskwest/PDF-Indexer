import logging
import sys
import inspect
import os

class Logger:
    def __init__(self, name, logfile="file.log") -> None:
        self.name = name
        self.logfile = f"logs/{logfile}"
        self.logger = logging.getLogger(f"{name:20}")
        if not os.path.exists("logs"):
            os.mkdir("logs")

        # Handlers
        self.c_handler = logging.StreamHandler(stream = sys.stdout)
        self.f_handler = logging.FileHandler(self.logfile)

        # Formats
        self.c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        self.f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.c_handler.setFormatter(self.c_format)
        self.f_handler.setFormatter(self.f_format)

        self.logger.addHandler(self.c_handler)
        self.logger.addHandler(self.f_handler)
        self.logger.setLevel(logging.DEBUG)
        self.f_handler.setLevel(logging.ERROR)
    
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

    def calledBy(self):
        ## Get function that called this function
        stack:list[inspect.FrameInfo]
        try:
            stack = inspect.stack()
            try:
                callingClass = stack[2][0].f_locals["self"].__class__.__name__
            except KeyError:
                callingClass = ""
            except IndexError:
                callingClass = ""
            try:
                callingMethod = stack[2][0].f_code.co_name
            except IndexError:
                callingMethod = ""
            MethodName = stack[1][0].f_code.co_name
            self.logger.debug(f"{self.name}.{MethodName}() was called from {callingClass}.{callingMethod}()")
        except Exception as error:
            self.logger.exception(error)
        finally:
            pass
