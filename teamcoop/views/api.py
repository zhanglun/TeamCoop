#coding: utf-8
from flask import Blueprint, render_template
from __init__ import *

api = Blueprint('api', __name__)

print api_response_dict

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
            api_response_dict['code'] = 'success'
            api_response_dict['result'] = 'add a new member'
            response = make_response(jsonify(api_response_dict))
            response.status = '200'
        else:
            response = make_response('already exist')
            response.status = '200'
        return response

    elif request.method == 'GET':
        return "Down!"

@api.route('/project/person/', methods=['GET', 'POST'])
def set_person():
    if request.method == 'POST':
        name = request.json['name']
        username = request.json['username']
        password = request.json['password']
        confirm_password = request.json['confirm_password']

    elif request.method == 'GET':
        return 'API-setting person'