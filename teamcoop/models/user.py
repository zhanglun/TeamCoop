from __init__ import *

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    name = db.Column(db.Text, default='')
    gender = db.Column(db.Text, default='')
    phone = db.Column(db.Text, default='')
    email = db.Column(db.Text, default='')
    createtime = db.Column(db.DateTime, default=time.time()),

    def __repr__(self):
        return '<User %r>' % self.username


class UserDepartMent(db.Model):
    __tablename__ = 'user_department'
    departmentId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<UserDepartMent %r %r>' & self.userId %self.departmentId


class UserProject(db.Model):
    __tablename__ = 'user_project'
    projectId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=2)

    def __repr__(self):
        return '<UserProject %r %r>' % self.userId % self.projectId
