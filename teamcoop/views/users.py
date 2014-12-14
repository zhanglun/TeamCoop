# coding:utf-8
from __init__ import *

users = Blueprint("users", __name__)

@users.route('/<username>/issues/')
def user_issues(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    user_id = u.id
    if u is not None:
        other_issues = get_other_issues(user_id)
        related_issues = get_related_issues(user_id)
        data = {'username': u.username, 'userid': u.id, 'related_issues': related_issues, 'other_issues': other_issues}
        session['username'] = u.username
        session['userid'] =  u.id
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
        user_project_items = []
        user_project_others = []
        u_p = Model.UserProject.query.filter_by(userId=u.id).all()
        for p in u_p:
            user_project_items.append(Model.Project.query.filter_by(id=p.projectId).order_by(Model.Project.title).first())

        u_p_other = Model.UserProject.query.filter(Model.UserProject.userId!=u.id).order_by(Model.UserProject.projectId).all()

        for p in u_p_other:
            user_project_others.append(Model.Project.query.filter_by(id=p.projectId).order_by(Model.Project.title).first())
            
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




