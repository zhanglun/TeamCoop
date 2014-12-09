# coding:utf-8

from __init__ import *

project = Blueprint('project', __name__)

@project.route('/<project_id>/')
def project_detail(project_id):
    item = Model.Project.query.filter_by(id=project_id).first()
    # print session['username']
    data = {'username': session['username']}
    return render_template('project_detail.html', data=data)