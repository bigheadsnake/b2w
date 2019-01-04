# encoding=utf-8
import os
from mysqlobj import MysqlObj


def noisy_get_env(k, dft=None):
    v = os.getenv(k, dft)
    if v is None:
        assert isinstance(k, object)
        raise RuntimeError("%s is not found in environ" % k)
    return v


def get_db(dbname: object = None) -> object:
    """

    :rtype: object
    """
    dbconf = {}
    if dbname is None:
        dbname = 'b2w'
    tpl = "CONF_MYSQL_{}_{}".format
    uppername = dbname.upper()
    dbconf['host'] = noisy_get_env(tpl(uppername, 'HOST'))
    dbconf['port'] = int(noisy_get_env(tpl(uppername, 'PORT'), 3306))
    dbconf['user'] = noisy_get_env(tpl(uppername, 'USER'))
    dbconf['passwd'] = noisy_get_env(tpl(uppername, 'PASSWD'))
    dbconf['db'] = noisy_get_env(tpl(uppername, 'DB'))

    db = MysqlObj(**dbconf)
    return db


def del_data(db, tbl_name, where=None):
    db.delete(tbl_name, where)
    db.commit()


def set_data(db, tbl_name, recs, interval=2048, replace_flag=False):
    #    for rec in recs:
    #        db.insert_list(tbl_name, rec)
    total = len(recs)
    offset = 0
    if total > 0:
        while offset < total:
            subrecs = recs[offset:offset + interval]
            offset = offset + interval
            if replace_flag:
                db.replace_many(tbl_name, data=subrecs)
            else:
                db.insert_many(tbl_name, data=subrecs)
            db.commit()


def insert_or_update_data(db, tbl_name, update_fields, recs, interval=2048):
    total = len(recs)
    offset = 0
    if total > 0:
        while offset < total:
            subrecs = recs[offset:offset + interval]
            offset = offset + interval
            db.insert_ondup_many(tbl_name, update_fields, data=subrecs)
            db.commit()


def get_table_dat(db, tbl_name, sortfield=None, order='', limit=None, where=None, select_fields='*'):
    query = db.form_sql(tbl_name, sortfield, order, limit, where, select_fields)
    result = db.get_all(query)

    fields = None
    rows = []
    if result:
        fields = [f[0] for f in db.cur.description]
        for row in result:
            rows.append(list(row))
    return fields, rows


# 返回 cursor
def raw_query(db, sql, params=None):
    return db.query(sql, params)


# 返回类似 (u'2014-12-08',) or None
def query_single(db, query):
    return db.get_one(query)


# 返回类似 ((u'2014-12-08',), (u'2014-12-08',), (u'2014-12-08',)) or ()
def query_multiple(db, query):
    return db.get_all(query)


# 返回 generator
def query_next(db, sql, params=None):
    return db.get_next(sql, params=params)


# 返回 generator of namedtuple
def query_next_namedtuple(db, sql, params=None, prefix='', fieldformat=None):
    return db.get_next_named_tuple(sql, params=params, prefix=prefix, fieldformat=fieldformat)


# del_fields is a list
# if data_flag='list', data will be a list of list, corresponding the del_fields
# if data_flag='dict', data will be a list of dict, whose keys() contains del_fields
def del_multi_data(db, tbl_name, del_fields, data, interval=1024, data_flag='list'):
    total = len(data)
    offset = 0
    if total > 0:
        where = ' and '.join("%s=" % f + "%s" for f in del_fields)
        while offset < total:
            subrecs = data[offset:offset + interval]
            offset = offset + interval

            num = len(subrecs)
            multi_where = ' or '.join(["(%s)" % where] * num)
            sql = "delete from %s where %s" % (tbl_name, multi_where)

            params = []
            for rec in subrecs:
                if data_flag == 'list':
                    params += rec
                else:
                    for f in del_fields:
                        params.append(rec[f])

            db.query(sql, params)
        db.commit()


def update_table_dat(db, tbl_name, upd_data, where=None):
    db.update(tbl_name, upd_data, where)
    db.commit()


def commit(db):
    db.commit()


def close(db):
    db.end()
