import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:fakepassword@localhost/fake_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = '../minimum_flask_storage/'

    LOGGING = {
        'log_file_path': '../minimum_flask_log/flask_backend.log',
        'level': logging.DEBUG,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }

    ###################################################################################################################
    # redis set up
    ###################################################################################################################
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
