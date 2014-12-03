# coding:utf-8
from __init__ import *

users = Blueprint("users", __name__)


@users.route('/')
def index():
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
            return redirect(url_for('.user', username=name, dash='issues'))
        else:
            return render_template('login.html', form=form)


# @users.route('/user/<regex("[\s]\w+[\s]"):userid>/<slug>/')
# def project(userid, slug):
#     u = Model.User.query.filter_by(username=unicode(userid)).first()
#     if u is not None:
#         data = {'username': u.username, 'part': str(slug)}
#         if str(slug) == 'dashboard':
#             return render_template('project_dashboard.html', data=data)
#         elif str(slug) == 'setting':
#             return render_template('setting.html', data=data)
#     else:
#         return "uid: %s, slug: %s" % (userid, slug)


@users.route('/user/<username>/<dash>/')
def user(username, dash):
    u = Model.User.query.filter_by(username=unicode(username)).first()
    if u is not None:
        data = {'username': u.username}
        # TODO: can do better
        part = {'issues': 'issues', 'setting': 'setting', 'dashboard': 'dashboard'}
        print 'dash'
        print dash
        if dash == 'issues':
            return render_template('issue.html', data=data, dash=part)
        elif dash == 'dashboard':
            return render_template('project_dashboard.html', data=data, dash=part)
        elif dash == 'setting':
            return render_template('setting.html', data=data, dash=part)
        else:
            print dash
            return "uid: %s, slug: %s" % (username, dash)
    else:
        return "uid: %s, slug: %s" % (username, dash) + '\n' + u'用户不存在'


@users.route('/test/')
def test():
    return render_template('test.html')




