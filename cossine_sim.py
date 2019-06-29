from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_cosine_sim(*strs):
    vectors = [t for t in get_vectors(*strs)]
    print(vectors)
    return cosine_similarity(vectors)

def get_vectors(*strs):
    text = [t for t in strs]
    vectorizer = CountVectorizer(text)
    vectorizer.fit(text)
    return vectorizer.transform(text).toarray()

print(get_cosine_sim(
    'AI is our friend and it has been friendly',
    'AI and humans have always been friendly',
    'AI is not a human'
))
