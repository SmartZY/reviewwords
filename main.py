# -*- coding: UTF-8 -*-
from words import words
from flask import Flask,render_template, session, redirect, url_for, flash,request,jsonify
from flask.ext.bootstrap import Bootstrap
from forms.validateForm import validateForm
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'zhaoyuan work'


WORDS = words()
WORDS.get_words_from_db('select * from word')

class Handle(object):
	def __init__(self):
		self.begin = 0;
		self.end = 0;

handle = Handle()


@app.route('/')
def hello_world():
	return 'Hello world'

@app.route('/play',methods=['get','post'])
def test_validate():
	
	form = validateForm()
	if form.validate_on_submit():
		# The first one of the data This is only test
		words = form.words.data
		meaning = form.meaning.data
		if not WORDS.match_words(words,meaning):
			flash('哦吼，%s的意思没有输入对哦' % words)
		session['words'] = words
		session['meaning'] = meaning
		return redirect(url_for('test_validate'))
	form.words.data = session.get('words')
	form.meaning.data = session.get('meaning')
	#以上都是legacy代码，没jb啥用，下面是初步构思
	#初始化只在页面显示8个单词，第一个参数是WORDS列表的起始位置，第二个是终止位置
	#如果终止位置-起始位置==8说明还没到末尾，如果终止位置-起始位置>0 <8则还有，并且不够8个
	#如果 == 0 则重头开始，起始位置需要从表单那边获取，终止位置需要一步计算。
	#begin = request.args.get('begin', 0, type=int)
	if handle.begin + 8 > len(WORDS.wordsarray) and handle.begin != len(WORDS.wordsarray) - 1:
		handle.end = len(WORDS.wordsarray)
	else:
		if handle.begin == len(WORDS.wordsarray) - 1:
			handle.begin = 0
		handle.end = handle.begin + 8
	return render_template('user.html',form=form,WORDS=WORDS,begin=handle.begin,end=handle.end)



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
	print handle.begin,handle.end
	return jsonify(begin=handle.begin,end=handle.end)




@app.route('/test',methods=['get','post'])
def testFuck():
	word = request.args.get('word', 0, type=str)
	meaning = request.args.get('meaning', 0, type=str)
	return jsonify(result=word + meaning)




if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
	

