import os
from  backend import util
from  backend  import tokenizer as tk
from  backend import  queryer as q
from  collections import Counter

class IRSystem():
    def __init__(self,tokenizer,init_queryer=True):
        self.corpus_list = []
        self.corpus_names = {} # key is category ,value is name
        self.queryers = {}  # key is corpus name ,value is queryer
        self.tokenizer = tokenizer
        self.root = os.path.join(os.path.join(os.path.dirname(__file__), 'data'))
        self.all_vocab = set()
        self.corpus_names = util.create_corpus_names()
        
        if init_queryer:
            self.initialize_queryer()


    def initialize_queryer(self,load_from_pkl=False):
        #corpus_paths = [ os.path.join(root,corpus_name)   for corpus_name in self.corpus_names]
        for cat,corpus_names in self.corpus_names.items():
            for corpus_name in corpus_names:
                corpus_path =   os.path.join(self.root,corpus_name)

                corpus,indexer = util.build_corpus_and_indexer(corpus_name,corpus_path,self.tokenizer)
                self.queryers[corpus_name] = q.Queryer(indexer)
                self.all_vocab  =  self.all_vocab | corpus.vocab

    def all_in_vocab_set(self,tokens):
        for token in tokens:
            if token not in self.all_vocab:
                return  False
        return True




    def alternative_query(self,query,tokenizer):
        tokens  = tokenizer.tokenize(query)
        alternative_tokens = [util.most_near_token_in_vocab(self.all_vocab, token)[0] for token in tokens]
        return  alternative_tokens

    def make_query(self,query,top_k=10,preview_len=200):

        article_corpusname  = {}
        article_match_total = {}
        article_token_matchtimes ={}
      
        import queue
        q = queue.PriorityQueue()

        for corpus_name,queryer in self.queryers.items():
            files, tokens = queryer.query_files_by_sentence(query, self.tokenizer, error_rate=0.0, flag_spell_check=False)
            articles = queryer.indexer.corpus.getArticlesByPaths(files)
            for article in articles:
                match_times,match_details = self.count_matches_in_article(article,tokens)
                article_match_total[article.getTitle()] = match_times
                article_corpusname[article.getTitle()] = corpus_name
                article_token_matchtimes[article.getTitle()] = match_details
                if article.getType()=='pubmed':
                    content = article.abstract_text[0]
                elif article.getType()=='twitter':
                    content = article.text
               
                q.put((-1*match_times,article.getTitle(),content),False)
                
        ret_article_info =[]
        ret_num = min(top_k,q.qsize())
        for i in range(ret_num):
            occur,title,abstract = q.get(False)
            if len(abstract)>preview_len:
                abstract = abstract[0:preview_len]
            print('queue')
            print((occur,title))
            ret_article_info.append((title,abstract))

        ret_article_titles, ret_article_abstracts = [],[]
        if len(ret_article_info)>0:
            ret_article_titles,ret_article_abstracts =  zip(*ret_article_info)
            ret_article_titles, ret_article_abstracts = list(ret_article_titles), list(ret_article_abstracts)

        k_article_corpusname ={ k:v for k,v in article_corpusname.items() if k in ret_article_titles}
        k_article_match_total = {k: v for k, v in article_match_total.items() if k in ret_article_titles}
        k_article_token_matchtimes = {k: v for k, v in article_token_matchtimes.items() if k in ret_article_titles}

        return  ret_article_titles,ret_article_abstracts,k_article_corpusname,k_article_match_total, k_article_token_matchtimes,tokens



    def count_matches_in_article(self, article, tokens):
        match_times = 0
        match_detail = {}
        for token in list(set(tokens)):
            
            counter = Counter(article.getTokens())
            occur_times = counter[token]
            match_detail[token] = occur_times
            match_times += occur_times

        return match_times,match_detail