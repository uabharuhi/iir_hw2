from collections import Counter
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

def minEditDist(sm,sn):
  m,n = len(sm),len(sn)
  f = (lambda: 0 if sm[i-1] == sn[j-1] else 2)
  D = list(map(lambda y: list(map(lambda x,y : y if x==0 else x if y==0 else 0,
    range(n+1),[y]*(n+1))), range(m+1)))
  for i in range(1,m+1):
    for j in range(1,n+1):
      D[i][j] = min( D[i-1][j]+1, D[i][j-1]+1, 
        D[i-1][j-1] + f())
  return D[m][n] 

def zip_dist_corpus(corpus,title):
    zipf = Zipf()
    for path, article in corpus.articles.items():
        zipf.add_tokens(article.getTokens())
    #zipf.draw_picture(title)
    zipf.display_first_k()


def most_near_token(corpus,token,near_func=minEditDist):
    vocab = list(corpus.vocab)
    token_dist = [ (vocab_token,near_func(vocab_token, token)) for vocab_token in vocab]
    token_dist = sorted(token_dist, key=lambda x: (x[1]))
    return token_dist[0]



class Zipf():
    def __init__(self):
        self.counter = Counter()

    def add_tokens(self,tokens):
        c = Counter(tokens)
        self.counter+=c

    def draw_picture(self,title):

        x = self.getDist()
        plt.plot()
        #print(x)
        rank, freq = zip(*x)
        #freq = (6,7,8,4,2)
        #print(freq)        # the histogram of the data
        #n, bins, patches = plt.hist(freq, len(freq),density=False,facecolor='blue')
        plt.xlabel('rank')
        plt.ylabel('frequency')
        plt.title(title)
        plt.plot(list(range(len(rank))),freq)
        #plt.title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
        #plt.axis([40, 160, 0, 0.03])
        #plt.grid(True)
        plt.show()

    def display_first_k(self,k=10):
        print(self.counter.most_common(k))

    def getDist(self):
        return self.counter.most_common()
    # def token_histogram(tokens):
    #     c = Counter(tokens)
    #     return c.most_common()

