__author__ = 'q'
from twisted.internet import reactor

from scrapy import log, signals
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.xlib.pydispatch import dispatcher

from spiders.dmoz_spider import PriceSpider
import MySQLdb

class GasCrawler(object):
	
	def stop_reactor(self):
	    reactor.stop()

	def run(self):
		dispatcher.connect(self.stop_reactor, signal=signals.spider_closed)
		spider = PriceSpider()
		testset = Settings()
		testset.set("ITEM_PIPELINES",{
		    'tutorial.pipelines.MySQLStorePipeline': 1
		})
		crawler = Crawler(testset)
		crawler.configure()
		crawler.crawl(spider)
		crawler.start()
		log.start()
		log.msg('Running reactor...')
		reactor.run(installSignalHandlers=0)  # the script will block here until the spider is closed
		log.msg('Reactor stopped.')

conn2 = MySQLdb.connect(host="mysql.server", # your host, usually localhost
                         user="gasmanager", # your username
                          passwd="pw", # your password
                          db="gasmanager$GMData", charset="utf8", use_unicode=True)
cursor2 = conn2.cursor()
cursor2.execute('DELETE FROM gm_gasstation')
conn2.commit()
g = GasCrawler()
g.run()