#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Varpool(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__

    def __init__(self):
        self.project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.case_dir = os.path.join(self.project_dir,"case")
        self.lib3_dir = os.path.join(self.project_dir, "lib3")
        self.testplan_dir = os.path.join(self.project_dir,"testplan")
        self.result_dir = os.path.join(self.project_dir,"result")

varpool = Varpool()


