#coding: utf-8
from flask import Blueprint, render_template
from __init__ import *

# temp
import random
import datetime

api = Blueprint('api', __name__)


# ====Team=========================== #
# =================================== #
# Team成员
@api.route('/team/member/', methods=['GET', 'POST'])
def team_member():
    if request.method == 'POST':

        username = request.json['username']
        # print request.json
        # username = 'admin'
        if username is None:
            return api_response(400, 'fail', '参数错误')
        check = Model.User.query.filter_by(username=username).first()
        if check is None:
            new_member = Model.User(username=username)
            db.session.add(new_member)
            db.session.commit()
            return api_response(200, 'success', 'add a new member')
        else:
            return api_response(200, 'success', 'the member is already exist')

    elif request.method == 'GET':
        # 返回所有部门和各成员
        depart = Model.DepartMent.query.all()
        result = []
        if depart is None:
            return api_response(200, 'success', 'no department')
        else:
            for x in depart:
                depart_id = x.id
                members = Model.UserDepartMent.query.filter_by(departmentId=depart_id).all()
                if members is not None:
                    m_list = []
                    for m in members:
                        u = Model.User.query.filter_by(id=m.userId).first()
                        m_list.append(u.get_json())

                    result.append({'department_id': depart_id, 'members': m_list})

            return api_response(200, 'success', 'no department', result)


# Team 添加部门，获取所有部门
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
                u = Model.User.query.filter_by(name=x).first()
                if x is not None:
                    new_user = Model.User(name=x, username=x)
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
            depart_id = x.id
            counts = Model.UserDepartMent.query.filter_by(departmentId=depart_id).count()
            x = x.get_json()
            x['counts'] = counts
            depart[index] = x
        return api_response(200, 'success', 'get team all department', depart)


#Team 删除部门
@api.route('/team/department/trash/', methods=['POST'])
def drop_department():
    if request.method == 'POST':
        depart_id = request.json.get('department_id')
        for x in depart_id:
            p = Model.DepartMent.query.filter(Model.DepartMent.id == x)
            p.delete()
        db.session.commit()
        return api_response(200, 'success', 'delete department')
    else:
        return '405'


# ====Project======================== #
# =================================== #

# Project-状态
@api.route('/project/detail/status/', methods=['GET', 'POST'])
def project_status():
    if request.method == 'POST':
        project_id = request.json['project_id']
        status = request.json['project_status']
        p = Model.Project.query.filter_by(id=project_id).first_or_404()
        p.status = status
        db.session.commit()
        return 'success'
    elif reuqest.method == 'GET':
        project_id = request.json['project_id']
        p = Model.Project.query.filter_by(id=project_id).first_or_404()
        return api_response(200, 'success', 'project status', {'status': p.status})

# Project-成员
@api.route('/project/member/', methods=['GET', 'POST'])
def project_member():
    if request.method == 'POST':
        project_id = request.json['project_id']
        members = request.json['members']
        p = Model.Project.query.filter_by(id=project_id).first_or_404()

        for m in members:
            user_p = Model.UserProject.query.filter(Model.UserProject.userId == m).first()
            u = Model.User.query.filter_by(id=m).first()
            if user_p is None and u is not None:
                new_user_p = Model.UserProject(projectId=project_id, userId=m)
                db.session.add(new_user_p)
        db.session.commit()

        return api_response(200, 'success', 'project member')

    elif request.method == 'GET':

        project_id = reuqest.args.get('project_id')
        u = Model.UserProject.query.filter_by(projectiId=project_id).all()

        return api_response(200, 'success', 'project member')

#Project comment
@api.route('/project/comment/', methods=['GET', 'POST'])
def project_comment():
    if request.method == 'POST':
        project_id = request.json['project_id']
        content = request.json['content']
        user_id = request.json['user_id']

        new_content = Model.ProjectComment(content=content, projectId=project_id, userId=user_id)
        db.session.add(new_content)
        db.session.commit()

    elif request.method == 'GET':

        project_id = request.args.get('project_id')
        c = Model.ProjectComment.query.filter_by(projectId=project_id).order_by(Model.ProjectComment.createtime).all()

        for x in c:
            index = c.index(x)
            u = Model.User.query.filter_by(id=x.userId).first()
            x = x.get_json()
            x['user'] = u.get_json()
            c[index] = x
        return api_response(200, 'success', u'项目中所有的评论', {'comments': c})

#Task
# 添加任务和获取任务
@api.route('/project/task/', methods=['GET', 'POST'])
def project_task():
    if request.method == 'POST':
        title = request.json.get('title')
        description = request.json.get('description')
        deadline = request.json.get('deadline')
        project_id = request.json['project_id']
        execute_user_id = request.json.get('execute_user_id')
        create_user_id = request.json.get('create_user_id')
        status = 1
        createtime = request.json.get('create_time')

        t = Model.Task.query.filter(Model.Task.title == title and Model.Task.projectId == project_id).first()
        if t is not None:
            return api_response(200, 'failed', u'在这个项目中，任务名不能重复')

        new_t = Model.Task(title=title, description=description, executeUserId=execute_user_id, deadline=deadline,
                           createUserId=create_user_id, createtime=createtime, status=status)
        db.session.add(new_t)
        db.session.commit()
        return api_response(200, 'success', u'添加成功')
    elif request.method == 'GET':
        project_id = request.args.get('project_id')
        p = Model.Task.query.filter_by(id=project_id).all()
        task_list = []
        #
        for x in p:
            task_list.append(x.get_json())

        return api_response(400, 'success', 'test', {'tasks': task_list})


