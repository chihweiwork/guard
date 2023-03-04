from folder import FolderMonitor
from base import ToolBox, BasicLogger, LocalInformation
import click

from itertools import chain
import datetime
import pdb

#@click.option('--folder', 'exporter_folder', is_flag=True, help="exporter folder information")
class Exporter(
        ToolBox, BasicLogger, LocalInformation,
        FolderMonitor
    ):
    def __init__(self, config_path):
        ToolBox.__init__(self)

        # 實例化收集機器資訊的物件
        LocalInformation.__init__(self)
        
        # read config
        self.configs = self.read_yaml(config_path)
        
        # 設定 logger
        BasicLogger.__init__(self,
           log_name = self.configs['Log']['file'],
           log_dir = self.configs['Log']['dir']
        )

        # 這裡實例化監控物件
        FolderMonitor.__init__(self)
        
        self.reset_logger_format("[%(asctime)s] [%(levelname)s]: %(message)s")

    def insert_data(self, list1, list2):
        # merge two list
        return list(chain(list1, list2))

    def run(self):
        # get mechine information
        data = dict()
        data['info'] = self.basic_info()
        data['info']['exec_date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # start collect data
        data['data'] = list()
        if "folder" in self.configs['monitor'].keys():
            for target in self.folder_info_export():
                data['data'] = self.insert_data(data['data'], target)

        self.logger.info(data)
        return data

if __name__ == "__main__":
    e = Exporter("./monitor.yml")
    e.run()