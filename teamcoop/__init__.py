# coding=utf-8
from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def create_app(config_name):

    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    app.config.from_object(config_name)

    from models import db
    db.init_app(app)

    # views 中每一个文件都是一个蓝图，在这里引入蓝图
    from views.users import users
    from views.profile import profile
    from views.share import share
    from views.setting import setting
    from views.project import project

    from views.api import api

    app.register_blueprint(users)
    app.register_blueprint(project)
    app.register_blueprint(share, url_prefix='/share')
    app.register_blueprint(setting, url_prefix='/setting')
    app.register_blueprint(api, url_prefix='/api')

    return app

