#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/2 14:25
# @Author  : Echean
# @File    : Login_CMCC.py
# @Software: PyCharm

import requests
from http import cookiejar
import time
import logging
import json
import execjs

session = requests.session()
logging.basicConfig(level=logging.INFO)


class Login_CMCC(object):
    def __init__(self):
        self.session = session
        self.session.cookie = cookiejar.LWPCookieJar('cookie.txt')

    def _check_need_verify(self, phone_num):
        _check_need_verify_url = 'https://login.10086.cn/needVerifyCode.htm'
        query_string = {
            'accountType': '01',
            'account': phone_num,
            'timestamp': int(time.time() * 1000),
        }
        Headers = {
            'Host': 'login.10086.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Referer': 'https://login.10086.cn/login.html?'
                       'channelID=12003&'
                       'backUrl=http://shop.10086.cn/i/?f=billdetailqry',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _check_need_verify_resp = self.session.get(url=_check_need_verify_url, params=query_string, headers=Headers)
        logging.info('_check_need_verify_resp: %s %s' % (_check_need_verify_resp.status_code,
                                                         _check_need_verify_resp.text))
        return json.loads(_check_need_verify_resp.text)['needVerifyCode']

    def _chkNumberAction(self, phone_num):
        _chkNumberAction_url = 'https://login.10086.cn/chkNumberAction.action'
        Datas = {
            'userName': phone_num,
        }
        Headers = {
            'Host': 'login.10086.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://login.10086.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://login.10086.cn/login.html?'
                       'channelID=12003&'
                       'backUrl=http://shop.10086.cn/i/?f=billdetailqry',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _chkNumberAction_resp = self.session.post(url=_chkNumberAction_url, data=Datas, headers=Headers)
        logging.info('_chkNumberAction_resp: %s %s' % (_chkNumberAction_resp.status_code,
                                                       _chkNumberAction_resp.text))
        return _chkNumberAction_resp.text

    def _sendRandomCodeAction(self, phone_num):
        _sendRandomCodeAction_url = 'https://login.10086.cn/sendRandomCodeAction.action'
        Datas = {
            'userName': phone_num,
            'type': '01',
            'channelID': '12003',
        }
        Headers = {
            'Host': 'login.10086.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'https://login.10086.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://login.10086.cn/login.html?'
                       'channelID=12003&'
                       'backUrl=http://shop.10086.cn/i/?f=billdetailqry',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _sendRandomCodeAction_resp = self.session.post(url=_sendRandomCodeAction_url, data=Datas, headers=Headers)
        logging.info('_sendRandomCodeAction_resp: %s %s' % (_sendRandomCodeAction_resp.status_code,
                                                            _sendRandomCodeAction_resp.text))
        smsCode = input('请输入短信验证码：')
        return smsCode

    def _get_js(self):
        phantom = execjs.get('PhantomJS')
        with open("encrypt.js", 'r', encoding='utf-8') as f:
            source = f.read()
        return phantom.compile(source)

    def _get_pwd(self, pwd):
        jsstr = self._get_js()
        return jsstr.call('encrypt', pwd)

    def _post_login(self, phone_num, password, smscode):
        _post_login_url = 'https://login.10086.cn/login.htm'
        query_string = {
            'accountType': '01',
            'account': phone_num,
            'password': password,
            'pwdType': '01',
            'smsPwd': smscode,
            'inputCode': '',
            'backUrl': 'http://shop.10086.cn/i/?f=billdetailqry',
            'rememberMe': '0',
            'channelID': '12003',
            'protocol': 'https:',
            'timestamp': int(time.time() * 1000)
        }
        Headers = {
            'Host': 'login.10086.cn',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Referer': 'https://login.10086.cn/login.html?'
                       'channelID=12003&'
                       'backUrl=http://shop.10086.cn/i/?f=billdetailqry',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _post_login_resp = self.session.get(url=_post_login_url, params=query_string, headers=Headers)
        logging.info('_post_login_resp: %s %s' % (_post_login_resp.status_code,
                                                  _post_login_resp.text))
        return _post_login_resp.text

    def login(self):
        phone_num = input('请输入手机号:')
        server_pwd = input('请输入服务密码:')
        self._check_need_verify(phone_num)
        self._chkNumberAction(phone_num)
        smsCode = self._sendRandomCodeAction(phone_num)
        server_pwd_encrypt = self._get_pwd(server_pwd)
        self._post_login(phone_num, server_pwd_encrypt, smsCode)


if __name__ == '__main__':
    user = Login_CMCC()
    user.login()
