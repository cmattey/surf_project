import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    # retrieve from local environemt file
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI  = os.environ['DATABASE_URL']
    POSTS_PER_PAGE = 5

    MSW_API_KEY = os.environ.get('MSW_API_KEY')
    MSW_API_URL = "http://magicseaweed.com/api/{key}/forecast/?spot_id={spot_id}"


class ProductionConfig(Config):
    DEBUG = False
    POSTS_PER_PAGE = 15


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    POSTS_PER_PAGE = 15


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
