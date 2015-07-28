#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import logging
from controller import Controller

if __name__ == '__main__':
    logging.basicConfig(filename='log/weibo.log', filemode='w',
                        format='[%(asctime)s] - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    Controller.let_us_go()
