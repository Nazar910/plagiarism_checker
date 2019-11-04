import operator
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_topn_words(text, n):
    vectorizer = CountVectorizer()
    vectorizer.fit([text])
    feature_names = vectorizer.get_feature_names()
    vector = vectorizer.transform([text]).toarray()[0]
    result = []
    word_map = {v: vector[k] for k, v in enumerate(feature_names)}
    for _ in range(n):
        the_most_common_word = max(word_map.items(), key=operator.itemgetter(1))[0]
        result.append(the_most_common_word)
        del word_map[the_most_common_word]
    return result

def get_cosine_sim(strs):
    vectors = [t for t in get_vectors(strs)]
    return cosine_similarity(vectors)

def get_vectors(strs):
    vectorizer = CountVectorizer(ngram_range=(1, 3))
    return vectorizer.fit_transform(strs).toarray()
