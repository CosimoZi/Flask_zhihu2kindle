# -*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import json
from config import basedir


class ZhihuSpider():

    url = 'http://www.zhihu.com'
    session = requests.session()

    def get_captcha(self):
        captcha_dir=basedir+'/app/static/pictures/'
        captcha = self.session.get('http://www.zhihu.com/captcha.gif')
        with open(captcha_dir+'captcha.gif', 'wb') as f:
            for i in captcha.iter_content(10):
                f.write(i)


    def login(self,captcha_content):

        def get_xsrf():
            r = self.session.get(self.url)
            xsrf = re.search(r'(?<=name="_xsrf" value=")[^"]*(?="/>)', r.text)
            return xsrf.group(0)

        xsrf = get_xsrf()
        login_form_data = {'email': 'xzyufo@outlook.com', 'password': 'Nh4jEMSj', 'remember_me': 'true', '_xsrf': xsrf,
                           'captcha': captcha_content}
        req=self.session.post("http://www.zhihu.com/login/email", data=login_form_data)
        if req.json()['r']:
            return 'Failed'


    def get_data(self,people):

        def get_answerpages_amount_and_name():
            first_page = self.session.get(answers_url)
            first_soup = BeautifulSoup(first_page.text, 'lxml')
            a = first_soup.find_all('a', href=re.compile('page'))
            name = first_soup.find_all('a', class_="name")
            if not a:
                return 1, unicode(name[0].string)
            return int(a[-2].string), unicode(name[0].string)

        def get_all_comments(answer_number):
            url = 'https://www.zhihu.com/r/answers/' + answer_number + '/comments'
            js_content = self.session.get(url).content
            js_dict = json.loads(js_content)
            js_dicts = [js_dict]
            pages = (js_dict['paging']['totalCount'] + js_dict['paging']['perPage'] - 1) / js_dict['paging']['perPage']
            for i in range(2, pages + 1):
                content = self.session.get(url + '?page=' + str(i)).content
                dic = json.loads(content)
                js_dicts.append(dic)
            return js_dicts

        def get_conversations(comments):
            conversations = []
            for comments_of_one_answer in comments:
                conversation = {}
                for comments_of_one_page in comments_of_one_answer:
                    for comment in comments_of_one_page['data']:
                        if comment['author']['meta']['isAnswerAuthor']:
                            comment_content = [comment['createdTime'], comment['author']['name'], comment['content']]
                            if comment['inReplyToUser']:
                                Reply_name = comment['inReplyToUser']['name']
                                if Reply_name in conversation:
                                    conversation[Reply_name].append(comment_content)
                                else:
                                    conversation[Reply_name] = [comment_content]
                            else:
                                if 'Author_' in conversation:
                                    conversation['Author_'].append(comment_content)
                                else:
                                    conversation['Author_'] = [comment_content]
                for comments_of_one_page in comments_of_one_answer:
                    for comment in comments_of_one_page['data']:
                        author_name = comment['author']['name']
                        if author_name in conversation:
                            conversation[author_name].append(
                                [comment['createdTime'], comment['author']['name'], comment['content']])
                for single_conversation in conversation.values():
                    single_conversation.sort()
                conversations.append(conversation)
            return conversations

        answers_url = people + '/answers'
        pages_amount, name = get_answerpages_amount_and_name()
        questions = []
        answers = []
        comments = []

        for page_number in range(1, pages_amount + 1):
            page = self.session.get(answers_url + '?page=' + str(page_number))
            soup = BeautifulSoup(page.text, 'lxml')
            soup_answers = soup.find_all(class_="content hidden")
            soup_questions = soup.find_all(class_="question_link")
            # page_answers = [unicode(i.string) for i in soup_answers]
            # page_questions = [unicode(i.string) for i in soup_questions]
            # for i in page_answers:
            #     print i
            for i in soup_questions:
                questions.append(i.text)
            for j in soup_answers:
                answers.append(j.text)
            soup_answer_numbers = soup.find_all(class_="zg-anchor-hidden")
            answer_numbers = [i['name'][7:] for i in soup_answer_numbers]
            for answer_number in answer_numbers:
                comments.append(get_all_comments(answer_number))
        conversations = get_conversations(comments)
        return name, questions, answers, comments, conversations

if __name__=="__main__":
    s=ZhihuSpider()
    s.get_captcha()
    s.login()