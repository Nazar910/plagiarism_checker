import pdb

def jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    pdb.set_trace()
    return float(len(c)) / (len(a) + len(b) - len(c))

print(jaccard_sim(
    'AI is our friend and it has been friendly',
    'AI and humans have always been friendly'
))
