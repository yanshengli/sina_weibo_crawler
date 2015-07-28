# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import Queue
import time
import csv
import logging

import config
from crawler.blogcrawler import BlogCrawler, UserNotFoundError, PreprocessError
from crawler.toolkit import filelib as fl
from crawler.toolkit.accountlib import AccountManager
from crawler.usercrawler import UserCrawler

class Controller(object):
    """
    爬虫程序，负责抓取数据并保存
    """
    taskpool = Queue.Queue()  # 任务池
    finished_count = 0  # 已完成的任务数
    unexist_user_writer = None  # 不存在的用户的写入器
    noblog_user_writer = None  # 没有合法微博的用户的写入器

    @classmethod
    def load_tasks(cls):
        """
        生成任务，类方法，不能通过类的实例来调用。
        通过类名来调用，整个程序运行过程中只执行一次。
        """
        # 加载需要过滤的用户列表
        #finished_uids=open('completes.txt').read().strip().split()
        # 加载需要执行的任务
        uids = open(config.UID_FILEPATH).read().strip().split()
        print u'共', len(uids)
        for uid in uids:
            #if uid not in finished_uids:
            cls.taskpool.put(uid)

    @classmethod
    def init(cls):
        """
        执行程序前初始化，包括加载任务，初始化写入器，模拟登录等
        --------------------------------------------
        return: 初始化成功返回True，否则返回False
        """
	'''
        success = True
        # 进行模拟登录
        account_manager = AccountManager()
        try:
            while True:
                account_manager.init()
                if not account_manager.login():
                    print u'开始重新登录...'
                else:
                    break
        except Exception, e:
            print '模拟登录失败!', str(e)
            return False
	'''
        cls.load_tasks()
        cls.unexist_user_writer = open(config.UNEXIST_USER_FILEPATH, 'a')
        cls.noblog_user_writer = open(config.NOBLOG_USER_FILEPATH, 'a')
        return True

    @classmethod
    def free(cls):
        """
        程序执行结束以后释放资源
        """
        cls.unexist_user_writer.close()
        cls.noblog_user_writer.close()

    @classmethod
    def let_us_go(cls):
        """
        启动程序，包括初始化，实例化线程，以及结束以后的资源释放
        ----------------------------------------------
        thread_count: 工作线程的数量
        """
        cls.init()
        Controller().run()

    def run(self):
        """
        多线程的入口函数
        """
        # crawler = BlogCrawler()
        crawler = UserCrawler()
        while not Controller.taskpool.empty():
            uid = Controller.taskpool.get()
            print "\n已处理 %d 个任务, 还剩 %d 个任务" % (Controller.finished_count, Controller.taskpool.qsize())
            #print uid
            try:
		print 'task start'
                userinfo = crawler.scratch(uid)
		print 'task end'
                #with open('fuid.txt', 'a') as f:
                    #for fuid, un ,an ,follow_num,fans_num,weibo_num in userinfo['fui']:
                        #f.write(str(uid)+'\t'+str(fuid)+'\t'+un+'\t'+an+'\t'+str(follow_num)+'\t'+str(fans_num)+'\t'+str(weibo_num)+'\n')
                #with open('followee.txt', 'a') as f:
                    #for fuid,un,an ,a,b,c in userinfo['fui']:
                        #f.write(str(fuid)+'\n')
                    #f.write('\n')
                with open('user_repost.txt','a') as f:
                    for follow in userinfo['fui']:
                        f.write(str(uid)+'\t'+follow[0]+'\t'+follow[1]+'\t'+follow[2]+'\t'+follow[3]+'\n')
                with open('user_2_repost.txt','a') as f:
                    for follow_2 in userinfo['2_fui']:
                        f.write(follow_2[0]+'\t'+"\t".join(follow_2[1])+'\n')
                with open('completes.txt','a') as f:
                    f.write(str(uid)+'\n')
                Controller.finished_count += 1
            except:
                print uid



    @staticmethod
    def save_csv(blogs, uid):
        """
        将一组微博写到CSV文件中
        ---------------------------------
        blogs: 微博列表
        writer: 写入器
        """
        filename = Controller._get_filepath(uid)
        writer = csv.writer(file(filename, 'w'))
        writer.writerow(
            ['un', 'uid', 'iu', 'mid', 'mc', 'srn', 'run', 'ruid', 'rmc', 'pu', 'rrc', 'rcc', 'rpage', 'rpt', 'rc',
             'cc', 'page', 'pt'])
        for blog in blogs:
            writer.writerow((blog['un'], blog['uid'], blog['iu'], blog['mid'], blog['mc'], blog['srn'],
                             blog['run'], blog['ruid'], blog['rmc'], blog['pu'], blog['rrc'], blog['rcc'],
                             blog['rpage'], blog['rpt'], blog['rc'], blog['cc'], blog['page'], blog['pt']))
        print u'用户', uid, u'的微博已成功写入文件:', filename

    @staticmethod
    def _get_filepath(uid):
        """
        获取文件的保存路径
        -------------------------
        return: 保存的路径
        """
        dirpath = config.dir_root + str(config.dir_count)
        if not fl.exists(dirpath):
            fl.create_dir(dirpath)
        if not fl.exists(os.path.join(dirpath, uid + '.csv')):
            if fl.count(dirpath) >= config.MAX_FILE_COUNT:
                config.dir_count += 1
                dirpath = config.dir_root + str(config.dir_count)
                fl.create_dir(dirpath)
        return os.path.join(dirpath, uid + '.csv')
