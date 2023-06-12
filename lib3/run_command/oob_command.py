#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import paramiko
def get_ssh(ip, user, passwd, port=22, retry=3, retry_interval=10):
    """
    功能: 创建 ssh session。这个函数递归尝试 retry 次 ssh 连接，3次连接不上就停止。
    """
    if retry < 0:
        raise Exception("SSH connect %s failed. No More Retry! Throw Error!" % (ip))
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(
            ip,
            port,
            user,
            passwd,
            banner_timeout=30,
            auth_timeout=30,
            allow_agent=False,
        )
    except:
        time.sleep(retry_interval)
        return get_ssh(ip, user, passwd, port, retry - 1, retry_interval)
    return ssh