# -*- coding: UTF-8 -*-

import db
import datetime
import sys
import config.config as config
reload(sys)
sys.setdefaultencoding('utf-8')

__author__ = 'zhaoyuan'

func_words = config.function_words().get_func_words()

class words(object):
        def __init__(self):
                self.database = db.db()
                self.database.connectdb()
		self.wordsarray=[]
        def get_words_from_db(self,sql):
		cur = self.database.executesql(sql)
		if cur:
			data = cur.fetchone()
			while data is not None:
				self.wordsarray.append(data)
				data = cur.fetchone()
        def entering_words(self,data):
		#stupid insert
		if isinstance(data,list):
			flag = self.if_words_has_existed(data[0],data[1])
			if flag == 'yes':
				return 'word has existed'
			
			elif flag == 'word duplicate':
				sql = "update word set meaning = CONCAT(meaning,',%s') where words='%s'" %(data[1],data[0])
				self.database.executesql(sql)
			else:
				data_to_insert=[]
				for item in data:
					data_to_insert.append(item)
				data_to_insert.append(datetime.date.today())
				data_to_insert.append(0)	
				data_to_insert.append(0)
				self.wordsarray.append(data_to_insert)
				#insert data to db
				sql = "insert into word values('%s','%s','%s','%s','%s')" \
				 %(data_to_insert[0],data_to_insert[1].encode('utf-8'),data_to_insert[2],data_to_insert[3],data_to_insert[4])
				self.database.executesql(sql)
        def match_words(self,word,meaning):
		if self.wordsarray :
			for tupleitem in self.wordsarray:
				if tupleitem[0] == word:
					#stupid match
					if self.match_func(meaning,tupleitem[1]):
						sql = 'update word set review_count = review_count + 1 where words = "%s"' % word
						self.database.executesql(sql)
						return True
					else:
						sql = 'update word set review_count = review_count + 1 where words = "%s"' % word
                                                self.database.executesql(sql)
						sql = 'update word set mistake_count = mistake_count + 1 where words = "%s"' % word
						self.database.executesql(sql)
						return False
		else:
			print 'Data initialized failed!'
	def if_words_has_existed(self,word,meaning):
		if self.wordsarray:
			for item in self.wordsarray:
				#stupid match version 1.1
				if word == item[0] and self.match_func(meaning,item[1]):
					return 'yes'
				elif word == item[0] and not  self.match_func(meaning,item[1]):
					return 'word duplicate'
		return 'no'
	def workdone(self):
		if self.database:
			self.database.closedb()
	
	''' Compare the meaning of the word and the user input of one word'''
	def match_func(self,inputmeaning,meaning):
		#inputmeaning is the meaning from user so called input. Meaning is in the mysql 
		for item in func_words:
			index = inputmeaning.find(item)
			if index>-1:
				inputmeaning = inputmeaning[0:index]+ inputmeaning[index+1:]
		#If not doing as below it will occur an encode error
		if inputmeaning == None:
			inputmeaning = ""
		meaning = meaning.decode('utf-8','ignore').encode('utf-8')
		inputmeaning = inputmeaning.decode('utf-8','ignore').encode('utf-8')
		#print inputmeaning, meaning
		if meaning.find(inputmeaning)>-1:
			#stupid match version 1.1
			return True
		else:
			return False
			
							
if __name__ == '__main__':
        w = words()
	sql = 'select * from word'
        w.get_words_from_db(sql)
	word = raw_input('enter your input')
	meaning = raw_input('enter your meaning')
	if w.match_words(word,meaning):
		print 'matched'
	else:
		print 'not matched'
	data = []
	data.append(word)
	data.append(meaning)
	w.entering_words(data)
	w.workdone()
