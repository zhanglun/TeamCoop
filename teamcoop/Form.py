#coding:utf-8

from flask_wtf import Form
from wtforms import *
from wtforms.validators import *

class LoginForm(Form):
    username = TextField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'登录')
