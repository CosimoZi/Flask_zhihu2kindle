import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'hard to guess string'
    DEBUG = True

    MAIL_SERVER='smtp-mail.outlook.com'
    MAIL_PORT=465
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'zhihu2kindle@outlook.com'
    MAIL_PASSWORD = 'afcaerca1fava'

    @staticmethod
    def init_app(app):
        pass




