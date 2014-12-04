#coding: utf-8
from flask import Blueprint, render_template
from __init__ import *

# temp
import random
import datetime

api = Blueprint('api', __name__)


# Team成员
@api.route('/team/member/', methods=['GET', 'POST'])
def team_member():
    if request.method == 'POST':
        # get data from request.json
        # TODO:
        # project_id
        # checkout if the user is already exist
        username = request.json['username']
        print request.json
        if username is None:
            # return api_response(400, 'fail', '参数错误')
            return 'asdf'
        check = Model.User.query.filter_by(username=username).first()
        if check is None:
            # create a new member
            new_member = Model.User(username=username)
            db.session.add(new_member)
            db.session.commit()
            # set the response
            return api_response(200, 'success', 'add a new member')
        else:
            return api_response(200, 'success', 'the member is already exist')

    elif request.method == 'GET':
        return "Down!"


# 项目成员
@api.route('/project/member/', methods=['GET', 'POST'])
def project_member():
    if request.method == 'POST':
        project_id = ''
        username = ''
        # TODO: insert
        return api_response(200, 'success', 'project member')
    elif request.method == 'GET':
        return api_response(200, 'success', 'project member')



# 设置个人信息
@api.route('/project/setting/person/', methods=['GET', 'POST'])
def set_person():
    if request.method == 'POST':
        name = request.json['name']
        username = request.json['username']
        password = request.json['password']
        confirm_password = request.json['confirm_password']

        if confirm_password != password:
            return api_response(400, 'bad request', '参数错误')

        person = user.User.query.filter_by(name=name).first()
        if person is not None:
            person.username = username
            person.password = password
            api_response(200, 'success', 'test')

    elif request.method == 'GET':
        return api_response('200', 'success', 'test')


# 用户有关的项目
@api.route('/user/project/', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        # title = request.json['title']
        # user_id = request.json['user_id']
        # description = request.json['description']
        # level = request.json['level']
        # deadline = request.json['deadline']
        # is_public = request.json['is_public']
        title = u'项目编号-' + str(random.randint(0, 10)) + ' : ' + str(datetime.datetime.utcnow())
        description = u'项目描述： ' + u'这个是项目描述啊' * random.randint(1, 10) + 'ABC' * random.randint(0, 20)
        level = 1
        deadline = datetime.datetime.utcnow()
        status = 1
        is_public = 1
        # user_id = 2
        user_id = random.randint(1, 5)

        project_item = Model.Project.query.filter_by(title=title).first()

        if project_item is None:
            project_new = Model.Project(title=title, description=description, level=level, deadline=deadline, status=status, isPublic=is_public, createuserid=user_id)
            db.session.add(project_new)
            db.session.commit()
            return api_response(200, 'success', 'add a new project: ' + title)
        else:
            return 'already exist!'
    elif request.method == 'GET':
        # TODO: return all projects of user
        # param: userid
        return api_response(200, 'success', 'get all projects belongs to the team')
    else:
        # error
        return api_response(400, 'bad request', '参数错误')





