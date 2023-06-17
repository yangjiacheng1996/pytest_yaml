#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import importlib.util
import re
import sys
import logging

import pytest
import allure

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
lib3_dir = os.path.join(project_dir, "lib3")
result_dir = os.path.join(project_dir, "result")
sys.path.append(lib3_dir)
from lib3.settings.varpool import varpool
from lib3.log.basic_logger import create_logger, create_rotating_file_handler, logger_add_handler

# log
'''
pytest log knowledges:
All log fall into 2 categories: python log or pytest log
you can control python logs by logging 
you can control pytest logs by pytest.ini
By default , pytest will capture python warning,error,critical logging, and system stdout + stderr 
so your logging.info will not be printed or writen into log file by pytest!

the logging.info in cases will be force captured and ignored by pytest , you must open log_cli.
if you want to write info into python log file ,set pytest.ini like this:
log_cli = True
log_cli_level = INFO
log_cli_date_format = %Y-%m-%d %H:%M:%S
log_cli_format = %(asctime)s %(levelname)s %(message)s

pytest command parameters about log
--capture=fd/sys/no/tee-sys , decides how system and python logging logs can be capture by pytest.default is fd
--show-capture=no/stdout/stderr/log/all ,decides what are going to print to stdout when case failed. default is all
'''
log_file = os.path.join(result_dir, "result.log")
logger = create_logger()
filehandler = create_rotating_file_handler("INFO", log_file,maxBytes=5*1024*1024, backupCount=10)
logger_add_handler(logger, filehandler)


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


def render_args(args: dict) -> dict:
    """
    render all {{ }} in args
    """
    for k, v in args.items():
        args[k] = __get_value_from_varpool(str(v))
    return args


def __get_value_from_varpool(arg_string: str):
    """
    if you write args in testplan this:
    args:
      url: "https://xx.xxx.com/token={{token}}"
    ......
    and the {{token}} is a key of varpool from former cases
    this function will replace {{token}} with actual value of varpool.token
    """
    if "{{" not in arg_string:
        return arg_string
    pattern = r"\{\{\s{0,5}(\w+)\s{0,5}\}\}"
    matches = re.findall(pattern, arg_string)
    if not matches:
        return arg_string
    values = [eval(f"varpool.{m}") for m in matches]
    all_is_string = True
    for v in values:
        if not isinstance(v, str):
            all_is_string = False
            break
    if all_is_string:
        new_string = arg_string
        for i in range(len(matches)):
            p = r"(\{\{\s{0,5}" + f"{matches[i]}" + r"\s{0,5}\}\})"
            new_string = re.sub(p, values[i], new_string)
        return new_string
    elif len(matches) >= 2 and not all_is_string:
        logging.error(
            f"Ops, you write {len(matches)} " + "{{ }} in args ,but some of them are not string, I cannot handle this!")
        sys.exit(1)
    else:
        return values[0]


def assertion(ret, assertion_list: list):
    if not assertion_list:
        assert ret, "Case return False,but you expect True!"
    for one_assert in assertion_list:
        if not isinstance(one_assert, dict):
            logging.error(f"Ops,wrong format in assert,text is ： {json.dumps(one_assert)}")
            assert False, "Format error!"
        action = list(one_assert.keys())[0]
        value = __get_value_from_varpool(one_assert[action]) if isinstance(one_assert[action], str) \
            else one_assert[action]
        if action == "boolean" and value == "True":
            assert ret, "Case return False,but you expect True!"
        elif action == "boolean" and value == "False":
            assert not ret, "Case return True ,but you expect False!"
        elif action == "equal":
            assert int(ret) == int(value), f"return is not equal to {int(value)}"
        elif action == "bigger":
            assert int(ret) > int(value), f"return is {int(ret)}, expect > {int(value)}"
        elif action == "bigger&equal":
            assert int(ret) >= int(value), f"return is {int(ret)}, expect >= {int(value)}"
        elif action == "smaller":
            assert int(ret) < int(value), f"return is {int(ret)}, expect < {int(value)}"
        elif action == "smaller&equal":
            assert int(ret) <= int(value), f"return is {int(ret)}, expect <= {int(value)}"
        elif action == "contain":
            assert str(assertion_list[1]) in str(ret), f"Ops, {str(assertion_list[1])} is not in return:{str(ret)}"
        elif action == "same":
            assert str(assertion_list[1]) in str(ret), f"Ops, {str(assertion_list[1])} is not in return:{str(ret)}"
        else:
            assert False, f"Unknow key: {value}"

def logging_boxed_info(message:str,heng="-",shu="|"):
    lines = message.split('\n')
    max_line_length = max(len(line) for line in lines)
    box_width = max_line_length + 4
    horizontal_line = heng * box_width
    logging.info(horizontal_line)
    for line in lines:
        formatted_line = f'{shu} {line.ljust(max_line_length)} {shu}'
        logging.info(formatted_line)
    logging.info(horizontal_line)

@pytest.mark.parametrize("case", load_case_list())
def test_case(case):
    # varpool
    load_vars()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    # feature , story , suite
    allure.dynamic.feature(varpool.feature)
    allure.dynamic.story(varpool.story)
    allure.dynamic.suite(varpool.testplan)
    # load case
    allure.dynamic.title("Case: %s" % case["case_name"])
    for step in case["steps"]:
        script = step.get("script", 0)
        if not script.endswith(".py"):
            script += ".py"
        function_name = step.get("function_name", 0)
        description = step.get("description", function_name)
        kwargs = step.get("args", 0)
        kwargs = render_args(kwargs)
        assert_list = step.get("assert", [])
        allure.step(f"Step: {description}")
        function_obj = get_function(os.path.join(project_dir, "case", script), function_name)
        ret = function_obj(**kwargs)
        if isinstance(ret,int) or isinstance(ret,str) or isinstance(ret,bool) or isinstance(ret,float):
            logging_boxed_info("step return: \n"+str(ret))
        elif isinstance(ret,list) or isinstance(ret,dict):
            logging_boxed_info("step return: \n"+json.dumps(ret))
        elif isinstance(ret,set) or isinstance(ret, tuple):
            logging_boxed_info("step return: \n"+json.dumps(list(ret)))
        else:
            logging.info("step return: \n"+"An object")
        assertion(ret, assert_list)
        # record step return into varpool, following cases may use it .
        varpool.ret = ret
