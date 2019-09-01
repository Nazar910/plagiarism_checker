import os
import bcrypt
import re
from googlesearch import search
import urllib.request
from bs4 import BeautifulSoup

from src.utils.text_processor import get_topn_words, get_cosine_sim

TOP_WORDS_COUNT = 2
LINKS_TO_CHECK = 1

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

        self.url = url
        self.text = text
        self.raw_html = raw_html
        self.page_title = page_title

class TextService(Service):
    def get_topn_links(self, word, Nlinks):
        result = []
        for url in search(word, stop=Nlinks):
            try:
                html = urllib.request.urlopen(url).read().decode('utf-8')
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.find_all(text=True)
                output = ''
                blacklist = [
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

                for t in text:
                    if t.parent.name not in blacklist:
                        output += '{} '.format(t)
                link = Link(
                    url=url,
                    text=output,
                    raw_html=html,
                    page_title=soup.title.string
                )
                result.append(link)
            except:
                pass
        return result

    def check_text_for_plagiarism(self, text):
        topN_words = get_topn_words(text, TOP_WORDS_COUNT)
        assert len(topN_words) == TOP_WORDS_COUNT

        links = []
        for w in topN_words:
            links = links + self.get_topn_links(w, LINKS_TO_CHECK)

        texts_to_check = [item for item in map(
            lambda l: l.text, links
        )]
        # in order to get similarity to first text insert it here
        texts_to_check.insert(0, text)
        plagirism_coefs_array = get_cosine_sim(texts_to_check)[0]
        texts_to_check = texts_to_check[1:]
        plagirism_coefs_array = plagirism_coefs_array[1:]

        # soup = BeautifulSoup(html_doc, 'html.parser')
        return [{
            'url': links[i].url,
            'text': v,
            'title': links[i].page_title,
            'plagiarism_coef': plagirism_coefs_array[i]
        } for i, v in enumerate(texts_to_check)]
