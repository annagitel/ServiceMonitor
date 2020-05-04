from datetime import datetime
import time
import psutil


def diff(older, newer):
    diff_list = []
    older_list = next(iter(older.values()))
    newer_list = next(iter(newer.values()))
    for pro in older_list:
        if pro not in newer_list:
            diff_list.append(pro + " has stopped between " + older.keys() + " and " + newer.keys())
    for pro in newer_list:
        if pro not in older_list:
            diff_list.append(pro + "has started between" + older.keys() + " and " + newer.keys())
    return diff_list


def get_current_services():
    process_list = []
    for proc in psutil.process_iter():
        process_list.append(proc.as_dict(['pid', 'name']))
    return process_list


def write_to_serviceList(ts_obj):
    file = open("serviceList.txt", "a")
    file.write(str(ts_obj) + "\n")
    file.close()


def write_to_statusLog(diff_list):
    file = open("Status_Log.txt", "a")
    for line in diff_list:
        file.write(line + "\n")
    file.close()


def monitor(time_diff):
    current = {}
    prev = current
    while True:
        current_time = datetime.now()
        pro_list = get_current_services()
        current.update({current_time: pro_list})
        write_to_serviceList(current)

        diffs = diff(current, prev)
        write_to_statusLog(diffs)

        prev = current
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
        monitor(int(timer))
    else:
        print("are you stupid?")
