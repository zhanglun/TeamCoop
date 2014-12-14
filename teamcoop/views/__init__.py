# coding: utf8
# 在 views 的 __init__.py 中导入forms和models

import json
import dateutil.parser
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response, g
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter

from teamcoop.forms import userlogin
from teamcoop.models import db
from teamcoop.models import model as Model


def api_response(status, code, message, result=None):
    response_dict = {'code': code, 'message': message, 'result': result}
    response = make_response(jsonify(response_dict))
    response.status = str(status)
    return response

panel = {'issues': 'issues', 'setting': 'setting', 'dashboard': 'dashboard'}

def get_related_issues(userid):
    current_user = Model.User.query.filter_by(id=userid).first()
    if current_user.level ==1:
        is_admin = True
        print u'管理员'
    else:
        is_admin = False
        print u'普通用户'

    issues = []

    if is_admin == True:
        u = Model.User.query.filter(Model.User.level != 1).all()
        for x in u:
            if x.id != userid:
                print 'id'
                print x.id
                u_d = Model.UserDepartMent.query.filter_by(userId=x.id).first()
                print 'u_d'
                print u_d
                d = Model.DepartMent.query.filter_by(id=u_d.departmentId).first()
                issues.append({'flag': 'add new user', 'person_in_charge': u'你', 'new_user': x.username, 'department':
                    d.depName, 'create_time': x.createtime})
        # 管理员添加部门
        depart = Model.DepartMent.query.all()
        for x in depart:
            issues.append({'flag': 'add new department', 'person_in_charge': u'你', 'department': x.depName,
                           'create_time': x.createtime})
    else:
        # 管理员添加你
        u = Model.User.query.filter_by(id=userid).first()
        u_d = Model.UserDepartMent.query.filter_by(userId=u.id).first()
        d= Model.DepartMent.query.filter_by(id=u_d.departmentId).first()
        issues.append({'flag': 'add new user', 'person_in_charge': u'管理员', 'new_user': u'你', 'department': d.depName, 'create_time': u_d.createtime})

        # 用户添加项目
        project = Model.Project.query.filter(Model.Project.createuserid == userid).all()
        for x in project:
            # u = Model.User.query.filter_by(id=x.createuserid).first()
            issues.append({'flag': 'add new project', 'person_in_charge': u.username, 'project_title': x.title,
                           'create_time': x.createtime})
        # 用户加入到项目中
        u_project = Model.UserProject.query.filter(Model.UserProject.userId == userid).all()
        for x in u_project:
            # u = Model.User.query.filter_by(id=x.userId).all()
            p = Model.Project.query.filter_by(id=x.projectId).first()
            # for y in u:
            issues.append({'flag': 'add member to project', 'project_title': p.title, 'new_member': u'你',
                               'create_time': x.createtime})
        # 用户添加任务或者执行
        task = Model.Task.query.filter(Model.Task.createUserId == userid or Model.Task.executeUserId == userid).all()
        for t in task:
            project = Model.Project.query.filter_by(id=t.projectId).first()
            creater = Model.User.query.filter_by(id=t.createUserId).first()
            executer = Model.User.query.filter_by(id=t.executeUserId).first()
            if creater.id == userid:
                issues.append({'flag': 'deploy new task', 'deployer': u'你', 'executer': executer.username, 'task_title': t.title, 'project_title': project.title, 'create_time': t.createtime})
            elif executer.id == userid:
                issues.append({'flag': 'deploy new task', 'deployer': creater.username, 'executer': u'你', 'task_title': t.title, 'project_title': project.title, 'create_time': t.createtime})

        # 用户添加任务评论
        t_comment = Model.TaskComment.query.filter(Model.TaskComment.userId == userid).all()

        for x in t_comment:
            task = Model.Task.query.filter_by(id=x.taskId).first()
            user = Model.User.query.filter_by(id=x.userId).first()
            issues.append({'flag': 'task comment', 'task_title': task.title, 'publisher': u'你', 'create_time': x.createtime})

    issues.sort(key=lambda x: x['create_time'])
    return issues


