import json
from ast import literal_eval
from datetime import datetime
import time
import psutil


def diff(older, newer):
    diff_list = []
    older_time = next(iter(older.keys()))
    newer_time = next(iter(newer.keys()))
    older_list = next(iter(older.values()))
    newer_list = next(iter(newer.values()))
    for k in older_list:
        if k not in newer_list:
            diff_list.append(str(k) + " : " + str(older_list[k]) + " has stopped between " +
                             older_time.strftime("%d/%m/%Y %H:%M:%S") + " and " +
                             newer_time.strftime("%d/%m/%Y %H:%M:%S"))
    for k in newer_list:
        if k not in older_list:
            diff_list.append(str(k) + " : " + str(newer_list[k]) + " has started between " +
                             older_time.strftime("%d/%m/%Y %H:%M:%S") + " and " +
                             newer_time.strftime("%d/%m/%Y %H:%M:%S"))
    return diff_list


def get_current_services():
    process_list = {}
    for proc in psutil.process_iter():
        pid = proc.pid
        name = proc.name()
        process_list.update({pid: name})
    return process_list


def write_to_serviceList(ts_obj):
    file = open("serviceList.txt", "a")
    file.write(str(ts_obj) + "\n")
    file.close()


def write_to_statusLog(diff_list):
    file = open("Status_Log.txt", "a")
    for line in diff_list:
        file.write(line + " \n")
    file.close()


def string_to_sample_dict(s):
    d = literal_eval(s)
    t = next(iter(d.keys()))
    l = next(iter(d.values()))
    return {datetime.strptime(t, "%d/%m/%Y %H:%M:%S"): l}


def sample_dict_to_string(d):
    t = next(iter(d.keys()))
    l = next(iter(d.valus()))
    nd = {t.strftime("%d/%m/%Y %H:%M:%S"), l}
    return str(nd)


def monitor(time_diff=10):
    isFirst = True
    while True:
        current_time = datetime.now()
        pro_list = get_current_services()
        current = {current_time: pro_list}
        towrite = {current_time.strftime("%d/%m/%Y %H:%M:%S"): pro_list}
        write_to_serviceList(towrite)
        if isFirst:
            isFirst = False
        else:
            diffs = diff(prev, current)
            for line in diffs:
                print(line)
            write_to_statusLog(diffs)

        prev = current
        time.sleep(time_diff)


def manual(start_time, end_time):
    file = open("serviceList.txt", "r")
    old_sample = {}
    new_sample = {}

    log = file.readline()
    prev_sample = string_to_sample_dict(log)
    prev_time = next(iter(prev_sample.keys()))

    log = file.readline()
    current_sample = string_to_sample_dict(log)
    current_time = next(iter(current_sample.keys()))

    while log:

        if prev_time <= start_time <= current_time:
            old_sample = prev_sample
        if prev_time <= end_time <= current_time:
            new_sample = current_sample

        prev_sample = current_sample
        prev_time = current_time

        log = file.readline()
        if log:
            current_sample = string_to_sample_dict(log)
            current_time = next(iter(current_sample.keys()))

    diff_list = diff(old_sample, new_sample)
    return diff_list
    """log_list = [] // the code before Harel changed the log file to use
    file = open("Status_Log.txt", "r")
    log = file.readline()
    user_start = datetime.strptime(start_time, "%d/%m/%Y %H:%M:%S")
    user_end = datetime.strptime(end_time, "%d/%m/%Y %H:%M:%S")
    while log:
        splited = log.split(' ')
        older = datetime.strptime(splited[6] + " " + splited[7], "%d/%m/%Y %H:%M:%S")
        print(log)
        print(splited[9] + " " + splited[10])
        newer = datetime.strptime(splited[9] + " " + splited[10], "%d/%m/%Y %H:%M:%S")
        if older <= user_start <= newer or (older > user_start and newer < user_end) or older < user_end < newer:
            log_list.append(log.split('between')[0])

        log = file.readline()
    return log_list"""


if __name__ == '__main__':
    mode = int(input("Hello user, please choose a mode \n 2 - monitor \n 1 - manual \n 0 - exit"))
    if mode == 0:
        exit()
    elif mode == 1:
        start_time = datetime
        end_time = datetime
        flag = True
        while flag:
            try:
                start_input = input("Please enter the first date in d/m/Y H:M:S format")
                start_time = datetime.strptime(start_input, "%d/%m/%Y %H:%M:%S")
                flag = False
            except:
                print("time format is not valid. please try again")

        flag = True
        while flag:
            try:
                end_input = input("Please enter the second date in d/m/Y H:M:S format")
                end_time = datetime.strptime(end_input, "%d/%m/%Y %H:%M:%S")
                flag = False
            except:
                print("time format is not valid. please try again")

        out = manual(start_time, end_time)
        for item in out:
            print(item)

    elif mode == 2:
        timer = input("Please enter frequency check in seconds: ")
        monitor(int(timer))
    else:
        print("are you stupid?")
