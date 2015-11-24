# -*- coding: UTF-8 -*-
from words import words
from flask import Flask,render_template, session, redirect, url_for, flash
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
	return render_template('user.html',form=form,WORDS=WORDS)


if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)
	

