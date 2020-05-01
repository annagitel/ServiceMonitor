import time

import process
from process import PROCESS


class TIME_STAMP:
    def __init__(self, time, pro_list):
        self.time = time
        self.pro_list = pro_list

    def get_as_dict(self):
        pro_dict = {}
        for process in self.pro_list:
            pro_dict.update(process.get_as_dict())
        return {self.time, pro_dict}

    def add_process(self, process):
        self.pro_list.appand(process)


def get_from_dict(time_stamp_dict):
    ts = TIME_STAMP()
    pro_dict = time_stamp_dict.values()[0]
    t = time_stamp_dict.keys()[0]
    ts.time = t
    for k, v in pro_dict:
        pro = process.get_from_dict(pro_dict={k, v})
        ts.add_process(process=pro)

    return ts
