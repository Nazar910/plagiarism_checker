import os
import bcrypt
from googlesearch import search
import urllib.request
from inscriptis import get_text

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
    def __init__(self, url, text):
        self.url = url
        self.text = text

class TextService(Service):
    def get_topn_links(self, word, Nlinks):
        result = []
        for url in search(word, stop=Nlinks):
            try:
                html = urllib.request.urlopen(url).read().decode('utf-8')
                link = Link(url, get_text(html))
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

        return [{
            'url': links[i].url,
            'text': v,
            'plagiarism_coef': plagirism_coefs_array[i]
        } for i, v in enumerate(texts_to_check) if plagirism_coefs_array[i] >= 0.5]
