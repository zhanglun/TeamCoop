from flask import Blueprint, render_template
from __init__ import *

setting = Blueprint('setting', __name__)

@setting.route('/<username>', methods=['GET', 'POST'])
def setting_user(usrename):

    return render_template('setting.html')