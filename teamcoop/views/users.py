# coding:utf-8
from __init__ import *

users = Blueprint("users", __name__)


@users.route('/')
def index():
    if session.get('username') is not None:
        print session['username']
        return redirect(url_for('.user_issues', username=session['username']))
    else:
        form = userlogin.LoginForm()
        return render_template('login.html', form=form)


@users.route('/signin/', methods=['GET', 'POST'])
def submit():
    form = userlogin.LoginForm()
    if form.is_submitted():
        print "submitted"
    if form.validate():
        print "valid"
    if form.validate_on_submit():
        # check the password and log user in
        name = form.username.data
        u = Model.User.query.filter_by(username=name).first()
        if u is None or form.password.data != u.password:
            flash(u'用户名或密码错误')
            # if user is not exist, redirect to '/'
            return render_template('login.html', form=form)
        elif form.password.data == u.password:
            session['username'] = name
            return redirect(url_for('.user_issues', username=name))
        else:
            return render_template('login.html', form=form)

@users.route('/logout/')
def user_logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    form = userlogin.LoginForm()
    return redirect(url_for('.index'))


@users.route('/user/<username>/issues/')
def user_issues(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username}
        # TODO: can do better
        print session['username']
        return render_template('issue.html', data=data)
    else:
        return "uid: %s" % (username) + '\n' + u'用户不存在'


@users.route('/user/<username>/issues/<issue_id>')
def issues_detail(username, issue_id):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username}

        return 'issue_id: %s' % (issue_id)
    else:
        return "uid: %s" % (username) + '\n' + u'用户不存在'


@users.route('/user/<username>/project/')
def user_project(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username}
        # TODO: can do better
        return render_template('project_dashboard.html', data=data)
    else:
        return "uid: %s" % (username) + '\n' + u'用户不存在'


@users.route('/user/<username>/project/<project_id>')
def project_detail(username, project_id):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is None:
        return "uid: %s" % (username) + '\n' + u'用户不存在'
    else:
        # project = Model.Project.query.filter_by(project_id=unicode(project_id)).first()
        if project_id is not None:
            data = {'username': u.username, 'project_id': project_id}
            return render_template('project_detail.html', data=data)
        else:
            return redirect(url_for('.user_project', username=username))
            # return "pid: %s" % (project_id) + '\n' + u'项目不存在'   
        

@users.route('/user/<username>/setting/')
def user_setting(username):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username,'user_level': u.level}
        # TODO: can do better
        print data
        return render_template('setting.html', data=data)
    else:
        return "uid: %s, slug: %s" % (username, dash) + '\n' + u'用户不存在'








@users.route('/test/')
def test():
    return render_template('login_test.html')




