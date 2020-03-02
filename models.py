# -*- coding=utf-8 -*-
from libs import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    realname = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    is_login = db.Column(db.Integer, default=0)
    last_login_time = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    messages = db.relationship('Message')

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    from_author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    to_author_id = db.Column(db.Integer, default=0)
