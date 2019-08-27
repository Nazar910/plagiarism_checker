from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import operator

def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    print(vectors)
    return cosine_similarity(vectors)

def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    feature_names = vectorizer.get_feature_names()
    vectors = vectorizer.transform(text).toarray()
    return vectors

def get_topn_words(text, n):
    vectorizer = CountVectorizer()
    vectorizer.fit([text])
    feature_names = vectorizer.get_feature_names()
    print(feature_names)
    vector = vectorizer.transform([text]).toarray()[0]
    result = []
    word_map = {v: vector[k] for k, v in enumerate(feature_names)}
    for _ in range(n):
        the_most_common_word = max(word_map.items(), key=operator.itemgetter(1))[0]
        result.append(the_most_common_word)
        del word_map[the_most_common_word]
    return result

print(get_topn_words('AI and humans have always been friendly with AI AI AI and and have', 3))
