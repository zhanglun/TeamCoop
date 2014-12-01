# coding: utf8
# 在 views 的 __init__.py 中导入forms和models

import json
import yaml
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy

from teamcoop.forms import userlogin
from teamcoop.models import db, user


api_response_dict={'code': '', 'result': ''}