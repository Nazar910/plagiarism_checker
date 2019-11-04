import os
import bcrypt
import re
from googlesearch import search
import urllib.request
from bs4 import BeautifulSoup
from bson import ObjectId

from src.utils.text_processor import get_topn_words, get_cosine_sim

LINKS_TO_CHECK = 15

class Service:
    def __init__(self, collection):
        self.coll = collection

class UserService(Service):
    def find_by_email_and_password(self, email, password):
        user = self.coll.find_one({'email': email})
        if user is None:
            return None
        expected_pass = password.encode('utf-8')
        actual_pass = user['password'].encode('utf-8')
        if bcrypt.checkpw(expected_pass, actual_pass):
            return user
        return None

    def ensure_admin_user(self, email, password):
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        admin = {
            'first_name': 'Admin',
            'last_name': 'Admin',
            'email': email,
            'password': hashed.decode('utf-8'),
            'role': 'admin'
        }
        self.coll.update_one({'email': email}, {'$set': admin}, upsert=True)

    def find_by_id(self, id):
        return self.coll.find_one({'_id': ObjectId(id)})

class Link:
    def __init__(self, **kwargs):
        assert kwargs is not None
        url = kwargs['url']
        assert url is not None
        text = kwargs['text']
        assert text is not None
        raw_html = kwargs['raw_html']
        assert raw_html is not None
        page_title = kwargs['page_title']
        assert page_title is not None

        self.url = url
        self.text = text
        self.raw_html = raw_html
        self.page_title = page_title

bs4_tags_blacklist = [
    '[document]',
    'noscript',
    'header',
    'html',
    'meta',
    'head',
    'input',
    'script',
    'style'
]

class TextService(Service):
    def get_topn_links(self, seach_str, Nlinks):
        result = []
        for url in search(seach_str, stop=Nlinks):
            try:
                response = urllib.request.urlopen(url).read()
                html = response.decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.find_all(text=True)
                output = ''

                for t in text:
                    if t.parent.name not in bs4_tags_blacklist:
                        output += '{} '.format(t)
                link = Link(
                    url=url,
                    text=output,
                    raw_html=html,
                    page_title=soup.title.string
                )
                result.append(link)
            except Exception as e:
                print('Got exception')
                print(e)
        return result

    def check_text_for_plagiarism(self, title, text):
        links = self.get_topn_links(title, LINKS_TO_CHECK)
        texts_to_check = [item for item in map(
            lambda l: l.text, links
        )]
        # in order to get similarity to first text insert it here
        texts_to_check.insert(0, text)
        plagirism_coefs_array = get_cosine_sim(texts_to_check)[0]
        texts_to_check = texts_to_check[1:]
        plagirism_coefs_array = plagirism_coefs_array[1:]

        return [{
            'url': links[i].url,
            'text': v,
            'title': links[i].page_title,
            'plagiarism_coef': plagirism_coefs_array[i]
        } for i, v in enumerate(texts_to_check) if plagirism_coefs_array[i] >= 0.2]
