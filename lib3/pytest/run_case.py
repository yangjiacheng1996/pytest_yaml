#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import pytest
import importlib.util

project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_run_list():
    with open(os.path.join(project_dir, "result", "run.json"), encoding="utf-8") as j:
        return json.load(j)


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


@pytest.mark.parametrize("params", load_run_list())
def test_case(params):
    for step in params["steps"]:
        script = step.get("script", 0)
        if not script.endswith(".py"):
            script += ".py"
        function_name = step.get("function_name", 0)
        kwargs = step.get("args", 0)
        assert_text = step.get("assert", "True")
        function_obj = get_function(os.path.join(project_dir, "case", script), function_name)
        result = function_obj(**kwargs)
        if assert_text == "True":
            assert result
        elif assert_text == "False":
            assert not result
        else:
            assert eval(assert_text)
