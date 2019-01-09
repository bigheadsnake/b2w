#!/usr/bin/python3
# -*-coding:UTF-8-*-
import dbutils

# fields that do not need to show
HIDDEN_FIELDS = {
    "cargo_management": ["cargo_id"]
}


def get_hidden_cond(tbl_name):
    return " AND COLUMN_NAME NOT IN ('" + "','".join(HIDDEN_FIELDS[tbl_name]) + "')"


def get_all_fields(db, tbl_name):
    cursor = dbutils.query_multiple(db, 'SHOW FULL COLUMNS FROM "' + tbl_name + '"')
    print(cursor)


def get_fields_titles(db, tbl_name):
    sql = 'SELECT COLUMN_COMMENT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = "' \
          + db.conf['db'] + '" AND TABLE_NAME="' + tbl_name + '"'
    sql += get_hidden_cond(tbl_name)
    cursor = dbutils.query_multiple(db, sql)
    titles = [s[0] for s in cursor]
    return titles
