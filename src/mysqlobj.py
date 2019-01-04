# encoding=utf-8

# Mysql Wrapper Object for pymysql 

import pymysql

from collections import namedtuple
import re


class MysqlObj:
    conn = None
    cur = None
    conf = None

    # args should include db/user/passwd
    # host/charset/keep_alive are optional
    def __init__(self, **args):
        self.conf = args
        self.conf["charset"] = args.get("charset", "utf8")  # 'utf-8' will fail
        self.conf["use_unicode"] = args.get("use_unicode", True)

        self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(**self.conf)

            self.cur = self.conn.cursor()
        except Exception:
            print("MySql connection failed")
            raise

    # sql could inlude %s and the other formats
    # return cur
    def query(self, sql, params=None):
        try:
            self.cur.execute(sql, params)
        except pymysql.OperationalError:
            # mysql timed out. retry
            #if e[0#] == 2006:
            #    self.connect()
            #    self.cur.execute(sql, params)
            #else:
            print("Query Failed Lv1")
            raise
        except Exception:
            print("Query Failed Lv2")
            raise

        return self.cur

    @staticmethod
    def validate_table(instr):
        pat = re.compile(r'^[\w_\-]+$')
        return pat.match(instr)

    @staticmethod
    def validate_where(instr):
        if instr is None:
            return True
        pat = re.compile(r'^[\w\-<>=\s"]+$')
        return pat.match(instr)

    @staticmethod
    def validate_fields(instr, allow_none=True):
        if instr is None or instr == "":
            if allow_none:
                return True
            else:
                return False
        pat = re.compile(r'^[\w\-,\s"*]+$')
        return pat.match(instr)

    @staticmethod
    def validate_order(instr):
        uin = instr.strip().upper()
        return uin in ('ASC', 'DESC', '')

    @staticmethod
    def validate_limit(limit):
        if limit is None:
            return True
        offset, num = limit
        return offset.isdigit() and num.isdigit()

    # return sql string
    @staticmethod
    def form_sql(table, sortfield=None, order='ASC', limit=None, where=None, select_fields='*'):
        sql = 'SELECT %s FROM %s ' % (select_fields, table)

        if where:
            sql = '%s WHERE %s' % (sql, where)

        if sortfield:
            sql = '%s ORDER BY %s %s' % (sql, sortfield, order)

        if limit:
            offset, num = limit
            sql = '%s LIMIT %d,%d' % (sql, offset, num)

        return sql

    # return sql string
    def form_json_sql(self, table, sortfield=None, order='ASC', limit=None, where=None, select_fields='*'):

        # if not self.validate_table(table):
        #    print "table"
        # if not self.validate_fields(select_fields, allow_none=False):
        #    print"select"
        # if not self.validate_fields(sortfield):
        #    print "sort"
        # if not self.validate_order(order):
        #    print "order"
        # if not self.validate_where(where):
        #    print "where"

        if not self.validate_table(table) or \
                not self.validate_fields(select_fields, allow_none=False) or \
                not self.validate_fields(sortfield) or \
                not self.validate_order(order) or \
                not self.validate_where(where):
            return None

        sql = 'SELECT %s FROM %s ' % (select_fields, table)

        if where:
            sql = '%s WHERE %s' % (sql, where)

        if sortfield:
            sql = '%s ORDER BY %s %s' % (sql, sortfield, order)

        if limit:
            offset, num = limit
            sql = '%s LIMIT %d,%d' % (sql, offset, num)

        return sql

    # return a tuple or None
    # like (u'\u97a0\u4e39',) or None
    def get_one(self, sql):
        cur = self.query(sql)
        return cur.fetchone()

    # return a tuple of tuple or empty tuple
    # like ((u'\u97a0\u4e39',), (u'\u6768\u4f73',)) or ()
    def get_all(self, sql):
        cur = self.query(sql)
        return cur.fetchall()

    def get_next(self, sql, params=None):
        cur = self.query(sql, params)
        while True:
            r = cur.fetchone()
            if r:
                yield r
            else:
                break

    def get_next_named_tuple(self, sql, params=None, prefix='', fieldformat=None):
        cur = self.query(sql, params)
        fields = [_[0] if not fieldformat else fieldformat(_[0]) for _ in cur.description]
        ResultSet = namedtuple('{}ResultSet'.format(prefix), fields)
        while True:
            r = cur.fetchone()
            if r:
                yield ResultSet(*r)
            else:
                break

    # data is a dict
    @staticmethod
    def insert_format(data):
        """
            data = {"k1":"v1", "k2":"v2"}
            return ['k2,k1', '%s,%s']
        """
        keys = ",".join(data.keys())
        val_list = []
        for _ in list(range(0, len(data))):
            val_list.append("%s")
        val = ",".join(val_list)

        return [keys, val]

    # insert a single record
    # data is a dict
    # like db.insert_dict('test1', {'name':'aaa'})
    # return effected row count
    def insert_dict(self, table, data):
        query = self.insert_format(data)

        sql = f"INSERT INTO `{table}` {query[0]} values {query[1]}"

        return self.query(sql, data.values()).rowcount

    # insert a single record with full fields
    # data is a list
    # like db.insert_list('test1', ['aaa'])
    # return effected row count
    def insert_list(self, table, data):
        sql = f"INSERT INTO `{table}` values({','.join(['%s' for k in data])})"

        return self.query(sql, data).rowcount

    # insert multiple records
    # fields is a list of field name
    # data is a list of tuples
    # like db.insert_many('test1', 'name', [('bbb',), ('ccc',)])
    # return effected row count
    def insert_many(self, table, data=None, fields=None):
        if data is None:
            data = []
        if len(data) > 0:
            if fields and len(fields) > 0:
                sql = f'INSERT INTO `{table}` ({",".join(fields)}) values ({",".join(["%s" for i in data[0]])})'
            else:
                sql = f'INSERT INTO `{table}` values ({",".join(["%s" for i in data[0]])})'
            return self.cur.executemany(sql, data)

    def replace_many(self, table, data=None, fields=None):
        if data is None:
            data = []
        if len(data) > 0:
            if fields and len(fields) > 0:
                sql = f'REPLACE INTO `{table}` ({",".join(fields)}) values ({",".join(["%s" for i in data[0]])})'
            else:
                sql = f'REPLACE INTO `{table}` values ({",".join(["%s" for i in data[0]])})'
            return self.cur.executemany(sql, data)

    def insert_ondup_many(self, table, update_fields, data=None, fields=None):
        if data is None:
            data = []
        if len(data) > 0 and len(update_fields) > 0:
            if fields and len(fields) > 0:
                sql = f"INSERT INTO `{table}` ({','.join(fields)}) values ({','.join(['%s' for i in data[0]])}) ON DUPLICATE KEY UPDATE {', '.join(['%s = values(%s)' % (f, f) for f in update_fields])}"
            else:
                sql = f"INSERT INTO `{table}` values ({','.join(['%s' for i in data[0]])}) ON DUPLICATE KEY UPDATE {', '.join(['%s = values(%s)' % (f, f) for f in update_fields])}"
            return self.cur.executemany(sql, data)

    @staticmethod
    def _update_format(data):
        """
            data = {"k1":"v1", "k2":"v2"}
            return 'k2=%s,k1=%s'
        """
        return "=%s,".join(data.keys()) + "=%s"

    # data is a dict
    # like db.update('test1', {'name':'ddd'}, where="name='aaa'")
    # return effected row count
    def update(self, table, data, where=None):
        query = self._update_format(data)

        sql = f"UPDATE `{table}` SET {query}"

        if where:
            sql += " WHERE %s" % where

        return self.query(sql, data.values()).rowcount

    # like db.delete('test1', "name='ccc'")
    def delete(self, table, where=None):
        sql = f"DELETE from `{table}`"

        if where:
            sql += " WHERE %s" % where

        return self.query(sql).rowcount

    # commit must be called for inno-db table
    # or nothing will be actually done for that table
    def commit(self):
        return self.conn.commit()

    def end(self):
        self.cur.close()
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, cate, value, traceback):
        self.end()