@api.route('/project/task/trash/', methods=['GET', 'POST'])
def drop_task():
    if request.method == 'POST':
        project_id = request.json['project_id']
        task_id = request.json['task_id']
        Model.Task.query.filter_by(id=task_id, projectId=project_id).delete()

        db.session.commit()
        return api_response(200, 'success', u'删除成功')
        # if t is None:
        #     return api_response(200, 'failed', u'找不到id对应的任务')
        # else:
        #     # db.session.delete()
        #     db.session.commit()
        #     return api_response(200, 'success', u'删除成功')


# 用户相关的（部署和创建任务）
@api.route('/user/project/task/', methods=['GET', 'POST'])
def user_task():
    if request.method == 'POST':
        user_id = request.json['user_id']
        pass
    elif request.method == 'GET':
        user_id = request.args.get('user_id')
        project_id = request.args.get('project_id')
        # user部署的task
        task_c = Model.Task.query.filter(Model.Task.projectId == project_id and Model.Task.createUserId == user_id).order_by(Model.Task.title).all()
        # user执行的task
        task_e = Model.Task.query.filter(Model.Task.projectId == project_id and Model.Task.executeUserId ==
                                         user_id).order_by(Model.Task.title).all()
        if task_c is not None:
            for c in task_c:
                index = task_c.index(c)
                c = c.get_json()
                c['creater_name'] = Model.User.query.filter_by(id=c['create_user_id']).first().name
                c['execute_name'] = Model.User.query.filter_by(id=c['execute_user_id']).first().name
                task_c[index] = c
        if task_e is not None:
            for e in task_e:
                index = task_e.index(e)
                e = e.get_json()
                e['creater_name'] = Model.User.query.filter_by(id=c['create_user_id']).first().name
                e['execute_name'] = Model.User.query.filter_by(id=c['execute_user_id']).first().name
                task_e[index] = e

        return api_response(200, 'success', 'all data', {'tasks': {'create': task_c, 'execute': task_e}})

# 任务的详情
@api.route('/project/task/detail/')
def task_detail():
    project_id = request.args.get('project_id')
    task_id = request.args.get('task_id')
    task = Model.Task.query.filter_by(id=task_id, projectId=project_id).first()
    t = task.get_json()
    t['create_name'] = Model.User.query.filter_by(id=task.createUserId).first().username
    t['execute_name'] = Model.User.query.filter_by(id=task.executeUserId).first().username
    if task is None:
        return api_response(200, 'failed', 'wrong task id')
    else:
        return api_response(200, 'success', 'get task detail', {'detail': t})


# 任务的讨论
@api.route('/project/task/comment/', methods=['GET', 'POST'])
def task_comment():
    if request.method == 'POST':
        task_id = request.json['task_id']
        user_id = request.json['user_id']
        content = request.json['content']
        c = Model.TaskComment(taskId=taskId, userId=user_id, content=content)
    elif request.method == 'GET':
        return '222'






# ====User=========================== #
# =================================== #

# User-设置个人信息
@api.route('/personal/setting/', methods=['GET', 'POST'])
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
            api_response(200, 'success', 'Down!')

    elif request.method == 'GET':
        return api_response('200', 'success', 'test')

# User-项目
@api.route('/user/project/', methods=['GET', 'POST'])
def project():
    if request.method == 'POST':
        title = request.json['title']
        description = request.json['description']
        level = request.json.get('level')
        deadline = request.json.get('deadline')
        if deadline:
            deadline = dateutil.parser.parse(deadline)
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
        userid = request.json['user_id']
        if userid is not None:
            projects = Model.UserProject.query.filter_by(userId=userid).order_by(Model.UserProject.projectId).all()
            # response_data={}
            for x in projects:
                index = projects.index(x)
                projects[index] = projects[index].get_json()

            return api_response(200, 'success', 'get all projects belongs to the team', projects)
        else:
            # error
            return api_response(400, 'bad request', '参数错误')
    else:
        return api_response(400, 'bad request', '参数错误')































# ====DepartMent===================== #
# =================================== #

# DepartMent-管理成员
@api.route('/department/detail/member/', methods=['GET', 'POST', 'DELETE'])
def department_member():
    if request.method == 'POST':
        depart_id = request.json['department_id']
        members = request.json.get('members')
        if depart_id is None:
            return api_response(200, 'success', u'没有部门id，TM怎么添加！')
        if members is None:
            return api_response(200, 'success', u'没有新成员你发送个蛋请求！')
        if len(members) == 0:
            return api_response(200, 'success', u'没有新成员你发送个蛋请求！')

        check_list = []
        for x in members:
            u = Model.User.query.filter_by(username=x).first()
            if u is None:
                u = Model.User(username=x)
                db.session.add(u)
                db.session.commit()
                user_depart = Model.UserDepartMent(userId=u.id, departmentId=depart_id)
                db.session.add(user_depart)
                db.session.commit()
                check_list.append(True)
            else:
                check_list.append(False)
        return api_response(200, 'success', u'操作结束', check_list)

    elif request.method == 'GET':
        # 获取所有成员
        depart_id = request.json['depart_id']
        user_depart = Model.UserDepartMent.query.filter_by(departmentId=depart_id).order_by(
            Model.UserDepartMent.userId).all()
        m_list = []
        for x in user_depart:
            u = Model.User.query.filter_by(id=x.userId).first()
            m_list.append(u.get_json())
        return api_response(200, 'success', 'all members of the department', m_list)

# DepartMent-删除成员
@api.route('/department/detail/member/trash/', methods=['GET', 'POST'])
def drop_member():
    if request.method == 'POST':
        depart_id = request.json['department_id']
        members = request.json.get('members')
        Model.UserDepartMent.query.filter(Model.UserDepartMent.departmentId == depart_id and Model.UserDepartMent.userId.in_(members)).delete()
        db.session.commit()
        return api_response(200, 'success', 'delete member')

    elif request.method == 'GET':

        return 'hello'

    else:
        return '405'



