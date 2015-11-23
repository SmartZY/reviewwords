# -*- coding: UTF-8 -*-
#!/usr/bin/python
import os
import ConfigParser
cwd = os.path.dirname(os.path.abspath(__file__))
class function_words(object):
	def __init__(self):
		self.conf =  ConfigParser.ConfigParser()
		self.conf.read(os.path.join(cwd, 'function_words.conf'))
		self.func_words = self.conf.get('chinese_function_words','words')
	def get_func_words(self):
		if self.func_words:
			return self.func_words.split(',')
		else:
			return None
	
		

if __name__  == '__main__':
	f = function_words()
	print f.get_func_words()
