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


@api.route('/project/member/', methods=['GET', 'POST'])
def set_member():
    if request.method == 'POST':
        # get data from request.json
        username = request.json['username']
        # checkout if the user is already exist
        check = user.User.query.filter_by(username=username).first()
        if check is None:
            # create a new member
            new_member = user.User(username=username)
            db.session.add(new_member)
            db.session.commit()
            # set the response
            return api_response(200, 'success', 'add a new member')
        else:
            return api_response(200, 'success', 'the member is already exist')

    elif request.method == 'GET':
        return "Down!"

@api.route('/project/person/', methods=['GET', 'POST'])
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