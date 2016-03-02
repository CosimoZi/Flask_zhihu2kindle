import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess string'
    DEBUG = True

    @staticmethod
    def init_app(app):
        pass




