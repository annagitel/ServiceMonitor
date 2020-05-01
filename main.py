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
            processName = str(proc.name())
            processID = proc.pid()
            process_list.update({processName, processID})
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_list


if __name__ == '__main__':
    current_time = time.clock()
    current_process_list = get_current_services()
    current_time_stamp = time_stamp.get_from_dict({current_time, current_process_list})
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
        time.sleep(30)

