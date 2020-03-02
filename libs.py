# -*- coding=utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from flask import session, redirect, url_for, request, abort
from functools import wraps
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from flask_moment import Moment

# 创建数据库对象
# 此处app实例尚未创建，所以不用传入app实例对象
db = SQLAlchemy()
csrf = CSRFProtect()
socketio = SocketIO()
moment = Moment()

def login_required(func):
    @wraps(func)
    def decorator_nest(*args, **kwargs):
        if not 'user' in session:
            return redirect(url_for('login'))
        else:
            print(func)
            return func(*args, **kwargs)
    return decorator_nest

def admin_required(func):
    @wraps(func)
    def decorator_nest(*args, **kwargs):
        if session.get('user') != 'admin':
            abort(404)
        else:
            print(func)
            return func(*args, **kwargs)
    return decorator_nest
