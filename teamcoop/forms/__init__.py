# coding: utf-8
# 在使用 import * 导入包时，会将 __init__.py 中的 __all__ 变量全部导入，如果没有定义 __all__变量，就会报错

from flask_wtf import Form
from wtforms import TextField, BooleanField, PasswordField, SubmitField, TextAreaField, validators
from wtforms.validators import *