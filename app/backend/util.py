from collections import Counter
import matplotlib.pyplot as plt
from  backend import textloader as tl
from  backend  import parse
from  backend import tokenizer as tk
from  backend  import indexer as idx
from  backend  import  ir
import re
import _pickle as  pickle 
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

def get_top_down_random_words(zipf, k=10):
    import random

    x = zipf.getDist()
    rank, freq = zip(*x)
    random_idx = random.sample(list(range(len(freq))), k)
    random_idx.sort()

    top_words, top_freqs = rank[0:k], freq[0:k]
    down_words, down_freqs = rank[-1:-k:-1], freq[-1:-k:-1]
    random_words = []

    for i in random_idx:
        random_words.append(rank[i])

    random_freqs = []
    for i in random_idx:
        random_freqs.append(freq[i])

    return top_words, down_words, random_words, top_freqs, down_freqs, random_freqs, random_idx


def find_partgroup_in_string(pat,s,tokens,tokenizer):
    #print(tokenizer)
    part_group = []
    for m in re.finditer(pat,s):
        if m.group(1) is not None:
            _l = tokenizer.tokenize(m.group(1)) 
            #check the group after tokenizer is the sane as token
            #不會成立 因為有做stopwords...  所以tokenize之後可能是
            if len(_l)<1:
                part_group.append((-1, m.group(1)))
                continue

            assert len(_l)<2

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
    print('#############################')
    print(cp_name)
    loader = tl.TextLoader()
    corpus = loader.load_corpus_from_directory(cp_name,corpus_path)
    factory = parse.ParserFactory()
    corpus.parseAll(factory)
    corpus.tokenizeAll(tokenizer)
    corpus.build_vocab()
    print('end1')
    indexer = idx.Indexer(corpus)
    print('end2')
    return corpus,indexer


def get_indxer_pkl_dirpath(cpname,tokenizer_name,filename):
    return './temp/%s/%s/%s.pkl'%(cpname,tokenizer_name,filename)

def dump_corpus_and_indexer(prefix,cpname,tokenizer):
    print('cpname')
    print(cpname)
    corpus_names=create_corpus_names()
    corpus,indexer = None,None
    for cat,corpus_names in corpus_names.items():
        for corpus_name in corpus_names:
            print(corpus_name)
            flag = False
            if cpname == corpus_name:
                corpus_path =   os.path.join(get_app_root(),corpus_name)
                corpus,indexer = build_corpus_and_indexer(corpus_name,corpus_path,tokenizer)
                flag =True
        if flag:
            break

    indexer.dump_index_corpus(prefix)
            

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
    zipf.add_corpus(corpus)
    zipf.save_dist_figure(title,save_path)

def top_n_relevant_articles(corpus,n):
    import datetime,queue,os

    q = queue.PriorityQueue()
    article_list =[]
    for path,articles in corpus.articles.items():
        if type(articles) is list:
            article_list.extend(articles)
        else:
            article_list.append(articles)

    for article in article_list:
        if article.getType() == 'pubmed':
            order =  int(os.path.basename(article.path).split(".")[0])
            q.put((order,article), False)
        elif article.getType() == 'twitter':
            date = datetime.datetime.strptime(article.date,"%Y/%m/%d %H:%M")
            q.put((-1*date.timestamp(),article),False)

    ret_articles = []
    for i in range(min(n,len(article_list))):
        _,article = q.get(False)
        #if article.getType() == 'twitter':
        #    print(article.date)
        #    print(article.getTitle())
        #else:
        #    print(article.path)
        #    print(article.getTitle())
        ret_articles.append(article)

    return ret_articles

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

    def add_corpus(self,corpus):
        for path, articles in corpus.articles.items():
            if type(articles) is list:
                for a in articles:
                    self.add_tokens(a.getTokens())
            else:
                self.add_tokens(articles.getTokens())

    def add_articles(self,articles):
        for  article in articles:
            self.add_tokens(article.getTokens())


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


import os

def get_app_root():
    root =   os.path.join(os.path.join(os.path.dirname(__file__), 'data'))
    return root

def create_corpus_names():
    root = get_app_root()
    corpus_category_paths = [os.path.join(root,path) for path in os.listdir(root)]
    print(corpus_category_paths)
    corpus_names = {}
    for category_path in corpus_category_paths:
        print(category_path)
        corpus_topic_paths = [os.path.join(category_path,path) for path in os.listdir(category_path)]
        corpus_names[os.path.basename(category_path)] = []
        for  topic_path in  corpus_topic_paths:
            print(topic_path)
            category_name = os.path.basename(category_path)
            topic_name =  os.path.basename(topic_path)
            corpus_names[category_name].append(os.path.join(category_name,topic_name))
    corpus_names = corpus_names
    return corpus_names

