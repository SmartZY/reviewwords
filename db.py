#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'zhaoyuan'
import MySQLdb as mdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class db(object):
	def __init__(self):
		pass
	def connectdb(self):
		try:		
			self.conn = mdb.connect('localhost','root','123456','words',charset='utf8')
		except mdb.Error,e:
			print 'Mysql Error %d: %s' &(e.args[0],e.args[1])
	def closedb(self):
		self.conn.close()
	def executesql(self,sql):
		if self.conn:
			cur = self.conn.cursor()
			try:
				cur.execute(sql)
				self.conn.commit()
				return cur
			except mdb.Error,e:
				print 'Mysql Error %d: %s' &(e.args[0],e.args[1])
		else:
			print 'db has been closed'
			return None


if __name__ == '__main__':
	database = db()
	database.connectdb()
	cur = database.executesql('select * from word')
	if cur:
		data = cur.fetchone()
		while data is not None:
			for k in data:
				print k,
			data = cur.fetchone()
	database.closedb()

