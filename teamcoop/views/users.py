# coding:utf-8
from __init__ import *

users = Blueprint("users", __name__)

issues_body = {'subject': '管理员', 'object': 'XX', 'action': ''}


# 添加了新成员
# 创建了新项目
# 在XX项目中添加了新成员
# 在XX项目中添加了新任务，并分配给XX
# 在XX项目中的XX任务中发布了评论



class IssueControler():
    pass


def get_related_issues(userid):
    # 管理员添加用户
    u = Model.User.query.all()

    # 管理员添加部门
    depart = Model.DepartMent.query.filter(Model.Project.createuserid == userid).all()

    # 用户添加项目
    project = Model.Project.query.filter(Model.Project.createuserid == userid).all()
    # 用户加入到项目中
    u_project = Model.UserProject.query.filter(Model.UserProject.userId == userid).all()

    # 用户添加任务或者执行
    task = Model.Task.query.filter(Model.Task.createUserId == userid or Model.Task.executeUserId == userid).all()
    # 用户添加任务评论
    t_comment = Model.TaskComment.query.filter(Model.TaskComment.userId == userid).all()

    l = u + depart + project + u_project + task + t_comment
    l.sort(cmp=lambda x, y: cmp(x.get_time(), y.get_time()))
    pass


def get_other_issues(userid):
    # 管理员添加用户
    u = Model.User.query.all()
    # 管理员添加部门
    depart = Model.DepartMent.query.all()

    # 用户添加项目
    project = Model.Project.query.filter(Model.Project.createuserid != userid).all()
    # 用户加入到项目中
    u_project = Model.UserProject.query.filter(Model.UserProject.userId != userid).all()

    # 用户添加任务或者执行
    task = Model.Task.query.filter(Model.Task.createUserId != userid or Model.Task.executeUserId != userid).all()
    # 用户添加任务评论
    t_comment = Model.TaskComment.query.filter(Model.TaskComment.userId != userid).all()

    l = u + depart + project + u_project + task + t_comment
    l.sort(cmp=lambda x, y: cmp(x.get_time(), y.get_time()))


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
                issues.append({'flag': 'add new project', 'person_in_charge': u.username, 'task_title': p.title,
                               'create_time':
                    x.createtime})
            elif x.level == 2:
                issues.append({'flag': 'join new project', 'participant': u.username, 'task_title': p.title,
                               'create_time':
                    x.createtime})

    # Task
    t = Model.Task.query.filter_by(projectId=project_id).order_by(Model.Task.createtime).all()

    if t is not None:
        for x in t:
            execute_u = Model.User.query.filter_by(id=x.executeUserId).first()
            create_u = Model.User.query.filter_by(id=x.createUserId).first()
            issues.append({'flag': 'deploy new task', 'deployer': create_u.get_json()['username'], 'executer': execute_u.get_json()['username'], 'task_title': p.title, 'create_time': x.createtime})

    # project_comment
    p_c = Model.ProjectComment.query.filter_by(projectId=project_id).order_by(Model.ProjectComment.createtime).all()

    if p_c is not None:
        for c in p_c:
            u = Model.User.query.filter_by(id=c.userId).first()
            issues.append({'flag': 'add new comment', 'publisher': u.username, 'comment': p_c.content, 'create_time':
                c.createtime})

    issues.sort(key=lambda x: x['create_time'])
    return issues

@users.route('/<username>/issues/')
def user_issues(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    user_id = u.id
    if u is not None:
        data = {'username': u.username, 'userid': u.id}
        # TODO: can do better
        #
        session['username'] = u.username
        get_related_issues(user_id)
        get_other_issues(user_id)
        return render_template('issue.html', data=data)
    else:
        # return
        return "uid: %s" % username + '\n' + u'用户不存在'


@users.route('/<username>/issues/<issue_id>/')
def issues_detail(username, issue_id):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username, 'userid': u.id}

        return 'issue_id: %s' % issue_id
    else:
        return "uid: %s" % username + '\n' + u'用户不存在'


@users.route('/<username>/project/')
def user_project(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        user_project_items = Model.Project.query.filter_by(createuserid=u.id).order_by(Model.Project.title).all()
        user_project_others = Model.Project.query.filter(Model.Project.createuserid != u.id).all()
        data = {'username': u.username, 'userid': u.id}
        session['username'] = username
        return render_template('project_dashboard.html', data=data, user_project_items=user_project_items,
                               user_project_others=user_project_others)
    else:
        return "uid: %s" % username + '\n' + u'用户不存在'


@users.route('/<username>/project/<project_id>/')
def project_detail(username, project_id):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is None:
        return "uid: %s" % username + '\n' + u'用户不存在'
    else:
        if project_id is not None:
            p = Model.Project.query.filter_by(id=project_id).first()
            issues = project_issues(project_id)
            data = {'username': u.username, 'userid': u.id, 'project_id': project_id, 'project': p.get_json(),
                    'issues': issues}
            return render_template('project_detail.html', data=data)
        else:
            return redirect(url_for('.user_project', username=username))


@users.route('/<username>/setting/')
def user_setting(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username, 'userid': u.id, 'user_level': u.level, 'name': u.name}
        return render_template('setting.html', data=data)
    else:
        return "uid: %s" % username + '\n' + u'用户不存在'


@users.route('/test/')
def test():
    return render_template('login_test.html')




