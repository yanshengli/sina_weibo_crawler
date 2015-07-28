# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from BeautifulSoup import BeautifulSoup


class BlogParser:
    def __init__(self):
        pass

    def init_user(self, uid='', imgurl='', nickname=''):
        '''
        用户信息的初始化
        '''
        self.uid = uid
        self.username = nickname
        self.userimg = imgurl

    def init_blog(self):
        self.blog = {
        'uid': self.uid,  #用户的id
        'un': self.username,  #用户用户名
        'iu': self.userimg,  #用户头像URL
        'mid': '',  #消息id
        'mc': '',  #消息内容
        'nc': '',  #消息中@的用户
        'run': '',  #转发的消息的用户名
        'ruid': '',  #转发的消息的用户ID
        'rmc': '',  #转发的消息的内容
        'pu': '',  #消息中的图片
        'rrc': '',  #转发的消息的转发次数
        'rcc': '',  #转发的消息的评论次数
        'rpage': '',  #转发的消息的微博页面
        'rpt': '',  #转发的消息的发布时间
        'rc': '0',  #消息的转发次数
        'cc': '0',  #消息的评论次数
        'srn': '',  #消息来源
        'page': '',  #消息的微博页面
        'pt': '',  #消息的发布时间
        'feedpin': 0  #是否置顶
        }

    def parse(self, html):
        '''
        解析给定html字符串里面的微博数据
        -----------------------------------------
        html: 给定的html字符串
        --------------------------------------
        return: blog列表
        '''
        bpos = html.find('<!--feed内容-->')
        epos = html.find('<!--翻页-->', bpos)
        bloghtml = html[bpos:epos].replace('\\/', '/') + '</div>'
        soup = BeautifulSoup(bloghtml)
        blogsouplist = soup.find_all('div', class_='WB_cardwrap WB_feed_type S_bg2 ')
        bloglist = []
        for blogsoup in blogsouplist:
            self.init_blog()
            self._parse_blog(blogsoup)
            bloglist.append(self.blog)
        return bloglist

    def _parse_blog(self, blogsoup):
        '''
        解析一条微博文本
        ----------------------------------------
        blogsoup: 用BeautifulSoup包装的微博文本
        '''
        raise NotImplementedError()

    def _get_attr(self, soup, attr):
        '''
        获取soup对象的attr属性值
        -------------------------------
        soup: 获取属性值的soup对象
        attr: 待获取的属性值
        -------------------------------
        return: 成功则返回获取的属性值,否则返回空串
        '''
        attrvalue = ''
        if soup and attr in soup:
            attrvalue = soup[attr]
        return attrvalue

    def _get_text(self, soup):
        '''
        获取soup对象的text
        --------------------------------
        soup: 待获取text的soup对象
        --------------------------------
        return: 获取到的text值或返回空串
        '''
        text = ''
        if soup:
            text = soup.get_text().strip()
        return text

    def _parse_statistics(self, statsoup):
        '''
        获取 转发/评论 数
        ---------------------------------------
        statsoup: 统计数据所在html片段的BSoup对象
        ---------------------------------------
        return: 转发数,评论数
        '''
        forwardcount = '0'
        commentcount = '0'
        statstr = str(statsoup)
        bpos = statstr.find('转发(')
        if bpos != -1:
            epos = statstr.find(')', bpos)
            forwardcount = statstr[bpos + 7:epos]
        bpos = statstr.find('评论(')
        if bpos != -1:
            epos = statstr.find(')', bpos)
            commentcount = statstr[bpos + 7:epos]
        return forwardcount, commentcount

    def _parse_blog_from(self, fromsoup):
        '''
        获取微博的 地址/时间/来源 等信息
        --------------------------------------
        fromsoup: 包含以上信息片段的soup
        --------------------------------------
        return: 地址,时间,来源
        '''
        page = ''
        pt = ''
        srn = ''
        asoup = fromsoup.find('a', attrs={'node-type': 'feed_list_item_date'})
        if asoup:
            pt = asoup['title']
            page = "http://www.weibo.com" + asoup['href']
        srnsoup = fromsoup.find('a', attrs={'action-type': 'app_source'})
        if srnsoup:
            srn = srnsoup.get_text().strip()
        return page, pt, srn

    def output(self, blogmsg):
        print 'iu  is :' + blogmsg['iu']
        print 'un  is :' + blogmsg['un']
        print 'mid is :' + blogmsg['mid']
        print 'mc  is :' + blogmsg['mc']
        print 'nc  is :' + blogmsg['nc']
        print 'run is :' + blogmsg['run']
        print 'rmc is :' + blogmsg['rmc']
        print 'pu  is :' + blogmsg['pu']
        print 'rrc is :' + blogmsg['rrc']
        print 'rcc is :' + blogmsg['rcc']
        print 'rpt is :' + blogmsg['rpt']
        print 'rpage is :' + blogmsg['rpage'] ;
        print 'rc  is :' + blogmsg['rc']
        print 'cc  is :' + blogmsg['cc']
        print 'page is :' + blogmsg['page'] ;
        print 'pt  is :' + blogmsg['pt']
        print 'srn is :' + blogmsg['srn'] ;
        print '======================================'


if __name__ == '__main__':
    import sys, os

    sys.path.append(os.path.abspath('../'))
    from toolkit.downloader import Downloader
    from toolkit.accountlib import AccountAssistant

    assistant = AccountAssistant()
    from officeblogparser import OfficeBlogParser

    parser = OfficeBlogParser()
    assistant.init()
    assistant.login()
    url = 'http://weibo.com/p/1002061649159940/weibo?is_tag=0&is_search=0&pre_page=0&profile_ftype=1&visible=0&pagebar=&page=1'
    downloader = Downloader()
    content = downloader.download(url)
    parser.init_user('1649159940')
    blog_list = parser.parse(content)
    #parser.print_blog()
