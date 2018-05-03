#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/2 17:28
# @Author  : Echean
# @File    : test.py
# @Software: PyCharm

import random
import base64

print(int(random.random() * 10000000000000000)/10000000000000000)

s = input()
s = bytes(s, encoding='utf-8')
print(str(base64.b64encode(s), encoding='utf-8'))
