# -*- coding=utf-8 -*-
from flask import Flask, request, render_template, url_for, session, jsonify, redirect, current_app
from forms.account_form import LoginForm, RegisterForm
from libs import db, csrf, socketio, moment
from models import User, Message
from settings import config
from flask_migrate import Migrate
from view.chat import *


app = Flask(__name__)
app.config.from_object(config['development'])

db.init_app(app)
csrf.init_app(app)
moment.init_app(app)
socketio.init_app(app)

app.register_blueprint(chat_app, url_prefix='/chat')

@app.route('/')
def index():
    if not session.get('user'):
        return redirect(url_for('login'))
    users = User.query.order_by(User.last_login_time.desc(),User.created_at.desc()).all()

    amount = current_app.config['MESSAGE_SIZE_PER_PAGE']
    messages = Message.query.order_by(Message.created_at.asc())[-amount:]
    for msg in messages:
        for user in users:
            if msg.from_author_id == user.id:
                msg.from_username = user.username
            if msg.to_author_id == user.id:
                msg.to_username = user.username

    user_amount = User.query.count()
    return render_template('index.html', users=users, online_user_amount=len(users), user_amount=user_amount, messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 已经登录的直接跳转到首页
    if session.get('user'):
        return redirect(url_for('index'))

    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)

    if form.validate_on_submit():
        username = form.data['username'].replace(' ', '')
        password = form.data['password'].replace(' ', '')
        user = User.query.filter_by(username=username).first()

        if user and user.validate_password(password):
            session['user'] = user.username
            session['user_id'] = user.id
            user.is_login = 1
            user.last_login_time = datetime.utcnow()
            db.session.commit()
            # 登录成功返回首页
            return jsonMsg('success','登录成功，正在进入聊天室...',url_for('index'))
        else:
            return jsonMsg('fail','登录失败：用户名或密码错误')
    else:
        print(form.errors)
        error_msg = ';'.join([msg[0] for msg in form.errors.values()])
        error_msg =  '登录失败: ' + error_msg,
        return jsonMsg('fail',error_msg)


def validate_username(username):
    '''
    验证用户名是否重复
    :param username: 用户名
    :return:
    '''
    return User.query.filter_by(username=username).first()

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)

    if form.validate_on_submit():
        realname = form.data['realname']
        username = form.data['username']
        password = form.data['password']
        if validate_username(username):
            return jsonMsg('fail','注册失败: 用户名已存在',)

        user = User(
            realname = realname,
            username = username,
            password = password,
        )
        # 密码加密
        user.hash_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonMsg('success', '注册成功，正在前往 登录...', url_for('login'))
        except Exception as e:
            msg =  '注册失败：' + str(e)
            return jsonMsg('fail',msg)
    else:
        print(form.errors)
        error_msg = ';'.join([msg[0] for msg in form.errors.values()])
        error_msg =  '注册失败: ' + error_msg
        return jsonMsg('fail',error_msg)

@app.route('/logout')
def logout():
    message = None
    if session.get('user'):
        user = User.query.filter_by(username=session.get('user')).first()
        user.is_login = 0
        db.session.commit()
        session.pop('user')
        session.pop('user_id')

        message = {
            'result': 'success',
            'message': '已退出，正在前往 登录页面...',
            'url': url_for('index')
        }

    return jsonify(message)

def jsonMsg(res, msg, url=''):
    return jsonify({
        'result': res,
        'message': msg,
        'url': url
    })


migrate = Migrate(app, db, render_as_batch=True)