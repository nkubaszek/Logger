import json
import csv
import sqlite3
from logentry import *
import datetime
from handlers import *
from profillogger import *
from re import search, match, I

class ProfilLoggerReader():
    def __init__(self, handler):
        self.handler=handler

    def find_by_text(self, text, start_date= None, end_date=None):
        log_list=[]
        for logs in self.handler.read():
            if start_date and end_date==None:
                if start_date <= logs.date:
                    log_list.append(logs)
            if end_date and start_date==None:
                if end_date >= logs.date:
                    log_list.append(logs)
            if start_date and end_date:
                if start_date > end_date:
                    return print("error dates")
                else:
                    if end_date >= logs.date and start_date <= logs.date:
                        log_list.append(logs)
            else:
                if text in logs.msg and logs not in log_list:
                    log_list.append(logs)
        return log_list

    def find_by_regex(self, regex, start_date= None, end_date= None):
        logs_array = []
        for logs in self.handler.read():
            if start_date and end_date == None:
                if start_date <= logs.date:
                    result = search(f"{regex}", logs.msg)
                    if result != None:
                        if result.group() in logs.msg and logs not in logs_array:
                            logs_array.append(logs)
            elif end_date and start_date==None:
                if end_date >= logs.date:
                    result = search(f"{regex}", logs.msg)
                    if result != None:
                        if result.group() in logs.msg and logs not in logs_array:
                            logs_array.append(logs)
            elif start_date and end_date:
                if start_date > end_date:
                    return print("Error occured")
                else:
                    if end_date >= logs.date and start_date <= logs.date:
                        result = search(f"{regex}", logs.msg)
                        if result != None:
                            if result.group() in logs.msg and logs not in logs_array:
                                logs_array.append(logs)
            else:
                result = search(f"{regex}", logs.msg)
                if result != None:
                    if result.group() in logs.msg and logs not in logs_array:
                        logs_array.append(logs)
        if logs_array == []:
            return print("Can't find regex in LogEntries")
        return logs_array

    def groupby_level(self, start_date = None, end_date= None):
        levels_dict={'CRITICAL':[], 'ERROR':[], 'WARNING':[], 'INFO':[], 'DEBUG':[]}
        for logs in self.handler.read():
            if start_date and end_date == None:
                if start_date <= logs.date:
                    if "CRITICAL" in logs.level and logs not in levels_dict:
                        print(logs.date, logs.level)
                        levels_dict['CRITICAL'].append(logs)
                    elif "ERROR" in logs.level and logs not in levels_dict:
                        levels_dict['ERROR'].append(logs)
                    elif "WARNING" in logs.level and logs not in levels_dict:
                        levels_dict['WARNING'].append(logs)
                    elif "INFO" in logs.level and logs not in levels_dict:
                        levels_dict['INFO'].append(logs)
                    elif "DEBUG" in logs.level and logs not in levels_dict:
                        levels_dict['DEBUG'].append(logs)
            elif end_date and start_date == None:
                if end_date >= logs.date:
                    if "CRITICAL" in logs.level:
                        levels_dict['CRITICAL'].append(logs)
                    elif "ERROR" in logs.level:
                        levels_dict['ERROR'].append(logs)
                    elif "WARNING" in logs.level:
                        levels_dict['WARNING'].append(logs)
                    elif "INFO" in logs.level:
                        levels_dict['INFO'].append(logs)
                    elif "DEBUG" in logs.level:
                        levels_dict['DEBUG'].append(logs)
            elif start_date and end_date:
                if start_date > end_date:
                    return print("error dates")
                else:
                    if end_date >= logs.date and start_date <= logs.date:
                        if "CRITICAL" in logs.level:
                            levels_dict['CRITICAL'].append(logs)
                        elif "ERROR" in logs.level:
                            levels_dict['ERROR'].append(logs)
                        elif "WARNING" in logs.level:
                            levels_dict['WARNING'].append(logs)
                        elif "INFO" in logs.level:
                            levels_dict['INFO'].append(logs)
                        elif "DEBUG" in logs.level:
                            levels_dict['DEBUG'].append(logs)
            else:
                if "CRITICAL" in logs.level:
                    levels_dict['CRITICAL'].append(logs)
                elif "ERROR" in logs.level:
                    levels_dict['ERROR'].append(logs)
                elif "WARNING" in logs.level:
                    levels_dict['WARNING'].append(logs)
                elif "INFO" in logs.level:
                    levels_dict['INFO'].append(logs)
                elif "DEBUG" in logs.level:
                    levels_dict['DEBUG'].append(logs)
        return levels_dict

    def groupby_month(self, start_date= None, end_date = None):
        year_dict = { 'jan': [], 'feb': [], 'mar': [], 'apr':[], 'may': [], 'jun':[], 'jul':[], 'aug':[], 'sep':[], 'oct':[],'nov':[], 'dec':[]}
        for log in self.handler.read():
            logs_month = int(log.date.split(' ')[0].split('/')[0])
            if start_date and end_date == None:
                if start_date <= log.date:
                    if logs_month==1:
                        year_dict['jan'].append(log)
                    if logs_month==2:
                        year_dict['feb'].append(log)
                    if logs_month==3:
                        year_dict['mar'].append(log)
                    if logs_month==4:
                        year_dict['apr'].append(log)
                    if logs_month==5:
                        year_dict['may'].append(log)
                    if logs_month==6:
                        year_dict['jun'].append(log)
                    if logs_month==7:
                        year_dict['jul'].append(log)
                    if logs_month==8:
                        year_dict['aug'].append(log)
                    if logs_month==9:
                        year_dict['sep'].append(log)
                    if logs_month==10:
                        year_dict['oct'].append(log)
                    if logs_month==11:
                        year_dict['nov'].append(log)
                    if logs_month==12:
                        year_dict['dec'].append(log)
            elif end_date and start_date == None:
                if end_date >= log.date:
                    if logs_month==1:
                        year_dict['jan'].append(log)
                    if logs_month==2:
                        year_dict['feb'].append(log)
                    if logs_month==3:
                        year_dict['mar'].append(log)
                    if logs_month==4:
                        year_dict['apr'].append(log)
                    if logs_month==5:
                        year_dict['may'].append(log)
                    if logs_month==6:
                        year_dict['jun'].append(log)
                    if logs_month==7:
                        year_dict['jul'].append(log)
                    if logs_month==8:
                        year_dict['aug'].append(log)
                    if logs_month==9:
                        year_dict['sep'].append(log)
                    if logs_month==10:
                        year_dict['oct'].append(log)
                    if logs_month==11:
                        year_dict['nov'].append(log)
                    if logs_month==12:
                        year_dict['dec'].append(log)
            elif start_date and end_date:
                if start_date > end_date:
                    return print("error occured")
                else:
                    if end_date >= log.date and start_date <= log.date:
                        if logs_month == 1:
                            year_dict['jan'].append(log)
                        if logs_month == 2:
                            year_dict['feb'].append(log)
                        if logs_month == 3:
                            year_dict['mar'].append(log)
                        if logs_month == 4:
                            year_dict['apr'].append(log)
                        if logs_month == 5:
                            year_dict['may'].append(log)
                        if logs_month == 6:
                            year_dict['jun'].append(log)
                        if logs_month == 7:
                            year_dict['jul'].append(log)
                        if logs_month == 8:
                            year_dict['aug'].append(log)
                        if logs_month == 9:
                            year_dict['sep'].append(log)
                        if logs_month == 10:
                            year_dict['oct'].append(log)
                        if logs_month == 11:
                            year_dict['nov'].append(log)
                        if logs_month == 12:
                            year_dict['dec'].append(log)
            else:
                if logs_month == 1:
                    year_dict['jan'].append(log)
                if logs_month == 2:
                    year_dict['feb'].append(log)
                if logs_month == 3:
                    year_dict['mar'].append(log)
                if logs_month == 4:
                    year_dict['apr'].append(log)
                if logs_month == 5:
                    year_dict['may'].append(log)
                if logs_month == 6:
                    year_dict['jun'].append(log)
                if logs_month == 7:
                    year_dict['jul'].append(log)
                if logs_month == 8:
                    year_dict['aug'].append(log)
                if logs_month == 9:
                    year_dict['sep'].append(log)
                if logs_month == 10:
                    year_dict['oct'].append(log)
                if logs_month == 11:
                    year_dict['nov'].append(log)
                if logs_month == 12:
                    year_dict['dec'].append(log)
        return year_dict

