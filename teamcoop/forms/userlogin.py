#coding:utf-8

from __init__ import *

class LoginForm(Form):
    username = TextField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    submit = SubmitField(u'登录')
