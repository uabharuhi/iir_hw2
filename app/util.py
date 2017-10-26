from collections import Counter
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def zip_dist_corpus(corpus,title):
    zipf = Zipf()
    for path, article in corpus.articles.items():
        zipf.add_tokens(article.getTokens())
    zipf.draw_picture(title)

class Zipf():
    def __init__(self):
        self.counter = Counter()

    def add_tokens(self,tokens):
        c = Counter(tokens)
        self.counter+=c

    def draw_picture(self,title):

        x = self.getDist()
        rank, freq = zip(*x)
        # the histogram of the data
        n, bins, patches = plt.hist(freq, len(freq), facecolor='blue')
        plt.xlabel('rank')
        plt.ylabel('frequency')
        plt.title(title)
        #plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
        #plt.axis([40, 160, 0, 0.03])
        #plt.grid(True)
        plt.show()

    def getDist(self):
        return self.counter.most_common()
    # def token_histogram(tokens):
    #     c = Counter(tokens)
    #     return c.most_common()

