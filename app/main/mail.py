# -*- coding: utf-8 -*-
from flask import current_app
from flask.ext.mail import Message

from .. import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(kindle_address,author_name):
    app = current_app._get_current_object()
    msg = Message(author_name,sender='zhihu2kindle@outlook.com',recipients=[kindle_address])
    # with app.open_resource("book.mobi") as fp:
    #     msg.attach(filename="book.mobi",content_type=None,data=fp.read())
    send_async_email(app,msg)



