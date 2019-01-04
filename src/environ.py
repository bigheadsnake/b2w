#!/usr/bin/python3
# -*-coding:UTF-8-*-

import os

def run_env():
    os.environ['CONF_MYSQL_B2W_HOST'] = '127.0.0.1'
    os.environ['CONF_MYSQL_B2W_USER'] = 'root'
    os.environ['CONF_MYSQL_B2W_PASSWD'] = ''
    os.environ['CONF_MYSQL_B2W_PORT'] = '3306'
    os.environ['CONF_MYSQL_B2W_DB'] = 'b2w'
