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
        u = user.User.query.filter_all(username=name).first()
        if u is None:
            flash('用户不存在')
            return render_template('login.html', form=form)
        flash("")
        return redirect(url_for('.username', username=name))

    return redirect(url_for('.index'))


@login.route('/<username>/')
def username(username):
    return render_template('project_dashboard.html', name=username)





