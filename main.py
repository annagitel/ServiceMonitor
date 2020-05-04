from datetime import datetime
import time
import psutil
import process
from time_stamp import TIME_STAMP


def diff(older, newer):

    diff_list = []
    for pro in older.pro_list:
        if pro not in newer.pro_list:
            diff_list.append(pro.pid + " has stopped between " + older.time + " and " + newer.time)
    for pro in newer.pro_list:
        if process not in older.pro_list:
            diff_list.append(pro.pid + "has started between" + older.time + " and " + newer.time)
    return diff_list


def get_current_services():
    process_list = []
    for proc in psutil.process_iter():
        process_list.append(proc.as_dict(['pid', 'name']))
    return process_list


def write_to_serviceList(ts_obj):
    file = open("serviceList", "a")
    file.write(ts_obj.get_as_dict + "\n")
    file.close()


def write_to_statusLog(diff_list):
    file = open("Status_Log.txt", "a")
    file.write(diff_list + "\n")
    file.close()


def monitor(time_diff):
    crnt_ts = TIME_STAMP
    prev_ts = crnt_ts
    while True:
        current_time = datetime.now()
        pro_list = get_current_services()
        crnt_ts = TIME_STAMP(time=current_time, pro_list=pro_list)

        write_to_serviceList(crnt_ts.get_as_dict())

        diffs = diff(crnt_ts, prev_ts)
        write_to_statusLog(diffs)

        prev_ts = crnt_ts
        time.sleep(time_diff)


def manual(start_time, end_time):
    log_list = []
    file = open("Status_Log.txt", "r")
    for _ in file:
        log = file.readline()
        splited = log.split(' ')
        older = splited[4]
        newer = splited[6]
        if older > start_time and newer < end_time:
            log_list.append(log.split('between')[0])
    return log_list


if __name__ == '__main__':
    mode = int(input("Hello user, please choose a mode \n 2 - monitor \n 1 - manual \n 0 - exit"))
    if mode == 0:
        exit()
    elif mode == 1:
        start = input("Please enter the first date in d/m/Y H:M:S format")
        end = input("Please enter the second date in d/m/Y H:M:S format")
        manual(start, end)
    elif mode == 2:
        timer = input("Please enter frequency check in seconds: ")
        monitor(timer)
    else:
        print("are you stupid?")
