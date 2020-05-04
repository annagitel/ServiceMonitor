from time import strptime

import process


class TIME_STAMP:
    def __init__(self, time, pro_list):
        self.time = time
        self.pro_list = pro_list

    def get_as_dict(self):
        pro_string_list = []
        for pro in self.pro_list:
            pro_string_list.append(pro)
        return {self.time.strftime("%d/%m/%Y %H:%M:%S"), pro_string_list}

    def add_process(self, pro):
        self.pro_list.appand(pro)
        print(type(self.pro_list))


def get_from_dict(time_stamp_dict):
    ts = TIME_STAMP()
    pro_dict = time_stamp_dict.values()[0]
    t = time_stamp_dict.keys()[0]
    ts.time = strptime(t, '%m/%d/%y %H:%M:%S')
    for k, v in pro_dict:
        pro = process.get_from_dict(pro_dict={k, v})
        ts.add_process(pro=pro)

    return ts
