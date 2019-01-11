#!/usr/bin/python3
# -*-coding:UTF-8-*-
import dbutils

# fields that do not need to show
HIDDEN_FIELDS = {
    "cargo_management": ["cargo_id"]
}


def get_hidden_cond(tbl_name):
    return " Field NOT IN ('" + "','".join(HIDDEN_FIELDS[tbl_name]) + "')"


def get_fields(db, tbl_name, field_name):
    if field_name == 'title':
        index = -1
    elif field_name == "field":
        index = 0
    else:
        index = 0
    sql = 'SHOW FULL COLUMNS FROM ' + tbl_name + ' WHERE ' + get_hidden_cond(tbl_name)
    cursor = dbutils.query_multiple(db, sql)
    titles = [s[index] for s in cursor]
    return titles
