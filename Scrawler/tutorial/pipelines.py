# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
import MySQLdb
import hashlib
from scrapy.exceptions import DropItem
from scrapy.http import Request

class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(host="mysql.server", # your host, usually localhost
                         user="gasmanager", # your username
                          passwd="pw", # your password
                          db="gasmanager$GMData", charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        x = item['address'][0].encode('utf-8')
        y = item['price'][0].encode('utf-8')
        self.cursor.execute('SELECT * FROM gm_gasstation WHERE address=%s',(x,))
        self.conn.commit()
        if len(self.cursor.fetchmany()) == 0 and y != "$0.0":
            try:
                self.cursor.execute('INSERT INTO gm_gasstation(name, address, price, location) VALUES ("%s","%s","%s","%s")' % (item['name'][0].encode('utf-8'),x,y,item['location'][0].encode('utf-8')))
                self.conn.commit()
            except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])


        return item