import os
import platform
import time
import subprocess
import json
import psutil
import process
import time_stamp
from time_stamp import TIME_STAMP


def diff(prev, current):
    """
    :param prev: previouse time stamp
    :param current: current time stamp
    :return: list of diffs between 2 time stemps
    """
    diff = []
    for pro in prev.pro_list:
        if pro not in current.pro_list:
            diff.append(pro.pid + "has stopped between" + prev.time + " and " + current.time)
    for pro in current.pro_list:
        if process not in prev.pro_list:
            diff.append(pro.pid + "has started between" + prev.time + " and " + current.time)
    return diff


def get_current_services():
    process_list = {}
    for proc in psutil.process_iter():
        try:
            processName = str(proc.name)
            processID = proc.pid
            process_list.update({processName: processID})
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_list


def write_to_serviceList(ts_obj):
    pass


def write_to_statusLog(diff_list):
    pass


def monitor(time_diff):
    crnt_ts = TIME_STAMP
    prev_ts = crnt_ts
    while True:
        current_time = time.clock()
        pro_list = get_current_services()
        crnt_ts = TIME_STAMP(time=current_time, pro_list=pro_list)
        write_to_serviceList(current_time)
        diffs = diff(crnt_ts, prev_ts)
        write_to_statusLog(diffs)
        prev_ts = crnt_ts

"""
    current_process_list = get_current_services()
    current_time_stamp = time_stamp.get_from_dict({current_time,current_process_list})
    previouse_time_stamp = current_time_stamp

    while True:
        current_time = time.time()
        current_process = get_current_services()
        with open('serviceList.txt', 'w') as file:
            file.write(json.dumps(current_process))
        # make the part above more OO

        diffs = diff(previouse_time_stamp, current_time_stamp)
        with open('status_log.txt', 'w') as file:
            file.write(json.dumps(diffs))

        previouse_time_stamp = current_time_stamp
        time.sleep(time_diff)"""


def manual(start_time, end_time):
    start_dict = {}
    end_dict = {}
    with open('serviceList.txt', 'r') as file:
        main_dict = file.read()
    for k, v in main_dict:
        if k == start_time:
            start_dict = v
        if k == end_time:
            end_dict = v
    start_ts = time_stamp.get_from_dict(start_dict)
    end_ts = time_stamp.get_from_dict(end_dict)
    return diff(start_ts, end_ts)


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
