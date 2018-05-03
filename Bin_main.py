#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 10:14
# @Author  : Echean
# @File    : Bin_main.py
# @Software: PyCharm

from My_requests import MyRequests
from Login_CMCC import LoginCMCC
from Spider_CMCC import Spider
import time

if __name__ == '__main__':
    Session = MyRequests()
    my_session = Session.get_requests()
    user_login = LoginCMCC(my_session)
    phone_num, pwd, my_session = user_login.login()
    print('请等待50秒.....')
    time.sleep(50)
    user_parse = Spider(my_session)
    user_parse.get_parse(phone_num, pwd)
    my_session.cookies.save()