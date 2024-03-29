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
@click.option("-s", "--story", help="this testing for which target?\n", required=True, default="Default")
def test(testplan, feature, story):
    testplan_path = os.path.join(varpool.testplan_dir, testplan)
    data = read_yaml(testplan_path)
    # The list of dict in testplan file includes case dict and vars dict.
    # Cases are going to be recorded into result/case.json
    # Vars are planed updated into varpool first, then be recorded into result/vars.json
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
    # Run test function which receive parameters.
    cmd_list = [f"--alluredir={varpool.result_dir}",
                "-o", "log_cli=True",
                "-o", "log_cli_level=INFO",
                "-o", "log_cli_date_format=%Y-%m-%d %H:%M:%S",
                "-o", "log_cli_format=%(asctime)s %(levelname)s %(message)s",
                "--capture=fd",
                "-v", os.path.join(varpool.lib3_dir,"pytest", "run_case.py")]
    pytest.main(cmd_list)
    # Following codes will teach you how to use allure.
    # You can change the logo in test report , if you cannot finish this , google it ! Lots of blogs!
    report_dir = os.path.join(varpool.result_dir, "report")
    wget_allure_command = "wget https://github.com/allure-framework/allure2/releases/download/2.22.4/allure-2.22.4.zip"
    allure_generate_cmd = f"allure generate {varpool.result_dir} -o {report_dir} --clean"
    allure_show_cmd = f"allure open {report_dir}"
    print(f"To download allure,run command:\n\t{wget_allure_command}")
    print(f"To generate report,install java then use command:\n\t{allure_generate_cmd}")
    print(f"To show report in browser,use command: \n\t{allure_show_cmd}")
    os.remove(os.path.join(varpool.result_dir, "case.json"))
    os.remove(os.path.join(varpool.result_dir, "vars.json"))


main.add_command(test)

if __name__ == "__main__":
    main()
