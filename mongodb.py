__author__ = 'LiGe'
#encoding:utf-8
import pymongo
import os
import csv

class mongodb(object):
    def __init__(self, ip, port):
        self.ip=ip
        self.port=port
        self.conn=pymongo.MongoClient(ip,port)

    def close(self):
        return self.conn.disconnect()

    def get_conn(self):
        return self.conn

if __name__=='__main__':
    conn=mongodb('219.223.245.53',27017)
    data_conn=conn.get_conn()
    dc=data_conn.weibo
    dc.authenticate('lige', '123') # check auth
    file_data_path='D:/python_workspace/data0'
    files=os.listdir(file_data_path)
    for file_data in files:
        print file_data
        user=file_data.split('.')[0]
        if dc.user.find_one({'user_id':user}) is None:
            dc.user.insert({'user_id':user})
        else:
            continue
        num=0
        for line in csv.reader(file(file_data_path+'\\'+file_data,'rb')):
            if num==0:
                num=num+1
                continue
            else:
                #print 'ok'
                dc.info.insert({"un":line[0],"uid":line[1],"iu":line[2],"mid":line[3],"mc":line[4],"srn":line[5]
                ,"run":line[6],"ruid":line[7],"rmc":line[8],"pu":line[9],"rrc":line[10],"rcc":line[11],"rc":line[12]
                    ,"cc":line[13],"pt":line[14],"nc":line[15]},save=True)
                num=num+1