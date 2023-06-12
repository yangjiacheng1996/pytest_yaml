#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import logging


def read_yaml(yaml_path):
    print("load yaml start -------------------")
    # load yaml
    try:
        with open(yaml_path, "r", encoding='utf-8') as f:
            yaml_dict = yaml.safe_load(f)
            # print(yaml_dict)
            #yaml_dict_obj = dictToObj(yaml_dict)
            logging.info(f"加载yaml到内存成功，文件路径：{yaml_path}")
            return yaml_dict
    except Exception as e:
        logging.error(e)
        raise IOError("加载配置文件失败，你给的配置文件是乱码的，或者有语法错误")
