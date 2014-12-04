# coding:utf-8
from __init__ import *

users = Blueprint("users", __name__)

@users.route('/<username>/issues/')
def user_issues(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username}
        # TODO: can do better
        print session['username']
        return render_template('issue.html', data=data)
    else:
        return "uid: %s" % username + '\n' + u'用户不存在'


@users.route('/<username>/issues/<issue_id>')
def issues_detail(username, issue_id):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username}

        return 'issue_id: %s' % issue_id
    else:
        return "uid: %s" % username + '\n' + u'用户不存在'


@users.route('/<username>/project/')
def user_project(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        user_project_items = Model.Project.query.filter_by(createuserid=u.id).order_by(Model.Project.title).all()
        user_project_others = Model.Project.query.filter(Model.Project.createuserid != u.id).all()
        data = {'username': u.username}
        print user_project_items
        return render_template('project_dashboard.html', data=data, user_project_items=user_project_items,
                               user_project_others=user_project_others)
    else:
        return "uid: %s" % username + '\n' + u'用户不存在'


@users.route('/<username>/project/<project_id>')
def project_detail(username, project_id):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is None:
        return "uid: %s" % username + '\n' + u'用户不存在'
    else:
        # project = Model.Project.query.filter_by(project_id=unicode(project_id)).first()
        if project_id is not None:
            data = {'username': u.username, 'project_id': project_id}
            return render_template('project_detail.html', data=data)
        else:
            return redirect(url_for('.user_project', username=username))
            # return "pid: %s" % (project_id) + '\n' + u'项目不存在'   
        

@users.route('/<username>/setting/')
def user_setting(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username, 'user_level': u.level}
        # TODO: can do better
        # print data
        return render_template('setting.html', data=data)
    else:
        return "uid: %s, slug: %s" % (username, dash) + '\n' + u'用户不存在'








@users.route('/test/')
def test():
    return render_template('login_test.html')




