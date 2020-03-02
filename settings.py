# -*- coding=utf-8 -*-
class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///my.db"
    SECRET_KEY = 'helloworld..'

    # 消息每页大小
    MESSAGE_SIZE_PER_PAGE = 15


class DevelopmentConfig(BaseConfig):
    pass

class ProductionConfig(BaseConfig):
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}