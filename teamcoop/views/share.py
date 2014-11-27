
from flask import Blueprint, render_template

share = Blueprint('share', __name__)

@share.route('/')
def index():
    return "share index"

