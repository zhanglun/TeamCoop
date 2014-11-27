from flask import Blueprint, render_template

setting = Blueprint('setting', __name__)

@setting.route('/')
def index():
    return "setting index"