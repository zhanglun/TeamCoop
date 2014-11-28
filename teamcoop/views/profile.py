#coding:utf-8

from flask import Blueprint, render_template


profile = Blueprint('profile', __name__)


@profile.route('/')
def index():
    return 'profile'


@profile.route('/<user_url_slug>')
def timeline(user_url_slug):
    # 做些处理
    return 'user/'


@profile.route('/<user_url_slug>/photos')
def photos(user_url_slug):
    # 做些处理
    return 'user/photos'


@profile.route('/<user_url_slug>/about')
def about(user_url_slug):
    # 做些处理
    return 'user/about'