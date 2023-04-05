from kafka3 import KafkaProducer
import json
import pandas as pd
from base import ToolBox
from base import BasicLogger

import pdb

class KafkaOps:
    def setup_producer(self):
        # 取得 kafka setting options
        options = self.configs['kafka'].keys()
        
        # kafka 基礎設定
        producer = KafkaProducer(
            bootstrap_servers=self.configs['kafka']['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('ascii')
        )

        # kafka kerberos 設定
        if "serurity_protocol" in options:
            producer.serurity_protocol = self.configs['kafka']['serurity_protocol']
        if "sasl_kerberos_service" in options:
            producer.sasl_kerberos_service = self.configs['kafka']['serurity_protocol']
        if "sasl_kerberos_service_name" in options:
            producer.sasl_kerberos_service_name = self.configs['kafka']['sasl_kerberos_service_name']
        if "sasl_mechanism" in options:
            producer.sasl_mechanism = self.configs['kafka']['sasl_mechanism']

        # 設定 kafka 行為
        if "retries" in options:
            producer.retries = self.configs['kafka']['retries']

        self.producer = producer
        return producer

    def _on_success(self, info: str):
        """
        成功時輸出的訊息
        """
        self.logger.info(info)
    def _on_error(self, excp: str):
        """
        失敗時輸出的訊息
        """
        self.logger.error(excp)

    def upload_dataframe(self, topic: str, data:list): 
        """
        上傳 pandas dataframe 到 kafka 
        """
        for _, row in data.iterrows():
            self.upload_dict(topic, row.to_dict())
        self.producer.flush()
    def upload_dict(self, topic: str, data: list):
        """
        上傳單一一個 dict 到 kafka 
        """
        self.producer.send(
            topic, data
        ).add_callback(self._on_success).add_errback(self._on_error)
        # 需要另外 flush

    def upload_dict_list(self, topic: str, data: list):
        """
        上傳多個 dict 到 kafka
        """
        for target in data:
            self.upload_dict(topic, target)
        self.producer.flush()
    
        

if __name__ == "__main__":

    configs = ToolBox().read_yaml("./monitor.yml")


    kops = KafkaOps(configs)
    kops.setup_producer()
    data = pd.DataFrame({"A":[1,2,3], "B":[2,5,1]})
    kops.upload_dataframe('test', data)
