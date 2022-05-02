import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '\xd5\xd4\x829uYz\x894\x82\xe0)\xe8\xc8^\xe8Z\xf7\xfa5\t\xbf3a'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    SESSION_TYPE="filesystem"
    SQLALCHEMY_DATABASE_URI="sqlite:///starter.db"