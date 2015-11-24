# -*- coding: UTF-8 -*-
from words import words
from flask import Flask
from flask.ext.wtf import Form
from flask.ext.bootstrap import Bootstrap
from wtforms import StringField, SubmitField,validators
from wtforms.validators import Required
from flask import render_template
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class validateForm(Form):
	words  = StringField('words')
        meaning = StringField('meaning?')
        submit = SubmitField('Submit')


