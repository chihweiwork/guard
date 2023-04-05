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
        if stderr != '': 
            stderr = stderr.split('\n')[0]
            self.logger.error(stderr)
        return stdout

    def format_bytes(self, bytes, unit, SI=False):
        """
        Converts bytes to common units such as kb, kib, KB, mb, mib, MB
    
        Parameters
        ---------
        bytes: int
            Number of bytes to be converted
    
        unit: str
            Desired unit of measure for output
    
    
        SI: bool
            True -> Use SI standard e.g. KB = 1000 bytes
            False -> Use JEDEC standard e.g. KB = 1024 bytes
    
        Returns
        -------
        str:
            E.g. "7 MiB" where MiB is the original unit abbreviation supplied
        """
        if unit.lower() in "b bit bits".split():
            return f"{bytes*8} {unit}"
        unitN = unit[0].upper()+unit[1:].replace("s","")  # Normalised
        reference = {"Kb Kib Kibibit Kilobit": (7, 1),
                     "KB KiB Kibibyte Kilobyte": (10, 1),
                     "Mb Mib Mebibit Megabit": (17, 2),
                     "MB MiB Mebibyte Megabyte": (20, 2),
                     "Gb Gib Gibibit Gigabit": (27, 3),
                     "GB GiB Gibibyte Gigabyte": (30, 3),
                     "Tb Tib Tebibit Terabit": (37, 4),
                     "TB TiB Tebibyte Terabyte": (40, 4),
                     "Pb Pib Pebibit Petabit": (47, 5),
                     "PB PiB Pebibyte Petabyte": (50, 5),
                     "Eb Eib Exbibit Exabit": (57, 6),
                     "EB EiB Exbibyte Exabyte": (60, 6),
                     "Zb Zib Zebibit Zettabit": (67, 7),
                     "ZB ZiB Zebibyte Zettabyte": (70, 7),
                     "Yb Yib Yobibit Yottabit": (77, 8),
                     "YB YiB Yobibyte Yottabyte": (80, 8),
                     }
        key_list = '\n'.join(["     b Bit"] + [x for x in reference.keys()]) +"\n"
        if unitN not in key_list:
            raise IndexError(f"\n\nConversion unit must be one of:\n\n{key_list}")
        units, divisors = [(k,v) for k,v in reference.items() if unitN in k][0]
        if SI:
            divisor = 1000**divisors[1]/8 if "bit" in units else 1000**divisors[1]
        else:
            divisor = float(1 << divisors[0])
        value = bytes / divisor
        #return f"{value:,.0f} {unitN}{(value != 1 and len(unitN) > 3)*'s'}"
        return float(f"{value:.2f}")

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
