from handlers import *
from logentry import *
import tkinter as tk

#dictionary of levels
levels = {
            "DEBUG": 10,
            "INFO": 20,
            "WARNING": 30,
            "ERROR": 40,
            "CRITICAL":50
        }

class ProfilLogger:
    def __init__(self, handlers):
        self.handlers = handlers
        self.level= ""
        self.msg=""
        self.min_level= ""
    #minimal log set by the user
    def set_log_level(self, level):
        self.min_level= level
        return self.min_level

    def info(self, msg):
        if levels["INFO"] >= levels[self.min_level]:
            self.level='INFO'
            dt=datetime.now()
            log= LogEntry(dt.strftime("%m/%d/%Y %H:%M:%S"), level=self.level, msg=msg)
            return f"{log.date},{log.level},{log.msg}"
        else:
            print("LogEntry can't be saved")

    def warning(self, msg):
        if levels["WARNING"] >= levels[self.min_level]:
            self.level = 'WARNING'
            dt=datetime.now()
            log = LogEntry(dt.now().strftime("%m/%d/%Y %H:%M:%S"), level=self.level, msg=msg)
            return f"{log.date},{log.level},{log.msg}\n"
        else:
            print("LogEntry can't be saved")


    def debug(self, msg):
        if levels["DEBUG"] >= levels[self.min_level]:
            self.level = 'DEBUG'
            dt=datetime.now()
            log = LogEntry(dt.now().strftime("%m/%d/%Y %H:%M:%S"), level=self.level, msg=msg)
            return f"{log.date},{log.level},{log.msg}\n"
        else:
            print("LogEntry can't be saved")


    def critical(self, msg):
        if levels["CRITICAL"] >= levels[self.min_level]:
            self.level = 'CRITICAL'
            dt=datetime.now()
            log = LogEntry(dt.now().strftime("%m/%d/%Y %H:%M:%S"), level=self.level, msg=msg)
            return f"{log.date},{log.level},{log.msg}\n"
        else:
            print("LogEntry can't be saved")


    def error(self, msg):
        if levels["ERROR"] >= levels[self.min_level]:
            self.level = 'ERROR'
            dt=datetime.now()
            log = LogEntry(dt.now().strftime("%m/%d/%Y %H:%M:%S"), level=self.level, msg=msg)
            return f"{log.date},{log.level},{log.msg}\n"
        else:
            print("LogEntry can't be saved")

if __name__ == '__main__':
    #example usage
    csv_handler = CSVHandler("data_files/logs.csv")
    file_handler = FileHandler("data_files/logs.txt")
    logger = ProfilLogger(handlers=[file_handler,csv_handler])

    logger.set_log_level(level="INFO")
    a= logger.info(msg= "Some info message")
    print(f'Example LogEntry: {a}')




