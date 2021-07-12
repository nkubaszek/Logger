from datetime import datetime

class LogEntry():
    def __init__(self, date, level, msg):
        self.date=date
        self.level=level
        self.msg=msg

