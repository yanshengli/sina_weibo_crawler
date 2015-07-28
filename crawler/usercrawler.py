# -*- coding: utf-8 -*-
# ! /usr/bin/env python

# import sys
# import os
# sys.path.append(os.path.abspath('../'))
# reload(sys)
# sys.setdefaultencoding('utf-8')

import logging
from .toolkit.downloader import Downloader
from BeautifulSoup import BeautifulSoup

class UserCrawler(object):
    """
    获取用户个人信息
    """

    def __init__(self):
	cookie="SINAGLOBAL=3670791019162.063.1432519568807; ULV=1434184446636:3:1:1:9776813265987.371.1434184446576:1432539758675; SUHB=0S7S3YyGl7ABmk; YF-Ugrow-G0=169004153682ef91866609488943c77f; SUS=SID-5513307770-1434867321-GZ-fdui1-417cce02c02cba62afb4b09ce64141b5; SUE=es%3D77e325518a1eeaab4d42c04535d022d9%26ev%3Dv1%26es2%3Dda7c170b38a64fa4d9b6668f496fa074%26rs0%3DzdWWsJgKtTVoMTjEP3CWSLj5LpFJ5UF0%252BWyN6Q8Sd35saJbSk7N2YdacjGPXamqnsYetxrZNNIwMVsz0JNGf%252FkJZ%252FIv1Bh9YQHxwFkUE3K1i7kZDBboUO0yOR%252Fz0Ucw37WwoeeAGM28l5q%252FSbHFjWwe%252F3DJSj1ZdRE59Qrdrt%252Fo%253D%26rv%3D0; SUP=cv%3D1%26bt%3D1434867321%26et%3D1434953721%26d%3Dc909%26i%3D41b5%26us%3D1%26vf%3D0%26vt%3D0%26ac%3D17%26st%3D0%26uid%3D5513307770%26name%3Dmkqtx11141ua%2540163.com%26nick%3D%25E6%25AF%2581%25E9%25A6%2599%25E5%258A%2588%25E5%25BC%25B9%26fmp%3D%26lcp%3D2015-03-20%252000%253A59%253A43; YF-V5-G0=d22a701aae075ca04c11f0ef68835839; _s_tentry=login.sina.com.cn; UOR=,,login.sina.com.cn; Apache=9776813265987.371.1434184446576; YF-Page-G0=8fee13afa53da91ff99fc89cc7829b07; WBStore=0d3077cd0cad2262|undefined; SUB=_2A254giYpDeTxGeNL6lES8CnLzDyIHXVb9hDhrDV8PUJbvNBeLRjHkW8xuQX_wA9ncQZsaP1yWBfuXyq9-w..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5iPVj051o7KP9Hly_f8Jud5JpX5K-t; ALF=1466403316; SSOLoginState=1434867321; wvr=6"
	print 'start load cookie'
	print cookie
        self.downloader = Downloader(cookie)

    def _process_html(self, content):
        """
        对下载的网页进行预处理,主要是替换\/为/
        """
        if content:
            return content.replace('\\/', '/')
        return ''

    def get_url(self, upage):
        #return 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=3783364643412551&max_id=3783417797719751&page='+str(upage)
	return 'http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=3855095853042261&max_id=3856157879315930&page='+str(upage)
    def _init(self, uid):
        """
        初始化用户信息列表
        """
        self.info = {
            'uid': uid,
            'time': '2014-12-02 16:11:00',
            'info_id':'3741311679142648',
            'source_equip':'皮皮时光机',
            'repost_num':1880,
            'fui': [],#一度好友
            '2_fui': []#N度好友
        }

    def _get_followee(self, uid):
        """
        获取user info repost info
        """
        followee_list = []
        repost_list=list()
        followee_set = set()
        for i in range(1,219):
            html_data = self.downloader.download(self.get_url(i))
            html_data = self._process_html(html_data)
	    #print html_data
            if html_data is not None:
                    try:
                        soup = BeautifulSoup(html_data.decode('utf-8', 'ignore'))
                        #followee_html_list= soup.findAll('div')
			#print followee_html_list
                        followee_html_list=soup.findAll('div',attrs={'class':'list_li S_line1 clearfix'})
			#print followee_html_list
                        for followee_html in followee_html_list:
                            #print followee_html
                            repost_use_list=list()
                            info_connect=followee_html.find('div',attrs={'class':'WB_face W_fl'})
			    #print info_connect
                            if info_connect is None:continue
                            if info_connect.find('img') is None:
                                continue
                            else:                              
                                follow_id=info_connect.find('img')                                
		     	   	print 'repost',follow_id['alt']
                                print 'image',follow_id['src']
                                #followee_list.append((info_connect['usercard'][3:],info_connect['alt']))
			    
                            after_data=followee_html.find('div',attrs={'class':'list_con'})
			    #print after_data
                            repost_2=after_data.find('span')
                            if repost_2.find('a') is not None:
                                repost_n_user=repost_2.findAll('a')
                                for repost_user in repost_n_user:
                                    print '2repost',repost_user.text
                                    if repost_user.text.find('http:')>=0:
                                        continue
                                    repost_use_list.append(repost_user.text)
                                #repost_user=repost_2.find('a').text
                                if len(repost_use_list)>0:
                                    repost_list.append((follow_id['usercard'][3:],repost_use_list))
                            time_user=after_data.find('div',attrs={'class':'WB_from S_txt2'})
                            time_list=time_user.find('a')['title']
                            followee_list.append((follow_id['usercard'][3:],follow_id['alt'],follow_id['src'],time_list))
                    except Exception, e:
                        logging.exception("获取好友列表异常:" + uid + str(e))
        self.info['fui'] = followee_list
        self.info['2_fui']=repost_list
        print self.info

    def scratch(self, uid):
        """
        抓取用户的个人信息
        ----------------------------------
        return：用户个人信息列表
        """
        self._init(uid)
        #self._get_basic_info(uid)
        self._get_followee(uid)
        return self.info



