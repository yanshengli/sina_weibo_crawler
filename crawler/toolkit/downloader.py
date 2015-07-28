# !/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import httplib
import time
import cookielib
import gzip, cStringIO

# 网页下载异常
class DownloadError(Exception):
    def __init__(self, url=''):
        self.error_msg = "Download %s error." % url ;

    def __str__(self):
        return repr(self.error_msg) ;


# 网页解码异常
class DecodeError(Exception):
    def __init__(self, url=''):
        self.error_msg = "Decode %s error." % url ;

    def __str__(self):
        return repr(self.error_msg) ;


class Downloader:
    '''
    下载器,负责下载网页资源
    '''

    def __init__(self, cookie,charset='utf-8', timeout=10, maxtry=2):
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36',
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Connection": "keep-alive",
        "Host": "weibo.com"
        }
        self.charset = charset
        self.timeout = timeout
        self.maxtry = maxtry
	self.cookie=cookie

    def use_proxy(self, proxy):
        """
        爬虫使用代理登录,代理proxy包含代理的链接和端口格式为:http://XX.XX.XX.XX:XXXX
        """
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        if proxy:
            proxy_support = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
        else:
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def use_http(self, url, params=''):
        connection = httplib.HTTPConnection('weibo.com')
        connection.request(method='GET', url=url, headers=self.headers)
        res = connection.getresponse()
        text = res.read()
        print text
        #text = gzip.GzipFile(fileobj = cStringIO.StringIO(text)).read()
        content = text.decode(self.charset, 'ignore')
        content = eval("u'''" + content + "'''").encode(self.charset)
        connection.close()
        return content

    def download(self, url, params='', try_num=0):
	
        if params != '':
            encode_params = '?' + urllib.urlencode(params)
            url += encode_params
        try:
	    self.headers['cookie']=self.cookie
	    #print 'print headers'
	    #print self.headers
            req = urllib2.Request(url, headers=self.headers)
            result = urllib2.urlopen(req, timeout=self.timeout)
            text = result.read()
	    #print '++++++++++++++'
	    #print text
	    #print '+++++++++++++++++++++'
        except Exception, e:
            #raise DownloadError(url)
            return None
        try:
            text = gzip.GzipFile(fileobj=cStringIO.StringIO(text)).read()
	    
            content = text.decode(self.charset, 'ignore')
            content = eval("u'''" + content + "'''").encode(self.charset)
        except Exception, e:
            return None
        #raise DecodeError(url)
        #self.write('tmp.html', content)
        return content

    def write(self, filepath, content):
        with open(filepath, 'w') as writer:
            writer.write(content)


if __name__ == '__main__':
    from accountlib import AccountManager

    url = 'http://weibo.com/u/1309628460'
    manager = AccountManager()
    manager.init()
    manager.login()
    downloader = Downloader()
    print downloader.download(url)
