# usr/bin/env python
# coding:utf-8

from __init__ import *

login = Blueprint('login', __name__)

@login.route('/')
def index():
    if session.get('username') is not None:
        print session['username']
        return redirect(url_for('users.user_issues', username=session['username']))
    else:
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

@login.route('/logout/')
def user_logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    # form = userlogin.LoginForm()
    return redirect(url_for('.index'))

