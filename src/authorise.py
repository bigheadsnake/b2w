#!/usr/bin/python3
# -*-coding:UTF-8-*-

from random import Random
from utils import make_databases
import hashlib
import dbutils


# 获取由4位随机大小写字母、数字组成的salt值
def create_salt(length=4):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    random = Random()
    for i in range(length):
        # 每次从chars中随机取一位
        salt += chars[random.randint(0, len_chars)]
    return salt


# 获取原始密码+salt的md5值
def create_md5(pwd, salt):
    md5_obj = hashlib.md5()
    md5_obj.update((pwd + salt).encode("utf8"))
    return md5_obj.hexdigest()


@make_databases
def registration(db, username, password, salt):
    pwd = create_md5(password, salt)
    dbutils.set_data(db, "b2w_users", [[username, pwd, "administrator", salt]])


# 在这里输入要注册的用户名密码
if __name__ == '__main__':
    use_salt = create_salt()
    registration('bigheadsnake', 'Dragoon881112', use_salt)
