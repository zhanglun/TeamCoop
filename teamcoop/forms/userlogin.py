#coding:utf-8

from __init__ import *

class LoginForm(Form):
    username = TextField(u'用户名', validators=[DataRequired(message='用户名不能为空')])
    password = PasswordField(u'密码', validators=[DataRequired(message='密码不能为空')])
    remember = BooleanField(False)
    submit = SubmitField(u'登录')
