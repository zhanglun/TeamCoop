from flask import Blueprint, render_template
from __init__ import *

setting = Blueprint('setting', __name__)

@setting.route('/', methods=['GET', 'POST'])
def index():
    return render_template('setting.html')