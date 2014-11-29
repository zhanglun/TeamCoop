import os
basedir = os.path.abspath(os.path.dirname(__file__)) + "\\db"
#
# class Config:
#     CSRF_ENABLED = True
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
#     SQLALCHEMY_COMMIT_ON_TEARDOWN = True
#     FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
#     FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
#     FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
#
#     @staticmethod
#     def init_app(app):
#         pass
#
#
# class DevelopmentConfig(Config):
#     DEBUG = True
#     MAIL_SERVER = 'smtp.googlemail.com'
#     MAIL_PORT = 587
#     MAIL_USE_TLS = True
#     MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#     MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev\\test.db')
#
#
# class TestingConfig(Config):
#     TESTING = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'dev\\teamcoop-test.db')
#
#
# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'pub\\teamcoop.db')
#
#
# config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }


DEBUG = True
SECRET_KEY = 'mysecretkey'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev\\test.db')