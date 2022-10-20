from distutils.command.config import config
from distutils.debug import DEBUG

from sqlalchemy import false


class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://root:4ever23/@localhost/api_cody'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mariadb+mariadbconnector://root:4ever23/@localhost/test_cody'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'test': TestConfig,
    'development': DevelopmentConfig 
}