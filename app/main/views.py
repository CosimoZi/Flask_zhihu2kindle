# -*- coding: utf-8 -*-
from flask import render_template, session, redirect, send_file
from flask_mail import Message
from shutil import copyfile

from . import main
from .forms import AddressForm
from app.main.zhihu2kindle.work.ZhihuSpider import ZhihuSpider
from app.main.zhihu2kindle.work.generate_ebook import generate_ebook
from config import basedir
from mail import send_email


@main.route('/', methods=['GET', 'POST'])
def index():
    Message('hello',recipients=['xzyufo@outlook.com'])
    spider=ZhihuSpider()
    spider.get_captcha()
    form = AddressForm()
    if form.validate_on_submit():
        session['address']=form.address.data
        if form.email.data:
            session['captcha']=form.captcha_1.data
            session['email']=form.email.data
            spider.login(session['captcha'])
            session['comment']=form.need_comments_or_not.data
            data=spider.get_data(session['address'])
            generate_ebook(data,mode=session['comment'])
            copyfile(basedir+"/app/main/zhihu2kindle/ebook/book.mobi",basedir+'/app/book.mobi')
            return redirect('/')
        else:
            session['captcha']=form.captcha.data
            # while spider.login(session['captcha'])=='Failed':
            #     spider.get_captcha()
            spider.login(session['captcha'])
            session['comment']=form.need_comments_or_not.data
            data=spider.get_data(session['address'])
            generate_ebook(data,mode=session['comment'])
            return send_file(basedir+"/app/main/zhihu2kindle/ebook/book.mobi",as_attachment=True)
    return render_template('index.html', form=form)

@main.route('/mail')
def mail():
    send_email('xzyufo@outlook.com','徐子悠')
    return '<p>test mail</p>'