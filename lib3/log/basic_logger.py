#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.handlers
import sys
import os

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
lib3_dir = os.path.join(project_dir, "lib3")
result_dir = os.path.join(project_dir, "result")
sys.path.append(lib3_dir)
from lib3.settings.varpool import varpool

def create_logger(logger_name=''):
    logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
    return logging.getLogger(logger_name)


def create_rotating_file_handler(minlevel:str,filepath:str,mode="a",maxBytes=1024*1024*5,backupCount=10,
                                 encoding="utf-8",logformat='%(asctime)s %(levelname)s %(message)s'):
    file_handler = logging.handlers.RotatingFileHandler(filepath,mode=mode,maxBytes=maxBytes,backupCount=backupCount,
                                                        encoding=encoding)
    file_handler.setLevel(eval("logging.%s"%minlevel))
    file_handler.setFormatter(logging.Formatter(logformat))
    return file_handler


def create_stream_handler(minlevel:str,stream=sys.stdout,logformat='%(asctime)s %(levelname)s %(message)s'):
    stream_handler = logging.StreamHandler(stream=stream)
    stream_handler.setLevel(minlevel)
    stream_handler.setFormatter(logging.Formatter(logformat))
    return stream_handler


def logger_add_handler(logger,handler):
    logger.addHandler(handler)


if __name__ == "__main__":
    log_file = os.path.join(result_dir, "test_result.log")
    logger = create_logger("test")
    filehandler = create_rotating_file_handler("INFO", log_file, backupCount=10)
    logger_add_handler(logger, filehandler)