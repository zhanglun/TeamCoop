from __init__ import *
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # id = db.relationship('UserProject', primaryjoin='user.id')
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, default='123456')
    name = db.Column(db.Text, default='')
    gender = db.Column(db.Text, default='')
    email = db.Column(db.Text, default='')
    createtime = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


class UserDepartMent(db.Model):
    __tablename__ = 'user_department'
    id = db.Column(db.Integer, primary_key=True)
    departmentId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<UserDepartMent %r %r>' & self.userId % self.departmentId


class UserProject(db.Model):
    __tablename__ = 'user_project'
    id = db.Column(db.Integer, primary_key=True)
    projectId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    # projectId = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    # userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False, default=2)

    def __repr__(self):
        return '<UserProject %r %r>' % self.userId % self.projectId


#project
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    # id = db.relationship('UserProject')
    title = db.Column(db.Text, unique=True)
    description = db.Column(db.Text, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    deadline = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    status = db.Column(db.Integer, nullable=False, default=1)
    isPublic = db.Column(db.Integer, nullable=False, default=1)
    createuserid = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Project %r>' % self.title






