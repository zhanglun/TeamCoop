# coding:utf-8

from __init__ import *

login = Blueprint("login", __name__)


@login.route('/')
def index():
    form = userlogin.LoginForm()
    return render_template('login.html', form=form)


@login.route('/checkuser/', methods=['GET', 'POST'])
def submit():
    form = userlogin.LoginForm()
    if form.is_submitted():
        print "submitted"
    if form.validate():
        print "valid"
    if form.validate_on_submit():
        # check the password and log user in
        print "username"
        flash("Successfully created a new book")
        return redirect(url_for('.index'))

    return redirect(url_for('.index'))



