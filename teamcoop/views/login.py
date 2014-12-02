# coding:utf-8
from __init__ import *

login = Blueprint("login", __name__)


@login.route('/')
def index():
    form = userlogin.LoginForm()
    return render_template('login.html', form=form)


@login.route('/signin/', methods=['GET', 'POST'])
def submit():
    form = userlogin.LoginForm()
    if form.is_submitted():
        print "submitted"
    if form.validate():
        print "valid"
    if form.validate_on_submit():
        # check the password and log user in
        name = form.username.data
        print type(name)
        u = UserModel.User.query.filter_by(username=name).first()
        if u is None or form.password.data != u.password:
            flash(u'用户名或密码错误')
            # if user is not exist, redirect to '/'
            return render_template('login.html', form=form)
        elif form.password.data == u.password:
            return redirect(url_for('.user', username=name))
        else:
            return render_template('login.html', form=form)


@login.route('/user/<username>/')
def user(username):
    print username
    print type(username)
    u = UserModel.User.query.filter_by(username=unicode(username)).first()
    data = {'username': u.username}
    return render_template('project_dashboard.html', data = data)





