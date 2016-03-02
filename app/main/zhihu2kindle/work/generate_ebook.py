# -*- coding:utf-8 -*-
import jinja2
import time
from os import system
from os.path import relpath
from config import basedir


def generate_ebook(data, mode=u'only conversations'):
    name, questions, answers, comments, conversations = data
    amount = len(questions)
    templates_dir = basedir + "/app/main/zhihu2kindle/work/templates/"
    ebook_dir = basedir + '/app/main/zhihu2kindle/ebook/'
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(relpath(templates_dir)))

    def add_content():
        if mode == u'no comments':
            template = env.get_template('content_module.html')
        elif mode == u'only conversations':
            template = env.get_template('content_with_only_conversations.html')
        elif mode == u'all comments':
            template = env.get_template('content_with_all_comments.html')
        with open(ebook_dir + "content.html", 'wb') as f:
            f.write(template.render(amount=amount, questions=questions, answers=answers, comments=comments,
                                    conversations=conversations).encode('utf-8'))

    def add_toc():
        template = env.get_template('toc_module.html')
        with open(ebook_dir + "toc.html", 'wb') as f:
            f.write(template.render(amount=amount, questions=questions).encode('utf-8'))

    def add_ncx():
        # env=jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = env.get_template('toc_module.ncx')
        with open(ebook_dir + 'toc.ncx', 'wb')as f:
            f.write(template.render(amount=amount, questions=questions).encode('utf-8'))

    def add_opf():
        # env=jinja2.Environment(loader=jinja2.FileSystemLoader('.'))
        template = env.get_template('opf_module.opf')
        with open(ebook_dir + 'book.opf', 'wb')as f:
            f.write(
                template.render(amount=amount, people_name=name, time=time.asctime(time.localtime(time.time()))).encode(
                    'utf-8'))

    add_ncx()
    add_content()
    add_opf()
    add_toc()
    system((
           basedir + '/app/main/zhihu2kindle/KindleGen/kindlegen' + ' ' + basedir + '/app/main/zhihu2kindle/ebook/book.opf').encode(
        'utf-8'))



