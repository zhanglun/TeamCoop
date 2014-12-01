from flask import Blueprint, render_template

project = Blueprint('project', __name__)

@project.route('/')
def index():
    return 'project index'
