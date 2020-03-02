# -*- coding=utf-8 -*-
from libs import db
from models import User
from werkzeug.security import generate_password_hash

def createBatchUsers():
    '''
    批量生成用户
    :return:
    '''
    words = list('abcdefghijklmnopqrstuvwxyz')
    import random

    for i in range(10):
        random.shuffle(words)
        username = ''.join(words[0:6])
        is_login = random.randint(0, 1)
        user = User(
            realname = '-',
            username = username,
            password = generate_password_hash('123456'),
            is_login = is_login
        )
        db.session.add(user)
    db.session.commit()