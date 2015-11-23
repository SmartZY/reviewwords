# -*- coding: UTF-8 -*-
from words import words
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello world'

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
	
'''	w = words()
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
        w.workdone()'''

