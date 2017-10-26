from collections import Counter
import numpy as np

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import textloader as tl
import parse
import tokenizer as tk
import indexer as idx



def build_corpus_and_indexer(cp_name,corpus_path,tokenizer):
    loader = tl.TextLoader()
    corpus = loader.load_corpus_from_directory(cp_name,corpus_path)
    factory = parse.ParserFactory()
    corpus.parseAll(factory)
    tokenizer = tk.SpaceTokenizer()
    corpus.tokenizeAll(tokenizer)
    corpus.build_vocab()
    indexer = idx.Indexer(corpus)
    return corpus,indexer

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

def save_dist_figure(corpus,title,save_path):
    zipf = Zipf()
    for path, article in corpus.articles.items():
        zipf.add_tokens(article.getTokens())
    zipf.save_dist_figure(title,save_path)



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

    def save_dist_figure(self,title,save_path):
        #matplotlib.use('Agg')
        x = self.getDist()
        plt.plot()
        rank, freq = zip(*x)
        plt.xlabel('rank')
        plt.ylabel('frequency')
        plt.title(title)
        plt.plot(list(range(len(rank))),freq)
        plt.savefig(save_path)

    def display_first_k(self,k=10):
        print(self.counter.most_common(k))

    def getDist(self):
        return self.counter.most_common()
    # def token_histogram(tokens):
    #     c = Counter(tokens)
    #     return c.most_common()

