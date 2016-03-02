# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail

from config import Config
bootstrap = Bootstrap()
mail=Mail()

def create_app():
    app=Flask(__name__)
    bootstrap.init_app(app)
    mail.init_app(app)
    app.config.from_object(Config)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
