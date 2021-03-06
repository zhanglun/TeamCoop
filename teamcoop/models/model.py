from __init__ import *
from werkzeug.security import generate_password_hash, check_password_hash

class UserDepartMent(db.Model):
    __tablename__ = 'user_department'
    id = db.Column(db.Integer, primary_key=True)
    # departmentId = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    # userId = db.Column(db.Text, db.ForeignKey('user.id'), nullable=False)
    departmentId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Text, nullable=False)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def get_time(self):
        return self.createtime

    def __repr__(self):
        return '<UserDepartMent userid: %d departmentid: %d>' % (self.userId, self.departmentId)

class UserProject(db.Model):
    __tablename__ = 'user_project'
    id = db.Column(db.Integer, primary_key=True)
    # projectId = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    # userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    projectId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=2)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def get_json(self):
        return {'id': self.id, 'project_id': self.projectId, 'user_id': self.userId, 'level': self.level}

    def get_time(self):
        return self.createtime

    def __repr__(self):
        return '<UserProject user_id:%r project_id:%r>' % (self.userId, self.projectId)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text, default='123456')
    level = db.Column(db.Integer, default=2)
    name = db.Column(db.Text, default='')
    gender = db.Column(db.Text, default='')
    email = db.Column(db.Text, default='')
    createtime = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    # department = db.relationship('UserDepartMent', backref='department', lazy='dynamic')

    def get_time(self):
        return self.createtime

    def get_json(self):
        return {'id': self.id, 'username': self.username, 'level': self.level, 'name': self.name, 'gender': self.gender,
                'email': self.email, 'create_time': self.createtime}

    def __repr__(self):
        return '<User %r>' % self.username


# project
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    description = db.Column(db.Text, nullable=False)
    level = db.Column(db.Integer, nullable=False, default=1)
    deadline = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    status = db.Column(db.Integer, nullable=False, default=1)
    isPublic = db.Column(db.Integer, nullable=False, default=1)
    createuserid = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def get_time(self):
        return self.createtime

    def get_json(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'level': self.level, 'importance': importance_list[self.level], 'deadline': self.deadline, 'status': self.status, 'isPublic': self.isPublic, 'createuserid': self.createuserid, 'createtime': self.createtime}

    def __repr__(self):
        return '<Project title: %r id: %r>' % (self.title, self.id)


# department

class DepartMent(db.Model):
    __tablename__ = 'department'
    id = db.Column(db.Integer, primary_key=True)
    depName = db.Column(db.Text, nullable=False, default='')
    parentId = db.Column(db.Integer, nullable=False, default=0)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    # userid = db.relationship('UserDepartMent', backref='members', lazy='dynamic')

    def get_json(self):
        return {'id': self.id, 'department_name': self.depName, 'parent_id': self.parentId}

    def get_time(self):
        return self.createtime

    def __repr__(self):
        return '<Department %r>' % self.depName


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False, default='')
    deadline = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    executeUserId = db.Column(db.Integer, nullable=False, default=0)
    createUserId = db.Column(db.Integer, nullable=False, default=0)
    projectId = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.Integer, nullable=False, default=1)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def get_time(self):
        return self.createtime

    def get_json(self):
        return {'id': self.id, 'title': self.title, 'description': self.description, 'deadline': self.deadline, 'execute_user_id': self.executeUserId, 'create_user_id': self.createUserId, 'status': self.status, 'create_time': self.createtime}

    def __repr__(self):
        return '<Task %r>' % self.title


class TaskComment(db.Model):
    __tablename__ = 'task_comment'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    content = db.Column(db.Text, nullable=False, default='')
    taskId = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def get_time(self):
        return self.createtime

    def get_json(self):
        return {'id': self.id, 'content': self.content, 'task_id': self.taskId, 'user_id': self.userId,
                'create_time': self.createtime}

    def __repr__(self):
        return '<TaskComment %r>' % self.content

class ProjectComment(db.Model):
    __tablename__ = 'project_comment'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    content = db.Column(db.Text, nullable=False, default='')
    projectId = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    createtime = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())

    def get_json(self):
        return {'id': self.id, 'content': self.content, 'project_id': self.projectId, 'user_id': self.userId,
                'create_time': self.createtime}

    def __repr__(self):
        return '<ProjectComment %r>' % self.content

