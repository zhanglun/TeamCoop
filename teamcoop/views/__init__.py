# coding: utf8
# 在 views 的 __init__.py 中导入forms和models

import json
import dateutil.parser
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response, g
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter

from teamcoop.forms import userlogin
from teamcoop.models import db
from teamcoop.models import model as Model


def api_response(status, code, message, result=None):
    response_dict = {'code': code, 'message': message, 'result': result}
    response = make_response(jsonify(response_dict))
    response.status = str(status)
    return response

panel = {'issues': 'issues', 'setting': 'setting', 'dashboard': 'dashboard'}

