#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import importlib.util
import sys
from lib3.log.basic_logger import create_logger, create_rotating_file_handler, logger_add_handler

import pytest
import allure

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
lib3_dir = os.path.join(project_dir, "lib3")
result_dir = os.path.join(project_dir, "result")
sys.path.append(lib3_dir)
from lib3.settings.varpool import varpool


def load_case_list():
    with open(os.path.join(project_dir, "result", "case.json"), encoding="utf-8") as j:
        return list(json.load(j))


def load_vars():
    with open(os.path.join(project_dir, "result", "vars.json"), encoding="utf-8") as j:
        vars = json.load(j)
        varpool.update(vars)
        return varpool


def get_function(file_path, function_name):
    # 获取模块名和文件名
    module_name = file_path.split("/")[-1].replace(".py", "")
    module_file = file_path

    # 使用 importlib 导入模块
    spec = importlib.util.spec_from_file_location(module_name, module_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 获取函数对象
    function = getattr(module, function_name)
    return function


load_vars()



@pytest.mark.parametrize("case", load_case_list())
def test_case(case):
    # 日志
    log_file = os.path.join(result_dir, "result.log")
    default_logger = create_logger()
    filehandler = create_rotating_file_handler("INFO", log_file, backupCount=100)
    logger_add_handler(default_logger, filehandler)
    # feature和story
    allure.dynamic.feature(varpool.feature)
    allure.dynamic.story(varpool.story)
    allure.dynamic.suite(varpool.testplan)
    # 加载case
    allure.dynamic.title("Case: %s" % case["case_name"])
    for step in case["steps"]:
        script = step.get("script", 0)
        if not script.endswith(".py"):
            script += ".py"
        function_name = step.get("function_name", 0)
        description = step.get("description", function_name)
        kwargs = step.get("args", 0)
        assert_text = step.get("assert", "True")
        allure.step(f"Step: {description}")
        function_obj = get_function(os.path.join(project_dir, "case", script), function_name)
        result = function_obj(**kwargs)
        if assert_text == "True":
            assert result
        elif assert_text == "False":
            assert not result
        else:
            assert eval(assert_text)
