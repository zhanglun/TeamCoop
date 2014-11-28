# coding=utf-8
from flask import Flask, render_template
from config import config


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # views 中每一个文件都是一个蓝图，在这里引入蓝图
    from views.login import login
    from views.profile import profile
    from views.share import share
    from views.setting import setting
    from views.project import project

    app.register_blueprint(login)
    app.register_blueprint(profile, url_prefix='/profile')
    app.register_blueprint(project, url_prefix='/project')
    app.register_blueprint(share, url_prefix='/share')
    app.register_blueprint(setting, url_prefix='/setting')

    return app



