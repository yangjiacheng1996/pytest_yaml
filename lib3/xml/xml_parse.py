#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import importlib
import os
import sys
from xml.etree import ElementTree


def load_xml(xml_file_path):
    """
    function: 读取xml文件，将xml中的内容加载成一个标签树
    """
    with open(xml_file_path, "r", encoding="utf-8") as rf:
        logging.info(f"加载xml文件内容变成标签树，文件路径：{xml_file_path}")
        tree = ElementTree.parse(rf)
    return tree


def dump_xml(tree, xml_file_path):
    """
    function: 将标签树写进一个文件中。
    """
    # with open(xml_file_path,"w+",encoding="utf-8") as wf:
    tree.write(xml_file_path, encoding="utf-8", xml_declaration=True)
    return True


def find_nodes(tree, xpath):
    """
    根据xpath搜索标签树，返回list，包含所有匹配的标签node
    """
    logging.info(f"根据xpath定位所有元素，XPATH: {xpath}")
    return tree.findall(xpath)


def if_match(node, kv_map):
    '''判断某个节点是否包含所有传入参数属性
    node: 节点
    kv_map: 字典，匹配的属性名及属性值map
    '''
    for key, value in kv_map.items():
        if node.attrib.get(key) != value:
            return False
    return True


def get_nodes_by_keyvalue(nodelist, kv_map):
    '''根据属性及属性值定位符合的节点，返回节点
    nodelist: 节点列表
    kv_map: 字典，匹配的属性名及属性值map
    '''
    result_nodes = []
    for node in nodelist:
        if if_match(node, kv_map):
            result_nodes.append(node)
    return result_nodes


def change_nodes_properties(nodelist, kv_map, to_delete=False):
    '''
    修改/增加 /删除 节点的属性及属性值
    nodelist: 节点列表
    kv_map:属性及属性值map
    to_delete: True删除，False修改
    '''
    for node in nodelist:
        for key, value in kv_map.items():
            if key in node.attrib.keys():
                if to_delete:
                    logging.info(f"删除标签属性{key}")
                    del node.attrib[key]
                else:
                    logging.info(f"开始修改标签的属性,新的键值对是 {key} = {value} ")
                    node.set(key, value)
    return None



def change_xml_tree_by_setting(tree, settings_module_path):
    if not os.path.isfile(settings_module_path):
        raise IOError("Error,file not exist!!")
    file_dir, file_name = os.path.split(settings_module_path)
    # import settings
    try:
        sys.path.append(file_dir)
        module = importlib.import_module(file_name.rstrip(".py"))
    except ImportError as ie:
        logging.error(ie)
        return False
    if getattr(module, "settings_for") != "XML":
        raise ValueError("This setting file is not for XML")
    varlist = getattr(module, "all_var_name")
    for var_name in varlist:
        var_value = getattr(module, var_name)
        if isinstance(var_value, dict):
            xpath = var_value.get("XPATH", None)
            check_map = var_value.get("check_map", None)
            change_map = var_value.get("change_map", None)
            node_list_by_xpath = find_nodes(tree, xpath)
            node_list_check = get_nodes_by_keyvalue(node_list_by_xpath, check_map)
            change_nodes_properties(node_list_check, change_map, to_delete=False)
        else:
            pass
    return tree