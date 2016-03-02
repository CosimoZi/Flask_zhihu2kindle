from app.main.zhihu2kindle.work.ZhihuSpider import ZhihuSpider
from app.main.zhihu2kindle.work.generate_ebook import generate_ebook
from os.path import relpath
from config import basedir

if __name__=='__main__':
    s=ZhihuSpider()
    s.get_captcha()
    print 'captcha:'
    c=raw_input()
    while s.login(c)=='Failed':
        s.get_captcha()
        print 'captcha'
        c=raw_input()

    data=s.get_data('https://www.zhihu.com/people/https://www.zhihu.com/people/ji-xuan-yi-9')
    # generate_ebook(data,mode=1)
    print data[0]
    # templates_dir=basedir+"/app/main/zhihu2kindle/work/templates/"
    # print relpath(templates_dir)