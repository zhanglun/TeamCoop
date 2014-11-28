# coding: utf8
# 在 views 的 __init__.py 中导入forms和models

from flask import Blueprint, render_template, request, redirect, url_for, flash
from teamcoop.forms import userlogin
from teamcoop.models import users

