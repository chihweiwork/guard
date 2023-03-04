import yaml
import subprocess
import socket
import pdb
import os
import logging

class ToolBox:
    def __init__(self):
        pass

    def read_yaml(self, path):
        configs = yaml.load(
            open(path), 
            Loader=yaml.FullLoader
        )
        return configs 

    def bash_command(self, cmd_string, timeout=None):
        process = subprocess.Popen(
            cmd_string, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8"
        )
        if timeout == None:process.wait()
        else: process.wait(timeout)
        
        stdout, stderr = process.communicate()
        if stderr != '': print(stderr)
        return stdout

class LocalInformation:
    def __init__(self):
        pass

    def get_hostname(self):
        self.hostname = socket.gethostname()
        return self.hostname
    
    def basic_info(self):
        output = {
            "hostname":self.get_hostname()
        }
        return output

class BasicLogger:
    def __init__(self, log_name, log_dir):
        # setup attribute
        self.log_dir = log_dir
        self.log_name = log_name
        self.log_path = f"{self.log_dir}/{self.log_name}"

        # create log Dir
        os.makedirs(self.log_dir, exist_ok=True)

        # create logger and set log level
        #self.logger = logging.getLogger("My logger")
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # create file handler and set log level
        self.file_handler = logging.FileHandler(self.log_path, mode='w')
        self.file_handler.setLevel(logging.INFO)

        # create stream handler and set log level
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setLevel(logging.INFO)

        # defined log format
        self.logger_format = logging.Formatter(
            '{"timestamp":"%(asctime)s", "file_name":"%(filename)s", ' +
              '"process_name":"%(processName)s", "function_name":"%(funcName)s", ' +
              '"line":"%(lineno)d", "log_level":"%(levelname)s", "message":"%(message)s"}'
        )

        # set log format
        self.file_handler.setFormatter(self.logger_format)
        self.stream_handler.setFormatter(self.logger_format)

        # add handler
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def __get_log_level(self, level):
        # 回傳 log level
        level = level.upper()
        log_level = {
            "INFO":logging.INFO, "WARNING":logging.WARNING, "DEBUG":logging.DEBUG,
            "ERROR":logging.ERROER, "CREITICAL":logging.CREITICAL
        }
        try:
            return log_level[level.upper()]
        except KeyError:
            self.logger.error(f"Get log level {level}, available keys: {log_level.keys()}")

    def reset_logger_log_level(self, level):
        # reset logger log level
        self.logger.setLevel(self.__get_log_level(level))

    def reset_stream_hander_log_level(self, level):
        # reset stream log level
        self.stream_handler.setLevel(self.__get_log_level(level))

    def reset_file_hander_log_level(self, level):
        # reset file log level
        self.file_handler.setLevel(self.__get_log_level(level))

    def reset_logger_format(self, log_format):
        # reset logger log format
        self.logger_format = logging.Formatter(log_format)
        self.file_handler.setFormatter(self.logger_format)
        self.stream_handler.setFormatter(self.logger_format)
