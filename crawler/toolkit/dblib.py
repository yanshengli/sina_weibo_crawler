# !/usr/bin/python
#-*- coding: utf-8 -*-

import MySQLdb as mdb
import MySQLdb.cursors
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class DBManager:
    def __init__(self, host, user, passwd, db=None):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.conn = None
        self.cursor = None
        self.db = db

    def __connect(self, db=None):
        if db or self.db:
            try:
                if db:
                    self.conn = mdb.connect(self.host, self.user, self.passwd, db)
                else:
                    self.conn = mdb.connect(self.host, self.user, self.passwd, self.db, charset='utf8')
            except Exception, e:
                print e
                return
        else:
            try:
                self.conn = mdb.connect(self.host, self.user, self.passwd)
            except Exception, e:
                print e
                return
        self.cursor = self.conn.cursor()

    #self.cursor = mdb.cursors.DictCursor(self.conn)

    def __close(self):
        if self.cursor:
            try:
                self.cursor.close()
                del self.cursor
            except Exception, e:
                print e
        if self.conn:
            try:
                self.conn.close()
                del self.conn
            except Exception, e:
                print e

    def select(self, query, db=None):
        self.__connect(db)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        self.__close()
        return data

    def select_one(self, query, db=None):
        self.__connect(db)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        self.__close()
        return data

    def insert(self, query, value=None, db=None):
        self.__connect(db) ;
        if value:
            self.cursor.execute(query, value) ;
        else:
            self.cursor.execute(query)
        rowid = self.cursor.lastrowid ;
        self.conn.commit() ;
        self.__close() ;
        return rowid ;

    def insert_many(self, query, values, db=None):
        self.__connect(db) ;
        self.cursor.executemany(query, values) ;
        rowcount = self.cursor.rowcount
        self.conn.commit() ;
        self.__close() ;
        return rowcount ;

    def __getRC(self):
        if (hasattr(self.cursor, 'rowcount')):
            return self.cursor.rowcount ;
        else:
            return -1 ;

    def update(self, query, value=None, db=None):
        self.__connect(db)
        if value:
            self.cursor.execute(query, value)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        count = self.__getRC() ;
        self.__close()
        return count

    def delete(self, query, value=None, db=None):
        self.__connect(db)
        if value:
            self.cursor.execute(query, value)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        count = self.__getRC() ;
        self.__close()
        return count

    def get_last_query(self):
        return self.cursor._last_executed ;


if __name__ == '__main__':
    db = DBAssistant('localhost', 'root', '', 'ecshop') ;
    #print db.insert_many("INSERT INTO ecs_brand (brand_name) VALUES (%s)", [['test7'],['test8']]);
    #db.delete("DELETE  FROM ecs_brand WHERE brand_name=%s", ['test9']);
    #print db.get_last_query();
    #res = db.select_one("SELECT count(brand_name) FROM ecs_brand WHERE brand_name='%s'"%'诺基亚');
    #print res[0];
    update_mt = '175,599'
    db.update("UPDATE `abbreviation` SET mt=%s WHERE abrid IN (" + update_mt + ")", [utility.now()]) ;