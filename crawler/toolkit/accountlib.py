# ! /usr/bin/env python
# -*- coding: utf-8 -*-

# 提供新浪微博的登录/退出等功能
# tbin (binTang.hit@gmail.com)
# 2013-12-1

import os
import sys
import urllib
import urllib2
import urlparse
import cookielib
import base64
import re
import json
import hashlib
import rsa
import binascii
import time
import random

# 账户登录异常
class LoginError(Exception):
    def __init__(self, account=''):
        self.error_msg = "Account %s login failed." % account

    def __str__(self):
        return repr(self.error_msg)


# 服务器超时异常
class ServerTimeError(Exception):
    def __init__(self, account=''):
        self.error_msg = "Account %s login exceed time error." % account

    def __str__(self):
        return repr(self.error_msg)


# 用户退出异常
class LogoutError(Exception):
    def __init__(self, account=''):
        self.error_msg = "Account %s log out failed." % account

    def __str__(self):
        return repr(self.error_msg)


# 新浪微博账户助手,提供账户的登录/退出等功能
class AccountManager:
    def init(self, proxy=None):
        cj = cookielib.LWPCookieJar()
        cookie_support = urllib2.HTTPCookieProcessor(cj)
        if proxy:
            proxy_support = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
        else:
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)

    def __init__(self):
        self.cur_user = ''  # 当前登录账户名
        self.pre_user = ''  # 上一个登录的账号
        self.loginpostdata = dict()
        self.accounts = list()
        pardir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        account_filepath = os.path.abspath(os.path.join(pardir, 'account.txt'))
        self.load_accounts(account_filepath)

    def __init_data(self):
        self.loginpostdata = {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'useticket': '1',
            'pagerefer': '',
            'pcid': '',
            'door': '',  # 验证码
            'vsnf': '1',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv': '',
            'sp': '',
            'sr': '',
            'encoding': 'UTF-8',
            'prelt': '115',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }

    # 获取服务器的一些数据
    def get_serverdata(self, username):
        url = 'http://login.sina.com.cn/sso/prelogin.php?' \
              'entry=weibo&callback=sinaSSOController.preloginCallBack&su={username}&rsakt=mod&checkpin=1&' \
              'client=ssologin.js(v1.4.18)&_={time}'
        url = url.format(username=self.encode_username(username), time=int(time.time() * 1000))
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            pubkey = data['pubkey']
            rsakv = data['rsakv']
            showpin = data['showpin']  # 是否需要验证码
            pcid = data['pcid']  # 验证码id
            return servertime, nonce, pubkey, rsakv, showpin, pcid
        except:
            raise ServerTimeError(username)

    # 对用户密码进行编码
    def encode_pwd(self, password, servertime, nonce, pubkey):
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
        passwd = rsa.encrypt(message, key)  # 加密
        passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
        return passwd

    # 对用户名进行编码
    def encode_username(self, username):
        username_ = urllib.quote(username)
        username = base64.encodestring(username_)[:-1]
        return username

    def load_accounts(self, filepath):
        """
        从文件中加载新浪微博账号信息,[(user, password),...]
        --------------------------------------
        filepath: 新浪微博账号数据文件所在路径,一行一个账号,账号名和密码用\t分隔
        """
        self.accounts = []
        with file(filepath) as f:
            for line in f:
                parts = line.strip().split('\t')  # 去掉每行账户前后空白
                self.accounts.append((parts[0], parts[1]))

    def get_account(self):
        """
        获取一个账户
        ---------------------
        return: account,password
        """
        username = ''
        password = ''
        if self.pre_user == '':
            username = self.accounts[0][0]
            password = self.accounts[0][1]
        else:
            for i in range(0, len(self.accounts)):
                account = self.accounts[i]
                if self.pre_user == account[0]:
                    index = (i + 1) % len(self.accounts)
                    username = self.accounts[index][0]
                    password = self.accounts[index][1]
                    break
        self.cur_user = username
        return username, password

    # 新浪微博账户模拟登录
    def login(self):
        username, pwd = self.get_account()
        self.__init_data()
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
        try:
            (servertime, nonce, pubkey, rsakv, showpin, pcid) = self.get_serverdata(username)
            if showpin:  # 需要验证码
                filename = 'data/pin.png'
                if self.get_pin(pcid, filename):  # 如果成功获取验证码则显示
                    from PIL import Image
                    import subprocess
		    print 'yes'
                    proc = subprocess.Popen(['display', filename])
                    self.loginpostdata['pcid'] = pcid
                    self.loginpostdata['door'] = raw_input(u'请输入验证码：')
                    os.remove(filename)
                    proc.kill()
                else:
                    print u'验证码获取失败,暂时退出!'
                    exit(0)
        except Exception, e:
            print e
            raise ServerTimeError(username)
        self.loginpostdata['servertime'] = servertime
        self.loginpostdata['nonce'] = nonce
        self.loginpostdata['rsakv'] = rsakv
        self.loginpostdata['su'] = self.encode_username(username)
        self.loginpostdata['sp'] = self.encode_pwd(pwd, servertime, nonce, pubkey)
        self.loginpostdata_encode = urllib.urlencode(self.loginpostdata)
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11 Linux i686 rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}
        req = urllib2.Request(
            url=url,
            data=self.loginpostdata_encode,
            headers=headers
        )
        result = urllib2.urlopen(req)
        text = result.read()
        # p = re.compile('location\.replace\(\"(.*)\"\)')  # 此处和之前略有区别，小心！
        try:
            # login_url = p.search(text).group(1)
            btag = 'location.replace("'
            etag = '");'
            bpos = text.find(btag)
            if bpos != -1:
                bpos += len(btag)
                epos = text.find(etag, bpos)
            else:
                bpos = text.find(btag.replace('"', "'")) + len(btag)
                epos = text.find(etag.replace('"', "'"), bpos)
            login_url = text[bpos:epos]
            # print login_url
            query_string = urlparse.parse_qs(urlparse.urlparse(login_url).query)
            # print query_string
            if not int(query_string['retcode'][0]):  # retcode = 0 登录成功
                feedback = urllib2.urlopen(login_url).read()
                # print feedback
                p = re.compile('\((.*)\)')
                feedback = json.loads(p.search(feedback).group(1))
                if feedback['result']:
                    print username, u'登录成功!'
                    # print feedback['userinfo']['displayname'], u'登录成功!'
                    return True
                else:
                    print username, u'登录失败！'
                    print u'错误代码:', feedback['errno']
                    return False
            else:
                print username, u'登录失败！'
                print u'错误代码:', query_string['retcode'][0]
                print u'错误提示:', query_string['reason'][0].decode('gbk')
                print
                return False
        except Exception, e:
            print e
            raise LoginError(username)

    # 退出登录当前用户
    def logout(self):
        is_logout = False
        logout_url = 'http://weibo.com/logout.php?backurl=%2F'
        try:
            urllib2.urlopen(logout_url)
            if not self.is_login():
                is_logout = True
                self.pre_user = self.cur_user
                self.cur_user = ''
        except Exception, e:
            raise LogoutError(self.cur_user)
        return is_logout

    # 更换登录账户
    def change_account(self):
        self.logout()
        self.login()
        print self.cur_user

    # 验证当前账户是否登录成功,登录成功返回True
    def is_login(self):
        url = 'http://weibo.com'
        req = urllib2.Request(url)
        result = urllib2.urlopen(req, timeout=5)
        text = result.read()
        if text.find('<div class="W_login_form" node-type="pl_login_normal">') != -1:
            return False
        else:
            return True

    def get_pin(self, pcid, filename):
        """
        获取验证码图片
        :param pcid:
        :param filename:
        :return
        """
        try:
            url = 'http://login.sina.com.cn/cgi/pin.php?r={randint}&s=0&p={pcid}'
            url = url.format(randint=random.randint(1000000, 99999999), pcid=pcid)
            urllib.urlretrieve(url, filename)
            if os.path.isfile(filename):
                return True
            else:
                return False
        except:
            pass

if __name__ == '__main__':
    tel = '13322931529'
    account = AccountManager()
    account.login('aishlinn219640801@163.com', '1234qwer')
