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

    L = u + depart + project + u_project + task + t_comment
    L.sort(cmp=lambda x, y: cmp(x.get_time(), y.get_time()))
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

    L = u + depart + project + u_project + task + t_comment
    L.sort(cmp=lambda x, y: cmp(x.get_time(), y.get_time()))

    # for x in L:
    # print str(x.get_time()) + '\n'


@users.route('/<username>/issues/')
def user_issues(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    user_id = u.id
    if u is not None:
        data = {'username': u.username, 'userid': u.id}
        # TODO: can do better
        #
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
        print user_project_items
        print user_project_others
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
        # project = Model.Project.query.filter_by(project_id=unicode(project_id)).first()
        if project_id is not None:
            data = {'username': u.username, 'userid': u.id, 'project_id': project_id}
            return render_template('project_detail.html', data=data)
        else:
            return redirect(url_for('.user_project', username=username))
            # return "pid: %s" % (project_id) + '\n' + u'项目不存在'   


@users.route('/<username>/setting/')
def user_setting(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username, 'userid': u.id, 'user_level': u.level}
        # TODO: can do better
        # print data
        return render_template('setting.html', data=data)
    else:
        return "uid: %s" % username + '\n' + u'用户不存在'


@users.route('/test/')
def test():
    return render_template('login_test.html')




