from folder import FolderMonitor
from base import ToolBox, BasicLogger, LocalInformation
from postman import KafkaOps
import click

from itertools import chain
import datetime
import pdb
import click

class Exporter(
        ToolBox, BasicLogger, LocalInformation,
        KafkaOps, 
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

        # 實例化 KAFKA 設定
        KafkaOps.__init__(self)
        # 設定 KAFKA PRODUCER 
        self.setup_producer()

        # 這裡實例化監控物件
        FolderMonitor.__init__(self)

        self.exec_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.reset_logger_format("[%(asctime)s] [%(levelname)s]: %(message)s")

    def insert_data(self, list1: list, list2: list) -> list:
        # merge two list
        return list(chain(list1, list2))

    def run(self):
        self.logger.info("Start Monitoring")

        # get mechine information
        self.default_label = self.basic_info()

        # get monitor category
        monitor_category = self.configs['monitor'].keys()
        self.logger.info(f"monitor category {monitor_category}")
        
        # setup kafka topic
        topic = self.configs['kafka']['topic']

        # start collect data
        data['data'] = list()
        if "folder" in self.configs['monitor'].keys():
            folder_info = self.folder_info_export()
            data['data'] = self.insert_data(data['data'], folder_info['folder_size'])

        self.logger.info(json.dumps(data, indent=4))
        return data

@click.command()
@click.option('-c','--config','config_path',help='--config [PATH/TO/CONFIGURATION/FILE]')
def main(config_path):
    e = Exporter(config_path)
    e.run()

if __name__ == "__main__":
    main()
