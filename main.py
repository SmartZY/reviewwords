# -*- coding: UTF-8 -*-
from words import words
from flask import Flask,render_template, session, redirect, url_for, flash,request,jsonify
from flask.ext.bootstrap import Bootstrap
from forms.validateForm import validateForm
from werkzeug import secure_filename
import xlrd
import sys
import os
import random
reload(sys)
sys.setdefaultencoding('utf-8')
UPLOAD_FOLDER = 'uploadfile/enterwords'
ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','xls'])
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'zhaoyuan work'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

WORDS = words()
WORDS.get_words_from_db('select * from word')
for i in range(5):
	random.shuffle(WORDS.wordsarray)

class Handle(object):
	def __init__(self):
		self.begin = 0;
		self.end = 0;

handle = Handle()


@app.route('/')
def hello_world():
	return 'Hello world'


def dealwithcursor():
	if handle.begin + 8 > len(WORDS.wordsarray) and handle.begin != len(WORDS.wordsarray) - 1:
		handle.end = len(WORDS.wordsarray)
	else:
		if handle.begin == len(WORDS.wordsarray) - 1:
			handle.begin = 0
		handle.end = handle.begin + 8
	if handle.begin < len(WORDS.wordsarray) - 1:
		handle.begin = handle.begin + 1
	if handle.end < len(WORDS.wordsarray):
		handle.end = handle.end + 1
	
@app.route('/play',methods=['get','post'])
def play():
	form = validateForm()

	#初始化只在页面显示8个单词，第一个参数是WORDS列表的起始位置，第二个是终止位置
	#如果终止位置-起始位置==8说明还没到末尾，如果终止位置-起始位置>0 <8则还有，并且不够8个
	#如果 == 0 则重头开始，起始位置需要从表单那边获取，终止位置需要一步计算。
	#begin = request.args.get('begin', 0, type=int)
	dealwithcursor()
	return render_template('user.html',WORDS=WORDS,begin=handle.begin,end=handle.end)



@app.route('/playmore',methods=['get','post'])
def palymore():
	form = validateForm()
	handle.begin = request.args.get('begin', 0, type=int)
	if handle.begin + 8 > len(WORDS.wordsarray) and handle.begin != len(WORDS.wordsarray) - 1:
		handle.end = len(WORDS.wordsarray)
	else:
		if handle.begin == len(WORDS.wordsarray) - 1:
			handle.begin = 0
		handle.end = handle.begin + 8
	return jsonify(begin=handle.begin,end=handle.end)




@app.route('/test',methods=['get','post'])
def testFuck():
	word = request.args.get('word', '', type=str).split('=')
	meaning = request.args.get('meaning', 0, type=str).split('=')
	validateresult = []


	for i in range(len(word)):
		validateresult.append(WORDS.match_words(word[i],meaning[i]))
	#print 	validateresult
	return jsonify(result=validateresult)

'''根据返回的words查找它的正确含义并返回'''
@app.route('/playhint',methods=['get','post'])
def get_hint():
	word = request.args.get('word', "", type=str)
	if word != "":
		for item in WORDS.wordsarray:
			if word == item[0]:
				return jsonify(hint=item[1])
	return jsonify(hint="") 

@app.route('/enterwords',methods=['get','post'])
def enter_words():
	word = request.args.get('word', "", type=str)
	meaning = request.args.get('meaning', "", type=str)	
	data = []
	data.append(word)
	data.append(meaning)
	if word != "":
		WORDS.entering_words(data)
	return render_template('enterwords.html')




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload',methods=['get','post'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            data =  xlrd.open_workbook(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            table = data.sheets()[0]
            nrows = table.nrows
            for i in range(nrows):
            	item=[]

            	item.append(table.row_values(i)[0].encode('utf-8'))
            	item.append(table.row_values(i)[2].encode('utf-8'))
            	WORDS.entering_words(item)
    return render_template('user.html')

@app.route('/playfrommistake',methods=['get','post'])
def get_words_from_mistake():
	sql = "select * from word where mistake_count > 0"
	WORDS.wordsarray = []
	WORDS.get_words_from_db(sql)
	random.shuffle(WORDS.wordsarray)
	handle.begin = 0
	handle.end = 0
	dealwithcursor()
	return render_template('user.html',WORDS=WORDS,begin=handle.begin,end=handle.end)
	



@app.route('/playforall',methods=['get','post'])
def get_words_for_all():
	sql = "select * from word"
	WORDS.wordsarray = []
	WORDS.get_words_from_db(sql)
	random.shuffle(WORDS.wordsarray)
	handle.begin = 0
	handle.end = 0
	dealwithcursor()
	return render_template('user.html',WORDS=WORDS,begin=handle.begin,end=handle.end)
	


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
	

