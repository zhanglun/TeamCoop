from flask import Flask, request, url_for, make_response, redirect, render_template, session, flash
# from route import *

app = Flask(__name__)
app.config.from_pyfile('config.py')



@app.route('/')
def index():
    return 'Welcome!'


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


if __name__ == '__main__':
    app.run()