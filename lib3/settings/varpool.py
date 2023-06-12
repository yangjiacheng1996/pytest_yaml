#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

class Varpool(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


varpool = Varpool()
varpool.project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
varpool.case_dir = os.path.join(varpool.project_dir, "case")
varpool.lib3_dir = os.path.join(varpool.project_dir, "lib3")
varpool.testplan_dir = os.path.join(varpool.project_dir, "testplan")
varpool.result_dir = os.path.join(varpool.project_dir, "result")

