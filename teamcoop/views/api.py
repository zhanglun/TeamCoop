#coding: utf-8
from flask import Blueprint, render_template
from __init__ import *

api = Blueprint('api', __name__)


@api.route('/team/project/', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        return api_response(200, 'success', 'add a new project')
    elif request.method == 'GET':
        return api_response(200, 'success', 'get all projects belongs to the team')


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


# 项目相关
@api.route('/user/project/', methods=['GET', 'POST'])
def user_project():
    if request.method == 'POST':
        # TODO: add project
        print request.json['projectname']
        item = Model.Project.query.filter_by(title=request.json['projectname']).first()
        if item is None:
            # TODO: insert
            return api_response(200, 'success', '新的项目')
        else:
            return api_response(200, 'failed', 'already exist')
    elif request.method == 'GET':
        # usrename = request.json['username']
        # TODO: return all projects of user
        # param: useridgit
        return api_response(200, 'success', 'GET method')
    else:
        # error
        return api_response(400, 'bad request', '参数错误')






