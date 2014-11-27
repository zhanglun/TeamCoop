from flask import Flask, render_template
from config import config


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from views.profile import profile
    from views.share import share
    from views.setting import setting
    from views.project import project

    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(project, url_prefix='/project')
    app.register_blueprint(share,  url_prefix='/share')
    app.register_blueprint(setting,  url_prefix='/setting')


@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/checkuser/', methods=['GET', 'POST'])
def checkuser():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
            print error
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
            print error
        else:
            session['logged_in'] = True
            flash('You were logged in')
            print error
            return redirect(url_for('index'))
    return render_template('login.html', error=error)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', now = datetime.utcnow()), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



