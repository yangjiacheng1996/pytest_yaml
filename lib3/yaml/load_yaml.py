#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml

def read_yaml(path):
    with open(path,"r",encoding="utf-8") as y:
        testplan = yaml.load(y,Loader=yaml.FullLoader)
        return testplan