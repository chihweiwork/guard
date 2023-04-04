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
            value, path = tmp.splitlines()[0].split('\t')
            tmp_d = {
                "metric":"folder_size", "value":int(value), "label":{"path":path}
            }
            output.append(tmp_d)
        return output
    
    def folder_info_export(self):
        # run all metric
        return {
            "folder_size" : self.get_folder_size()
        }
