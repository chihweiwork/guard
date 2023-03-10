import pdb

class FolderMonitor:

    def get_folder_size(self):
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
            tmp_d = {
                "metric":"folder_size", "label":{"path":path},
                "value": value, "exec_date":self.exec_date
            }
            tmp_d = {**tmp_d, **self.default_label}
            output.append(tmp_d)
        self.folder_size = output
        return self.folder_size
    
    def folder_info_export(self) -> list:
        # run all metric
        folder_size = self.get_folder_size()
        
        return [*folder_size]
