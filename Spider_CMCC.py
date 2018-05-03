#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/2 16:03
# @Author  : Echean
# @File    : Spider_CMCC.py
# @Software: PyCharm

import requests
from http import cookiejar
import random
from PIL import Image
import logging
import time
import json
import base64
import re

# session = requests.session()
logging.basicConfig(level=logging.INFO)


class Spider(object):
    def __init__(self, my_session):
        self.session = my_session
        # self.session.cookies = cookiejar.LWPCookieJar('cookies.txt')

    def _get_authImag(self):
        _get_authImage_url = 'http://shop.10086.cn/i/authImg'
        query_string = {
            't': int(random.random() * 10000000000000000) / 10000000000000000,
        }
        Headers = {
            'Host': 'shop.10086.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'http://shop.10086.cn/i/?f=billdetailqry&welcome=1525251281507',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _get_authImage_resp = self.session.get(url=_get_authImage_url, params=query_string, headers=Headers)
        logging.info('_get_authImage_resp: %s' % _get_authImage_resp.status_code)
        with open('captcha.jpg', 'wb') as f:
            f.write(_get_authImage_resp.content)
        img = Image.open('captcha.jpg')
        img.show()
        captcha = input('请输入验证码：')
        return captcha

    def _get_percheck(self, phone_num, captcha):
        _get_percheck_url = 'http://shop.10086.cn/i/v1/res/precheck/{0}'.format(phone_num)
        query_string = {
            'captchaVal': captcha,
            '_': int(time.time() * 1000),
        }
        Headers = {
            'Host': 'shop.10086.cn',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-store, must-revalidate',
            'pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Content-Type': '*',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'If-Modified-Since': '0',
            'expires': '0',
            'Referer': 'http://shop.10086.cn/i/?f=billdetailqry&welcome=1525251281507',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _get_percheck_resp = self.session.get(url=_get_percheck_url, params=query_string, headers=Headers)
        logging.info('_get_percheck_resp: %s' % _get_percheck_resp.text)
        return json.loads(_get_percheck_resp.text)['retMsg']

    def _get_Randomcode(self, phone_num):
        _get_Randomcode_url = 'https://shop.10086.cn/i/v1/fee/detbillrandomcodejsonp/{0}'.format(phone_num)
        query_string = {
            'callback': 'jQuery1830' + str(int(random.random() * 100000000000000000)),
            '_': int(time.time() * 1000)
        }
        Headers = {
            'Host': 'shop.10086.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'http://shop.10086.cn/i/?f=billdetailqry&welcome=1525251281507',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _get_Randomcode_resp = self.session.get(url=_get_Randomcode_url, params=query_string, headers=Headers)
        logging.info('_get_Randomcode_resp: %s' % _get_Randomcode_resp.text)
        sms_random_code = input('请输入二次短信验证码：')
        return sms_random_code

    def _get_base64(self, pwd):
        pwd_byte = bytes(pwd, encoding='utf-8')
        base64_pwd = base64.b64encode(pwd_byte)
        return str(base64_pwd, encoding='utf-8')

    def _get_tempident(self, phone_num, pwd, sms, cap):
        _get_tempident_url = 'https://shop.10086.cn/i/v1/fee/detailbilltempidentjsonp/{0}'.format(phone_num)
        query_string = {
            'callback': 'jQuery1830' + str(int(random.random() * 100000000000000000)),
            'pwdTempSerCode': self._get_base64(pwd),
            'pwdTempRandCode': self._get_base64(sms),
            'captchaVal': cap,
            '_': int(time.time() * 1000),
        }
        Headers = {
            'Host': 'shop.10086.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'http://shop.10086.cn/i/?f=billdetailqry&welcome=1525251281507',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _get_tempident_resp = self.session.get(url=_get_tempident_url, params=query_string, headers=Headers)
        logging.info('_get_tempident_resp: %s' % _get_tempident_resp.text)
        return json.loads(re.findall(r'{.*?}', _get_tempident_resp.text)[0])['retMsg']

    def _get_detialBill(self, phone_num):
        billtype = input('请输入要查询的详单类型（01：电话 02：短信 03：流量 04：余额）：')
        month = input('请输入要查询的月份（近六个月，格式如：201804）：')
        _get_detialBill_url = 'https://shop.10086.cn/i/v1/fee/detailbillinfojsonp/{0}'.format(phone_num)
        query_string = {
            'callback': 'jQuery1830' + str(int(random.random() * 100000000000000000)),
            'curCuror': '1',
            'step': '100',
            'qryMonth': month,
            'billType': billtype,
            '_': int(time.time() * 1000),
        }
        Headers = {
            'Host': 'shop.10086.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'http://shop.10086.cn/i/?f=billdetailqry&welcome=1525251281507',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        _get_detialBill_resp = self.session.get(url=_get_detialBill_url, params=query_string, headers=Headers)
        logging.info('_get_detialBill_resp: %s' % _get_detialBill_resp.text)
        return _get_detialBill_resp.text

    def get_parse(self, phone_num, pwd):
        while True:
            smsCode = self._get_Randomcode(phone_num)
            while True:
                captcha = self._get_authImag()
                ret = self._get_percheck(phone_num, captcha)
                if ret == '输入正确，校验成功':
                    break
                else:
                    print('验证码校验失败，请重新输入')
            ret_code = self._get_tempident(phone_num, pwd, smsCode, captcha)
            if ret_code == '认证成功!':
                break
        while True:
            print(self._get_detialBill(phone_num))
            jx = input('是否还要继续查询（y/n）：').strip()
            if jx.lower() != 'y':
                break


if __name__ == '__main__':
    my_session = requests.session()
    get_spider = Spider(my_session)
    get_spider.get_parse('13554xxxxxx', '027xxx')
