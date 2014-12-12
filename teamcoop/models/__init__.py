# coding: utf-8
import time
import datetime
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

importance_list = ['', u'一般', u'重要', u'非常重要']