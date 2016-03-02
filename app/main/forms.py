# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms.fields import RadioField, SubmitField, StringField
from wtforms.validators import DataRequired


class AddressForm(Form):
    address = StringField(u'用户主页:', validators=[DataRequired()])
    need_comments_or_not = RadioField(u'是否包括评论',
                                       choices=[(u'no comments', u'无评论'), (u'only conversations', u'仅答主评论与对话(推荐)'),
                                                (u'all comments', u'全部评论')],validators=[DataRequired()])
    email=StringField(u'Kindle地址:')
    captcha=StringField(u'验证码:')
    captcha_1=StringField(u'验证码:')
    submit_download=SubmitField(u'下载Mobi')
    submit_send=SubmitField(u'推送到Kindle')