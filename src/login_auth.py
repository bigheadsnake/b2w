# encoding=utf-8
from bottle import request, response
import dbutils
import time
import authorise


class User:

    def __init__(self, db):
        self.db = db
        self.COOKIE_SECRET_KEY = 'The_very_secret_key_for_b2w'
        self.username = ""
        self.salt = ""
        self.logged = False
        self.validate()

    def authenticate(self, username, password):
        # noinspection PyBroadException
        try:
            # verify password
            sql = 'select password, salt, cate from b2w_users where username=\'' + username + "'"
            user_cursor = dbutils.query_single(self.db, sql)
            if user_cursor is not None:
                db_password, db_salt, cate = user_cursor
            else:
                raise ValueError('user is not exist')
            md5_password = authorise.create_md5(password, db_salt)
            if md5_password != db_password:
                raise ValueError('password is not matched')
            dbutils.set_data(self.db, 'b2w_loginhistory',
                             [[time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), username, cate]])

            # manipulate cookie
            self.set_cookie(username)
            self.logged = True
            # 获取权限组
            if self.check_user():
                pass
            return True
        except ValueError:
            return False
        except Exception:
            return False
        finally:
            pass

    def logout(self):
        self.remove_cookie()
        self.logged = False
        self.username = None
        return True

    def validate(self):

        # now check cookie
        username = request.get_cookie('__b2w', secret=self.COOKIE_SECRET_KEY)
        user = dbutils.query_single(self.db, 'SELECT username, password, salt, cate'
                                             ' FROM b2w_users WHERE username = \'%s\'' % username)
        if user:
            self.logged = True
            self.username = username
            if self.check_user():
                # 获取权限组
                pass
            return True

        self.logout()
        return None

    def set_cookie(self, account):
        response.set_cookie(
            '__b2w',
            account,
            secret=self.COOKIE_SECRET_KEY,
            path='/'
        )

    def remove_cookie(self):
        response.set_cookie(
            '__b2w',
            '',
            secret=self.COOKIE_SECRET_KEY,
            path='/'
        )

    def check_user(self):
        if self.username is None:
            return False
        else:
            # 更新用户信息
            return True
