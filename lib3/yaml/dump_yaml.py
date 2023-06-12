#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

import yaml

def write_yaml(file_path,json_obj):
    logging.info("dump start --------------------")
    with open(file_path, "w", encoding="utf-8", ) as wf:
        yaml.safe_dump(json_obj, wf,default_flow_style=False,encoding='utf-8',allow_unicode=True)
        logging.info(f"新配置导入文件成功。导入文件路径：{file_path}")
    return None

