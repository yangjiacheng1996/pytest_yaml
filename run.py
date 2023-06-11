#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "lib3"))
from lib3.settings.varpool import varpool
from lib3.yaml.load_yaml import read_yaml


import click
import pytest




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
@click.option("-t","--testplan",help="testplan file name in <project_dir>/testplan/\n",required=True,default="sample.yml")
def datadrive(testplan):
    testplan_path = os.path.join(varpool.testplan_dir,testplan)
    data = read_yaml(testplan_path)
    run_list = []
    for i in range(len(data)):
        item = data[i].get("vars",0)
        case_name = data[i].get("case_name",0)
        if item:
            varpool.update(item)
        elif case_name:
            run_list.append(data[i])
        else:
            print("case_name not found after case: %s!"%case_name)
            sys.exit(1)
    tmp_json = open(os.path.join(varpool.result_dir,"run.json"),"w+",encoding="utf-8")
    json.dump(run_list,tmp_json)
    tmp_json.close()
    pytest.main(["-vs", os.path.join(varpool.lib3_dir,"pytest","run_case.py")])
    os.remove(os.path.join(varpool.result_dir,"run.json"))


main.add_command(datadrive)

if __name__ == "__main__":
    main()
