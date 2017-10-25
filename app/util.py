from collections import Counter
def token_histogram(tokens):
    c = Counter(tokens)
    return c.most_common()   

