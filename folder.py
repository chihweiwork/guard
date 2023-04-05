import pdb

class FolderMonitor:

    def get_folder_size(self) -> list:
        # 使用系統指令得到 folder 的大小
        cols = ['value', 'metric']
        output = list()
        # 從 configeration 取出需要監控的資料夾
        for target in self.configs['monitor']['folder']['size']:
            # 使用 toolbox 中的 bash_command 執行系統指令
            tmp = self.bash_command(f"du -s {target}")
            if tmp == '':
                self.logger.error(f"Can not find {target}, skip thie folder")
                continue
            value, path = tmp.splitlines()[0].split('\t')
            value = self.format_bytes(float(value), "MB")
            print(value)
            tmp_d = {
                "exec_date":self.exec_date, "label":{"path":path}, "metric":"folder_size",
                "data":{"folder_size":value}, 
                
            }
            tmp_d = {**tmp_d, **self.default_label}
            output.append(tmp_d)
        return output
    
    def folder_info_export(self):
        # run all metric
        function_list = [
            self.get_folder_size
        ]
        output = list()
        for func in function_list:
            tmp = func()
            yield tmp