if __name__ == '__main__':
    file_handler = FileHandler("data_files/logs.txt")
    log_reader = ProfilLoggerReader(handler=file_handler)

    print('find by text')
    find_text= log_reader.find_by_text("Some debug message", start_date="07/10/2021 18:26:09", end_date="07/11/2021 15:24:05")
    if find_text:
        for lentry in find_text:
            print(lentry.date, lentry.level, lentry.msg)

    print("\n")
    print('find by regex')
    log_regex= log_reader.find_by_regex(f"[a-z A-z]+ info", start_date="07/10/2021 18:26:09", end_date="07/11/2021 15:24:05")
    if log_regex:
        for lentry in log_regex:
            print(lentry.date, lentry.level, lentry.msg)

    print("\n")
    print('Group by level')
    group_level= log_reader.groupby_level(start_date="07/10/2021 18:26:09", end_date="07/11/2021 15:24:50")
    if group_level:
        print(group_level)
        for lentry in group_level['CRITICAL']:
            print("CRITICAL:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_level['ERROR']:
            print("ERROR:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_level['WARNING']:
            print("WARNING:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_level['INFO']:
            print("INFO:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_level['DEBUG']:
            print("DEBUG:", lentry.date, lentry.level, lentry.msg)

    print("\n")
    print('Group by month')
    group_month= log_reader.groupby_month(start_date="07/10/2021 18:26:09", end_date="07/11/2021 15:24:50")
    if group_month:
        print(group_month)
        for lentry in group_month['jan']:
            print("jan:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['feb']:
            print("feb:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['mar']:
            print("mar:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['apr']:
            print("apr:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['may']:
            print("may:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['jun']:
            print("jun:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['aug']:
            print("aug:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['sep']:
            print("sep:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['oct']:
            print("oct:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['nov']:
            print("nov:", lentry.date, lentry.level, lentry.msg)
        for lentry in group_month['dec']:
            print("dec:", lentry.date, lentry.level, lentry.msg)