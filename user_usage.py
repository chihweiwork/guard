import pdb
import psutil
import json
import re
import pandas as pd
import datetime

class UserMonitor:
    #def __init__(self):
        #self.regex = ["chihwei"]
        #self.regex = ["root"]
    
    def user_filter(self, username):
        for regex in self.configs['monitor']['user_usage']['regex']:
            if re.search(regex, username): return True
        return False
    def _get_cpu_info(self, cpu_info):
        try:
            return {'cpu_user':cpu_info.user, 'cpu_system':cpu_info.system, 'cpu_wio':0.0}
        except:
            return {'cpu_user':cpu_info.user, 'cpu_system':cpu_info.system, 'cpu_wio':cpu_info.iowait}
        
    def process_info_generator(self): 
        exec_data = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
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
                target = {
                    "exec_date":exec_data, "label":label, "metric":"user_usage",
                    "data": {
                        "user_usage_memory_rss":self.format_bytes(memory_info.rss, 'MB'), 
                        "user_usage_memory_vms":self.format_bytes(memory_info.vms, 'MB'), 
                        "user_usage_cpu_user":cpu_info['cpu_user'], 
                        "user_usage_cpu_system":cpu_info['cpu_system'], 
                        "user_usage_cpu_wio":cpu_info['cpu_wio']
                    }
                }
                yield {**self.default_label, **target}

            except psutil.NoSuchProcess: pass
            except psutil.AccessDenied: pass
    def user_usage_exporter(self):
        output = [x for x in self.process_info_generator()]
        return output
        

if __name__ == "__main__":

    user_usage = User_usage()

    #user_usage.process_info_generator()
    user_usage.get_info()
