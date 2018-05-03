#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/2 17:21
# @Author  : Echean
# @File    : My_requests.py
# @Software: PyCharm

import requests
from http import cookiejar


class MyRequests(object):
    def get_requests(self):
        session = requests.session()
        session.cookies = cookiejar.LWPCookieJar('cookies.txt')
        try:
            session.cookies.load(ignore_discard=True)
            flag = 1
        except FileNotFoundError:
            flag = 0
        return session