def get_other_issues(userid):
    current_user = Model.User.query.filter_by(id=userid).first()
    if current_user.level ==1:
        is_admin = True
        print u'管理员'
    else:
        is_admin = False
        print u'普通用户'
    issues = []
    # 管理员添加用户
    # u = Model.User.query.all()
    if is_admin == False:
        
        u = Model.User.query.filter(Model.User.level != 1).all()
        for x in u:
            if x.id != userid:
                print 'id'
                print x.id
                u_d = Model.UserDepartMent.query.filter_by(userId=x.id).first()
                print 'u_d'
                print u_d
                d = Model.DepartMent.query.filter_by(id=u_d.departmentId).first()
                issues.append({'flag': 'add new user', 'person_in_charge': u'管理员', 'new_user': x.username, 'department':
                    d.depName, 'create_time': x.createtime})
        # 管理员添加部门
        depart = Model.DepartMent.query.all()
        for x in depart:
            issues.append({'flag': 'add new department', 'person_in_charge': u'管理员', 'department': x.depName,
                           'create_time': x.createtime})
    # 用户添加项目
    project = Model.Project.query.filter(Model.Project.createuserid != userid).all()
    for x in project:
        u = Model.User.query.filter_by(id=x.createuserid).first()
        issues.append({'flag': 'add new project', 'person_in_charge': u.username, 'project_title': x.title,
                       'create_time': x.createtime})
    # 用户加入到项目中
    u_project = Model.UserProject.query.filter(Model.UserProject.userId != userid).all()
    for x in u_project:
        u = Model.User.query.filter_by(id=x.userId).all()
        p = Model.Project.query.filter_by(id=x.projectId).first()
        for y in u:
            issues.append({'flag': 'add member to project', 'project_title': p.title, 'new_member': y.username,
                           'create_time': x.createtime})
    # 用户添加任务或者执行
    task = Model.Task.query.filter(Model.Task.createUserId != userid or Model.Task.executeUserId != userid).all()
    for t in task:
        project = Model.Project.query.filter_by(id=t.projectId).first()
        creater = Model.User.query.filter_by(id=t.createUserId).first()
        executer = Model.User.query.filter_by(id=t.executeUserId).first()
        issues.append({'flag': 'deploy new task', 'deployer': creater.username, 'executer': executer.username, 'task_title': t.title, 'project_title': project.title, 'create_time': t.createtime})

    # 用户添加任务评论
    t_comment = Model.TaskComment.query.filter(Model.TaskComment.userId != userid).all()

    for x in t_comment:
        task = Model.Task.query.filter_by(id=x.taskId).first()
        user = Model.User.query.filter_by(id=x.userId).first()
        issues.append({'flag': 'task comment', 'task_title': task.title, 'publisher': user.username, 'create_time': x.createtime})

    issues.sort(key=lambda x: x['create_time'])
    return issues

def project_issues(project_id):
    issues = []
    p = Model.Project.query.filter_by(id=project_id).first()
    # user
    u_p = Model.UserProject.query.filter(Model.UserProject.projectId == project_id).order_by(
        Model.UserProject.createtime).all()

    if u_p is not None:
        for x in u_p:
            u = Model.User.query.filter_by(id=x.userId).first()
            if x.level == 1:
                issues.append({'flag': 'add new project', 'person_in_charge': u.name, 'project_title': p.title, 'create_time': x.createtime})
            elif x.level == 2:
                issues.append({'flag': 'join new project', 'participant': u.name, 'project_title': p.title,
                               'create_time': x.createtime})

    # Task
    t = Model.Task.query.filter_by(projectId=project_id).order_by(Model.Task.createtime).all()

    if t is not None:
        for x in t:
            execute_u = Model.User.query.filter_by(id=x.executeUserId).first()
            create_u = Model.User.query.filter_by(id=x.createUserId).first()
            issues.append({'flag': 'deploy new task', 'deployer': create_u.get_json()['name'], 'executer': execute_u.get_json()['name'], 'task_title': x.title, 'create_time': x.createtime})

            # task_comment
            t_c = Model.TaskComment.query.filter_by(id=x.id).all()
            for y in t_c:
                publisher = Model.User.query.filter_by(id=y.id).first()
                print '------'
                print x.title
                issues.append({'flag': 'add task comment', 'publisher': publisher.name, 'task_title': x.title,
                               'comment': y.content,
                               'create_time': y.createtime})

    # project_comment
    p_c = Model.ProjectComment.query.filter_by(projectId=project_id).order_by(Model.ProjectComment.createtime).all()

    if p_c is not None:
        for c in p_c:
            u = Model.User.query.filter_by(id=c.userId).first()
            issues.append({'flag': 'add project comment', 'publisher': u.name, 'comment': c.content, 'create_time':
                c.createtime})

    issues.sort(key=lambda x: x['create_time'])
    return issues