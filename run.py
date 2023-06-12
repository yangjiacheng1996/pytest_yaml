#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import json
import subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), "lib3"))
from lib3.settings.varpool import varpool
from lib3.yaml.load_yaml import read_yaml
from lib3.run_command.run_commnad import command

import click
import pytest
import allure


@click.group()
def main():
    # 创建result目录用于保存
    result_dir = varpool.result_dir
    print(result_dir)
    if os.path.exists(result_dir):
        shutil.rmtree(result_dir)
    try:
        os.mkdir(result_dir)
    except:
        print("can't create results folder, please check...")
        sys.exit(1)


@click.command()
@click.option("-t", "--testplan", help="testplan file name in <project_dir>/testplan/\n", required=True,
              default="sample.yml")
@click.option("-f", "--feature", help="this testing for which function?\n", required=True, default="Default")
@click.option("-t", "--story", help="this testing for which target?\n", required=True, default="Default")
def test(testplan, feature, story):
    testplan_path = os.path.join(varpool.testplan_dir, testplan)
    data = read_yaml(testplan_path)
    # testplan中有case或vars配置参数，所以需要将这两部分分开
    case_list = []
    for i in range(len(data)):
        vars = data[i].get("vars", 0)
        case_name = data[i].get("case_name", 0)
        if vars:
            varpool.update(vars)
        elif case_name:
            case_list.append(data[i])
        else:
            print("case_name not found after case: %s!" % case_name)
            sys.exit(1)
    varpool.testplan = testplan
    varpool.feature = feature
    varpool.story = story
    varpool_json = open(os.path.join(varpool.result_dir, "vars.json"), "w+", encoding="utf-8")
    case_json = open(os.path.join(varpool.result_dir, "case.json"), "w+", encoding="utf-8")
    json.dump(case_list, case_json)
    json.dump(varpool, varpool_json)
    varpool_json.close()
    case_json.close()
    pytest.main([f"--alluredir={varpool.result_dir}", "-vs", os.path.join(varpool.lib3_dir, "pytest", "run_case.py")])
    allure_path = os.path.join(varpool.project_dir, "tools", "allure", "bin", "allure")
    report_dir = os.path.join(varpool.result_dir,"report")
    allure_generate_cmd = f"{allure_path} generate {varpool.result_dir} -o {report_dir} --clean"
    allure_show_cmd = f"{allure_path} open {report_dir}"
    print(f"To generate report,install java then use command:\n\t{allure_generate_cmd}")
    print(f"To show report in browser,use command: \n\t{allure_show_cmd}")
    os.remove(os.path.join(varpool.result_dir, "case.json"))
    os.remove(os.path.join(varpool.result_dir, "vars.json"))


main.add_command(test)

if __name__ == "__main__":
    main()
