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
        # print request.json
        # username = 'admin'
        if username is None:
            return api_response(400, 'fail', '参数错误')
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
        # 返回所有部门和各成员

        # depart = Model.DepartMent.query.all()
        depart = Model.UserDepartMent.query.order_by(Model.UserDepartMent.departmentId).all()

        # for x in depart:
        #     depart_user =

        u = Model.User.query.all()
        for x in u:
            index = u.index(x)
            department = Model.UserDepartMent.query.filter_by(userId=x.id).first()
            if department is not None:
                x = x.get_json()
                x['department_id'] = department.departmentId
            else:
                x = x.get_json()
                x['department_id'] = 0
            u[index] = x

        return api_response(200, 'success', 'all team members', u)



@api.route('/team/department/', methods=['GET', 'POST'])
def team_department():
    if request.method == 'POST':
        depart_name = request.json['department_name']
        members = request.json['members']
        depart = Model.DepartMent.query.filter_by(depName=depart_name).first()
        if depart is None:
            new_department = Model.DepartMent(depName=depart_name)
            db.session.add(new_department)
            db.session.commit()
            for x in members:
                u = Model.User.query.filter_by(username=x).first()
                if x is not None:
                    new_user = Model.User(username=x)
                    db.session.add(new_user)
                    db.session.commit()
                    user_depart = Model.UserDepartMent(departmentId=new_department.id, userId=new_user.id)
                    db.session.add(user_depart)
                else:
                    user_depart = Model.UserDepartMent(departmentId=new_department.id, userId=u.id)
                    db.session.add(user_depart)
            db.session.commit()
            return '新增部门和成员'
        else:
            return api_response(400, 'fail', 'department is already exist')
    elif request.method == 'GET':
        depart = Model.DepartMent.query.all()
        for x in depart:
            index = depart.index(x)
            depart[index] = x.get_json()
            # print x.get_json()
        return api_response(200, 'success', 'get team all department', depart)
    else:
        return 'method Error！'


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
        title = request.json['title']
        description = request.json['description']
        level = request.json.get('level')
        print level
        deadline = request.json.get('deadline')
        is_public = request.json.get('is_public')
        status = 1
        creater_id = request.json.get('creater_id')
        person_in_charge = request.json.get('person_in_charge')
        members = request.json.get('members')


        item = Model.Project.query.filter_by(title=title).first()

        if item is None:
            # add new project to database
            project_new = Model.Project(title=title, description=description, level=level, deadline=deadline, status=status, isPublic=is_public, createuserid=creater_id)
            db.session.add(project_new)
            db.session.commit()

            # add new row to user_project
            project_new_id = Model.Project.query.filter_by(title=title).first().id
            if person_in_charge is not None:
                for x in person_in_charge:
                    charger = Model.UserProject(projectId=project_new_id, userId=x, level=1)
                    db.session.add(charger)
            if members is not None:
                for x in members:
                    member = Model.UserProject(projectId=project_new_id, userId=x, level=2)
                    db.session.add(member)

            db.session.commit()
            return api_response(200, 'success', 'add a new project: ' + title)
        else:
            return 'already exist!'
    elif request.method == 'GET':
        # param: userid
        userid = request.json['user_id']
        # userid = 2
        if userid is not None:
            projects = Model.UserProject.query.filter_by(userId=userid).order_by(Model.UserProject.projectId).all()
            # response_data={}
            for x in projects:
                index = projects.index(x)
                projects[index] = projects[index].get_json()

            return api_response(200, 'success', 'get all projects belongs to the team', projects )
        else:
            # error
            return api_response(400, 'bad request', '参数错误')
    else:
        return api_response(400, 'bad request', '参数错误')


@api.route('/department/member/', methods=['GET', 'POST'])
def depart_member():
    if request.method == 'POST':
        # depart = request.json['department_id']
        # username = request.json['username']
        # aa = request.json['username']

        department_id = 1
        department_name = u'开发部'
        username = 'zhanglun' + str(datetime.datetime.utcnow())

        d = Model.DepartMent.query.filter_by(depName=department_name).first()

        if d is not None:
            return api_response(200, 'fail', 'already exist')

        u = Model.User.query.filter_by(username=username).first()

        if u is not None:
            return api_response(200, 'fail', 'already exist')
        else:
            user_new = Model.User(username=username)
            db.session.add(user_new)
            db.session.commit()
            print '===='
            user_id = user_new.id
            new = Model.UserDepartMent(userId=user_id, departmentId=department_id)
            db.session.add(new)
            db.session.commit()
        return '新增成员'
    elif request.method == 'GET':
        department_id = request.json['department_id']
        # department_id = 2
        members = Model.UserDepartMent.query.filter_by(departmentId=department_id).order_by(
            Model.UserDepartMent.userId).all()
        for x in members:
            index = members.index(x)
            members[index] = x.userId

        return api_response(200, 'success', 'department\'s member', members)
    else:
        return 'Method Error!'