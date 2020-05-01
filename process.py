class PROCESS:
    def __init__(self, pid, name):
        self.pid = pid
        self.name = name

    def get_as_dict(self):
        return {self.pid, self.name}


def get_from_dict(pro_dict):
    return PROCESS(pid=pro_dict.keys()[0], name=pro_dict.values()[0])
