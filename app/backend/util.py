from collections import Counter
import matplotlib.pyplot as plt
from  backend import textloader as tl
from  backend  import parse
from  backend import tokenizer as tk
from  backend  import indexer as idx
from  backend  import  ir
import re
#一篇文章先用part 隔開 一個part是一堆垃圾或是token隔開後每一個字都給一個index
#
#pos就是那些被認為和token同樣的word的index
#可能出現在titile或文章內


#返回  1 一堆tilte part組成的 list, 2 list of list of part in abstract_texts
#          2  標記: 每一個part的標記 -1代表不是token 1代表這個part是token 1 ...
def find_token_pos_in_pubmed_article(tokens,article):
    pat = re.compile(r'([0-9a-zA-Z\-]+)|([^0-9^a-z^A-Z^\-]+)')

    title = article.getTitle()
    abstract_texts = article.abstract_text
    abstract_parts_group = []

    for abstract  in abstract_texts:
        part_group = find_partgroup_in_string(pat,abstract,tokens,article.tokenizer)
        abstract_parts_group.append(part_group)

    title_parts_group = find_partgroup_in_string(pat,title,tokens,article.tokenizer)

    return title_parts_group,abstract_parts_group

def find_token_pos_in_twitter_article(tokens, article):
    pat = re.compile(r'([0-9a-zA-Z\-]+)|([^0-9^a-z^A-Z^\-]+)')
    text_part_group = find_partgroup_in_string(pat,article.text,tokens,article.tokenizer)
    return  text_part_group

def find_partgroup_in_string(pat,s,tokens,tokenizer):
    part_group = []
    for m in re.finditer(pat,s):
        if m.group(1) is not None:
            _l = tokenizer.tokenize(m.group(1)) #check the group after tokenizer is the sane as token
            assert len(_l)==1
            token_number = -1
            for i,token in enumerate(tokens):
                if token == _l[0]:
                    token_number = i
                    break
            part_group.append((token_number, m.group(1)))
        else :
            assert m.group(2) is not None
            part_group.append((-1,m.group(2)))
    return part_group

def build_corpus_and_indexer(cp_name,corpus_path,tokenizer):
    loader = tl.TextLoader()
    corpus = loader.load_corpus_from_directory(cp_name,corpus_path)
    factory = parse.ParserFactory()
    corpus.parseAll(factory)
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
    for path, articles in corpus.articles.items():
        if type(articles) is list:
            for a in articles:
                zipf.add_tokens(a.getTokens())
        else :
            zipf.add_tokens(articles.getTokens())
    zipf.save_dist_figure(title,save_path)



def most_near_token(corpus,token,near_func=minEditDist):
    vocab = list(corpus.vocab)
    token_dist = [ (vocab_token,near_func(vocab_token, token)) for vocab_token in vocab]
    token_dist = sorted(token_dist, key=lambda x: (x[1]))
    return token_dist[0]
#return   tuple(token,distance)
def most_near_token_in_vocab(vocab,token,near_func=minEditDist):
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
        #print(rank[-1:-1-20:-1])
        plt.xlabel('rank')
        plt.ylabel('frequency')
        plt.title(title)
        plt.plot(list(range(len(rank))),freq)
        plt.savefig(save_path)
        plt.close()
        self.display_first_k(10)
    def display_first_k(self,k=10):
        print(self.counter.most_common(k))

    def getDist(self):
        return self.counter.most_common()
    # def token_histogram(tokens):
    #     c = Counter(tokens)
    #     return c.most_common()
