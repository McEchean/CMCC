#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/2 17:21
# @Author  : Echean
# @File    : My_requests.py
# @Software: PyCharm

import requests
from http import cookiejar


class My_requests(object):
    def get_requests(self):
        session = requests.session()
        session.cookies = cookiejar.LWPCookieJar('cookies.txt')
        return session