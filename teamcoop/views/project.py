# coding:utf-8

from __init__ import *

project = Blueprint('project', __name__)

@project.route('/<project_id>/')
def project_detail(project_id):
    if project_id is not None:
        p = Model.Project.query.filter_by(id=project_id).first()
        issues = project_issues(project_id)
        data = {'username': session['username'], 'userid': session['userid'], 'project': p.get_json(),
                        'issues': issues}
        return render_template('project_detail.html', data=data)
    else:
        return '405'