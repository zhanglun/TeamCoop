# usr/bin/env python
# coding:utf-8

from __init__ import *

login = Blueprint('login', __name__)

@login.route('/')
def index():
    username = session.get('username')
    u = Model.User.query.filter_by(username=username).first()
    if username and u:
        return redirect(url_for('users.user_issues', username=session['username']))
    else:
        form = userlogin.LoginForm()
        # session.pop('username')
        return render_template('login.html', form=form)


@login.route('/signin/', methods=['GET', 'POST'])
def submit():
    form = userlogin.LoginForm()
    if form.validate_on_submit():
        # check the password and log user in
        name = form.username.data
        u = Model.User.query.filter_by(username=name).first()
        if u is None or form.password.data != u.password:
            flash(u'用户名或密码错误')
            # if user is not exist, redirect to '/'
            return render_template('login.html', form=form)
        
        if form.password.data == u.password:
            if form.remember.data ==True:
                session['username'] = name
            return redirect(url_for('users.user_issues', username=name))
        else:
            flash(u'用户名或密码错误')
            return render_template('login.html', form=form)
    else:
        return "登陆错误，请联系管理员"

@login.route('/logout/')
def user_logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    # form = userlogin.LoginForm()
    return redirect(url_for('.index'))

