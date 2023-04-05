import pdb
import psutil
import json
import re
import pandas as pd

class User_usage:
    def __init__(self):
        #self.regex = ["chihwei"]
        self.regex = ["root"]
    
    def user_filter(self, username):
        for regex in self.regex:
            if re.search(regex, username): return True
        return False
    def _get_cpu_info(self, cpu_info):
        try:
            return {'cpu_user':cpu_info.user, 'cpu_system':cpu_info.system, 'cpu_wio':0.0}
        except:
            return {'cpu_user':cpu_info.user, 'cpu_system':cpu_info.system, 'cpu_wio':cpu_info.iowait}
        
    def process_info_generator(self): 
        
        for process in psutil.process_iter():
            try:
                username = process.username()
                if not self.user_filter(username): continue
                cpu_info = process.cpu_times()
                memory_info = process.memory_info()
                cmdline = process.cmdline()
                cmdline = '' if cmdline == None else ' '.join(cmdline)
                pid = process.pid
                label = {"username":username, 'pid':pid, 'cmdline': cmdline}
                cpu_info = self._get_cpu_info(cpu_info)
                m1 = {"metric": 'user_usage_memory_rss', 'value':memory_info.rss, 'label':label}
                m2 = {"metric": 'user_usage_memory_vms', 'value':memory_info.vms, 'label':label}
                m3 = {"metric": 'user_usage_cpu_user', 'value':cpu_info['cpu_user'], 'label':label}
                m4 = {"metric": 'user_usage_cpu_system', 'value':cpu_info['cpu_system'], 'label':label}
                m5 = {"metric": 'user_usage_cpu_wio', 'value':cpu_info['cpu_wio'], 'label':label}
                for target in [m1, m2, m3, m4, m5]: yield target

            except psutil.NoSuchProcess: pass
            except psutil.AccessDenied: pass
    def get_info(self):
        data = pd.DataFrame(self.process_info_generator())
        data = data.fillna(value=0.0)
        for _, row in data.iterrows(): print(row.to_dict())


if __name__ == "__main__":

    user_usage = User_usage()

    #user_usage.process_info_generator()
    user_usage.get_info()
