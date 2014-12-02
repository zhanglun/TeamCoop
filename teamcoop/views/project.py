from flask import Blueprint, render_template

project = Blueprint('project', __name__)

@project.route('/')
def index():
    return render_template('project_dashboard.html')
    # return 'ddd'


@project.route('/dashboard/')
def dashboard():
    return render_template('project_dashboard.html')


@project.route('/detail/')
def detail():
    return render_template('project_detail.html')
