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
    log_list = []
    file = open("Status_Log.txt", "r")
    log = file.readline()
    user_start = datetime.strptime(start_time, "%d/%m/%Y %H:%M:%S")
    user_end = datetime.strptime(end_time, "%d/%m/%Y %H:%M:%S")
    old_sample = []
    new_sample = []
    while log:
        splited = log.split(' ')
        older = datetime.strptime(splited[6] + " " + splited[7], "%d/%m/%Y %H:%M:%S")
        newer = datetime.strptime(splited[9] + " " + splited[10], "%d/%m/%Y %H:%M:%S")
        if older <= user_start <= newer:
            old_sample.append(log.split('between')[0])

        elif older < user_end < newer:
            new_sample.append(log.split('between')[0])

        log = file.readline()
    print("first sample: " + '\n')
    for line in old_sample:
        print(line)
    print('\n')
    print("second sample: " + '\n')
    for line in new_sample:
        print(line)
    return log_list


if __name__ == '__main__':
    mode = int(input("Hello user, please choose a mode \n 2 - monitor \n 1 - manual \n 0 - exit"))
    if mode == 0:
        exit()
    elif mode == 1:
        start = input("Please enter the first date in d/m/Y H:M:S format")
        end = input("Please enter the second date in d/m/Y H:M:S format")
        out = manual(start, end)
        for item in out:
            print(item)
    elif mode == 2:
        timer = input("Please enter frequency check in seconds: ")
        monitor(int(timer))
    else:
        print("are you stupid?")
