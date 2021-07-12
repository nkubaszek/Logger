import json
import csv
from profillogger import *
from sqlite3 import Error
import sqlite3
import logentry
class Handler():
    def __init__(self, file):
        self.file=file

    def read(self):
        pass

    def write(self, logentry):
        pass

class CSVHandler(Handler):
    def __init__(self, file):
        super().__init__(file)

    def read(self):
        logs=[]
        with open(self.file, "r") as f:
            lines = f.readlines()
            for line in lines:
                args= line.replace('\n', '').split(',')
                log= LogEntry(date=args[0], level= args[1],  msg=args[2])
                logs.append(log)
        f.close()
        return logs

    def write(self, logentry):
        with open(self.file, "a") as f:
            f.writelines(logentry)
            f.write("\n")
        f.close()

class FileHandler(Handler):
    def __init__(self, file):
        super().__init__(file)

    def read(self):
        table_logs = []
        with open(self.file, "r") as f:
            lines = f.readlines()
            for line in lines:
                args = line.replace('\n', '').split(',')
                lg = LogEntry(date=args[0], level=args[1], msg=args[2])
                table_logs.append(lg)
        f.close()
        return table_logs

    def write(self, logentry):
        with open(self.file, "a") as f:
            f.writelines(logentry)
            f.write("\n")
        f.close()

class SQLLiteHandler():
    def __init__(self, file):
        self.file=file

    def create_connection(self, database):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(database)
            return conn
        except Error as e:
            print(e)

        return conn
    def create_table(self,conn, create_table_sql):

        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
    def insert(self,conn,sqlite_insert_query,variables):
        try:
            c = conn.cursor()
            c.execute(sqlite_insert_query,variables)
        except Error as e:
            print(e)
    def write(self,logentry):
        logent=logentry.replace('\n', '').split(',')
        date_log=logent[0]
        level_log=logent[1]
        msg_log=logent[2]
        sql_create_logs_table = """ CREATE TABLE IF NOT EXISTS logs (
                                            date date,
                                            level text,
                                            msg text
                           
                                        ); """

        sqlite_insert_query = """INSERT INTO logs
                          (date, level, msg) 
                           VALUES
                            (?, ?, ?);"""

        variables= (date_log,level_log,msg_log)

        # create a database connection
        conn = self.create_connection(self.file)
        # create tables
        if conn is not None:
            # create projects table
            self.create_table(conn, sql_create_logs_table)
            self.insert(conn, sqlite_insert_query,variables)
            conn.commit()

        else:
            print("Error! cannot create the database connection.")
    def read(self):
        sql_select="""SELECT *FROM  logs;"""
        conn = self.create_connection(self.file)
        # create tables
        try:
            c = conn.cursor()
            c.execute(sql_select)
            rows = c.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(e)



class JsonHandler(Handler):
    def __init__(self, file):
        super().__init__(file)

    def read(self):
        with open(self.file, 'r') as f:
            data = json.load(f)
            for i in data['logs']:
                print(i)

        f.close()

    def write(self, logentry):

        with open(self.file, "r+") as f:
            file_data = json.load(f)
            logent=logentry.replace('\n', '').split(',')
            #json structure
            log={
                "date":logent[0],
                "level":logent[1],
                "msg":logent[2]
            }
            file_data["logs"].append(log)
            f.seek(0)
            json.dump(file_data,f,indent=4,separators=(", ", ": "),)


if __name__ == '__main__':
    #example usage
    # files
    csv_handler = CSVHandler("data_files/logs.csv")
    file_handler = FileHandler("data_files/logs.txt")
    json_handler = JsonHandler("data_files/logs.json")
    sqllite_handler = SQLLiteHandler("data_files/logs.db")
    # read files:
    print("csv logs")
    for log in csv_handler.read():
        print(log.date, log.level, log.msg)
    print("txt logs")
    for log in file_handler.read():
        print(log.date, log.level, log.msg)
    print("json logs")
    json_handler.read()
    print("SQL logs")
    sqllite_handler.read()


    # create logs:
    logger = ProfilLogger(handlers=[file_handler, csv_handler,json_handler,sqllite_handler])

    # set minimal level:
    logger.set_log_level(level="INFO")
    # create LogEntries:
    a = logger.info(msg="Some info message")

    # write logs into files:
    csv_handler.write(a)
    file_handler.write(a)
    json_handler.write(a)
    sqllite_handler.write(a)




