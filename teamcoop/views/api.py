from flask import Blueprint, render_template

from __init__ import *

api = Blueprint('api', __name__)

@api.route('/add/member/')
def add_member():
    pass

@api.route('/add/user/')
def add_user():
    print "TeamCoop add_user API"
    # db.create_all()
    u = user.User(username='zhanglun', password='213', name='zhangxiaolun', gender='man', phone='18270919495', email='zhanglun1410@gmail.com')
    db.session.add(u)
    db.session.commit()
    return 'add user!'
