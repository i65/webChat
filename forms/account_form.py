# -*- coding=utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    '''
    登录表单
    '''
    username = StringField('用户名',
                           validators=[DataRequired(message='请填写用户名.')],
                           render_kw={'placeholder': '用户名'})
    password = PasswordField('密码',
                             validators=[DataRequired(message='请输入密码.'),
                                         Length(min=6, max=20, message='密码不能少于 6 个字符.')],
                             render_kw={'placeholder': '密码'})

    submit = SubmitField('',
                         render_kw={'class': 'ui fluid large teal submit button', 'type': 'button', 'value': '立即登录'})


from wtforms.validators import ValidationError

class BadWords:
    '''
    敏感词检查通用验证器
    '''
    def __init__(self, bad_words, message=None):
        '''
        :param bad_words: 敏感词列表
        :param message: 错误提示
        '''
        self.bad_words = bad_words
        if not message:
            message = '不能包含敏感词'
        self.message = message

    def __call__(self, form, field):
        '''
        :param form: 验证表单对象
        :param field: 验证字段对象
        :return:
        '''
        for word in self.bad_words:
            if field.data.find(word) != -1:
                raise ValidationError(self.message)

class RegisterForm(FlaskForm):
    '''
    注册表单
    '''
    realname = StringField('姓名',
                           validators=[BadWords(['admin', '客户服务', '客户', '管理员'], message='不能包含敏感字符')],
                           render_kw={'placeholder': '姓名'})

    username = StringField('用户名',
                           validators=[DataRequired(message='请填写用户名'),
                                       Length(min=2, max=12, message='用户名 2 ~ 12 个字符'),
                                       BadWords(['admin', '客户服务', '管理员'], message='不能包含敏感字符')],
                           render_kw={'placeholder': '用户名'})
    password = PasswordField('密码',
                             validators=[DataRequired(message='请填写密码'),
                                         Length(min=6, max=20, message='密码 6 ~ 20 个字符')],
                             render_kw={'placeholder': '密码'})
    password2 = PasswordField('验证密码',
                                    validators=[DataRequired(message='请填写验证密码'),
                                                Length(min=6, max=20, message='确认密码 6 ~ 20 个字符'),
                                                EqualTo(fieldname='password', message='两次密码输入不一致')],
                                    render_kw={'placeholder': '验证密码'})
    submit = SubmitField('',
                         render_kw={'class': 'ui fluid large teal submit button', 'type': 'button', 'value': '立即注册'})
