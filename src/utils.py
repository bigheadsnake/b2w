#!/usr/bin/python3
# -*-coding:UTF-8-*-

import re
import dbutils as dbtools


# 获取数据库
def make_databases(fn):
    def wrapper(*args, **kwargs):
        b2w_db = dbtools.get_db('b2w')
        r = fn(b2w_db, *args, **kwargs)
        return r

    return wrapper


# 应对xss注入和sql注入的关键字过滤代码
def check_html_request(request_str):
    black_regex = [r"\<.*script.*\>", r"\"", r"\'", r"\s"]
    check_flag = False

    for reg in black_regex:
        if re.search(reg, request_str) is not None:
            check_flag = True

    return check_flag
