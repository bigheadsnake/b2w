#!/usr/bin/python3
# -*-coding:UTF-8-*-


# 没有任何限制
no_limit_urls = {
    '/': 1,
    '/entry': 1
}

def nav_display_flags(db, user):
    return {}


def can_access(db, user, url):
    if url in no_limit_urls:
        return True

    if user.logged:
        return True

    return False
