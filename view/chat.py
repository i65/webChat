# # -*- coding: utf-8 -*-
from flask import render_template, session, Blueprint, request, current_app

from libs import socketio, db
from flask_socketio import emit
from models import Message, User
from datetime import datetime

chat_app = Blueprint('chat_app', __name__)


online_users = []
online_users_info = []

@socketio.on('new message')
def new_message(message_body):
    current_user_id = session.get('user_id')
    current_username = session.get('user')

    html_message = message_body['data']
    to_author_id = message_body['id']
    # 判断是否用户给自己发的留言
    flag = 0
    if current_user_id != to_author_id:
        d = datetime.utcnow()
        message = Message(from_author_id=current_user_id, to_author_id=to_author_id, body=html_message, created_at=d)
        db.session.add(message)
        db.session.commit()
        if to_author_id:
            to_user = User.query.get(to_author_id)
            message.to_username = to_user.username
        else:
            message.to_username = ''
        message.from_username = current_username
        flag = 1
    else:
        message = {}
        html_message = ''
        current_username = ''
        message.from_username = ''
        message.to_author_id = ''

    emit('new message',
         {
             'message_body': html_message,
             'username': current_username,
             'user_id': current_user_id,
             'to_username': message.to_username,
             'to_user_id': message.to_author_id,
             'flag': flag
          },  broadcast=True)

@socketio.on('connect')
def connect():
    global online_users
    user_id = session.get('user_id', 0)
    if user_id and user_id not in online_users:
        online_users.append(user_id)
        users =get_users(online_users)
        emit('user_connect', {
            'count': len(online_users),
            'user_html': render_template('_users.html', users=users),
            }, broadcast=True)

@socketio.on('disconnect')
def disconnect():
    global online_users
    user_id = session.get('user_id', 0)
    if user_id and user_id in online_users:
        online_users.remove(user_id)
        users = get_users(online_users)

        emit('user_disconnect', {
            'count': len(online_users),
            'user_html': render_template('_users.html', users=users),
            }, broadcast=True)

@chat_app.route('/messages')
def get_messages():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MESSAGE_SIZE_PER_PAGE']
    pagination = Message.query.order_by(Message.created_at.desc()).paginate(page, per_page)
    messages = pagination.items

    users = User.query.all()
    for msg in messages:
        for user in users:
            if msg.from_author_id == user.id:
                msg.from_username = user.username
            if msg.to_author_id == user.id:
                msg.to_username = user.username
    return render_template('_messages.html', messages=messages[::-1])

def get_users(ids):
    users = User.query.order_by(User.last_login_time.desc(), User.created_at.desc()).all()
    for user in users:
        if user.id in ids:
            user.last_login_time = datetime.utcnow()

    db.session.commit()
    return users

@chat_app.context_processor
def get_all_user():
    users = User.query.order_by(User.is_login.desc(),User.last_login_time.desc(),User.created_at.desc()).all()
    return {'users': users}
