from flask import Blueprint, render_template

project = Blueprint('project', __name__)

@project.route('/user/<username>/dashboard/project/<project_id>')
def proejct_detail(username, project_id):
    data = {'username': username}
    return render_template('project_detail.html', data=data)

