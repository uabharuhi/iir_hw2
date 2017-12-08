import os
from  backend import util,score
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
        self.idf_dict = {}
        self.corpus_names = util.create_corpus_names()

        
        if init_queryer:
            self.initialize_queryer()
            self.build_idf('n')
            self.build_idf('t')
          


    def initialize_queryer(self,load_from_pkl=False):
        #corpus_paths = [ os.path.join(root,corpus_name)   for corpus_name in self.corpus_names]
        for cat,corpus_names in self.corpus_names.items():
            for corpus_name in corpus_names:
                corpus_path =   os.path.join(self.root,corpus_name)

                corpus,indexer = util.build_corpus_and_indexer(corpus_name,corpus_path,self.tokenizer)
                self.queryers[corpus_name] = q.Queryer(indexer)
                self.all_vocab  =  self.all_vocab | corpus.vocab
        self.id2token,self.token2id = util.getLookupTables(self.all_vocab) 

    def all_in_vocab_set(self,tokens):
        for token in tokens:
            if token not in self.all_vocab:
                return  False
        return True


    def get_corpus_by_name(self,name):
        print('IRSys : get_corpus_by_name')
        print(name)
        corpus_list = [queryer.indexer.corpus for  _,queryer in self.queryers.items()]
        print('for corpus in corpus_list:')
        for corpus in corpus_list:
            print(corpus.name)
            if name == corpus.name:
                return corpus
        return None

    def alternative_query(self,query,tokenizer):
        tokens  = tokenizer.tokenize(query)
        alternative_tokens = [util.most_near_token_in_vocab(self.all_vocab, token)[0] for token in tokens]
        return  alternative_tokens

    def make_query_order_by_match_total(self,query,top_k,preview_len=200):
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

    def make_query_order_by_tfidf(self,query,top_k,which_tf='l',which_idf='t',preview_len=200):
        article_corpusname  = {}
        article_match_total = {}
        article_token_matchtimes ={}
      
        import queue
        q = queue.PriorityQueue()
        score_alogorithm = score.ScoreAlgorithm(self.token2id, tf_func=score.get_tf_func(which_tf)\
                            ,idf_func=score.get_idf_func(which_idf))

        query_tfidf =  score_alogorithm .calculateOneWithIdfData(self.idf_dict[which_idf],self.tokenizer.tokenize(query))

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

                article_tfidf = score_alogorithm.calculateOneWithIdfData(self.idf_dict[which_idf],article.getTokens())
                q.put((-1*score.cosine_sim(article_tfidf,query_tfidf),article.getTitle(),content),False)
                
        ret_article_info =[]
        ret_num = min(top_k,q.qsize())
        for i in range(ret_num):
            tfidf,title,abstract = q.get(False)
            if tfidf >0 : #minus
                continue
            if len(abstract)>preview_len:
                abstract = abstract[0:preview_len]
            print('queue')
            print((tfidf,title))
            ret_article_info.append((title,abstract))

        ret_article_titles, ret_article_abstracts = [],[]
        if len(ret_article_info)>0:
            ret_article_titles,ret_article_abstracts =  zip(*ret_article_info)
            ret_article_titles, ret_article_abstracts = list(ret_article_titles), list(ret_article_abstracts)

        k_article_corpusname ={ k:v for k,v in article_corpusname.items() if k in ret_article_titles}
        k_article_match_total = {k: v for k, v in article_match_total.items() if k in ret_article_titles}
        k_article_token_matchtimes = {k: v for k, v in article_token_matchtimes.items() if k in ret_article_titles}

        return  ret_article_titles,ret_article_abstracts,k_article_corpusname,k_article_match_total, k_article_token_matchtimes,tokens



#    def make_query(self,query,top_k=10,preview_len=200,rank_model=''):
#        if rank_model == 'match':
#            ret_article_titles,ret_article_abstracts,k_article_corpusname,k_article_match_total, k_article_token_matchtimes,tokens = self.make_query_order_by_match_total(query,top_k,preview_len)
#        elif  rank_model == 'tfidf':
#            ret_article_titles,ret_article_abstracts,k_article_corpusname,k_article_match_total, k_article_token_matchtimes,tokens = self.make_query_order_by_tfidf(query,top_k,preview_len)
#
#
#
#
#        return  ret_article_titles,ret_article_abstracts,k_article_corpusname,k_article_match_total, k_article_token_matchtimes,tokens



    def count_matches_in_article(self, article, tokens):
        match_times = 0
        match_detail = {}
        for token in list(set(tokens)):
            
            counter = Counter(article.getTokens())
            occur_times = counter[token]
            match_detail[token] = occur_times
            match_times += occur_times

        return match_times,match_detail

    def get_all_article_token_list(self):
        all_article_token_list = []
        title2Document ={}

        corupus_list = [queryer.indexer.corpus for  _,queryer in self.queryers.items()]
        for corpus in corupus_list:
            corpus_documents,corpus_title2Document = corpus.get_all_article_token_list()
            all_article_token_list.extend(corpus_documents)
            title2Document.update(corpus_title2Document) 

        return all_article_token_list,title2Document

    # return article and corpus_name
    def findArticleByTitle(self,article_title):
        corupus_list = [queryer.indexer.corpus for  _,queryer in self.queryers.items()]

        for corpus in corupus_list:
            for path,a in corpus.articles.items():
                if type(a) is list:
                    for  aa in a:
                        if aa.getTitle() == article_title:
                            return aa,corpus.name
                            
                elif a.getTitle() ==  article_title:
                    return  a,corpus.name
        return None

    def build_idf(self,which):
        all_article_token_list,title2Document = self.get_all_article_token_list()
        if which == 'n':
          self.idf_dict[which] = [1 for i  in range(0,len(self.all_vocab)) ]
        elif which == 't':
          self.idf_dict[which] = score.idf_t(all_article_token_list,self.token2id)

    def get_tfidf_of_article_all_corpus(self,title,which_tf='l',which_idf='t'):
 
        all_article_token_list,title2Document = self.get_all_article_token_list()

        if title in title2Document:
            tokens = title2Document[title]
        else:
            assert False
     
        strategy = score.ScoreAlgorithm(self.token2id,score.get_tf_func(which_tf),score.get_idf_func(which_idf))
        
        tfidf_scores = strategy.calculateOneWithIdfData(self.idf_dict[which_idf],tokens)
        return tfidf_scores

    def get_all_articles(self):
        corupus_list = [queryer.indexer.corpus for  _,queryer in self.queryers.items()]
        all_articles = []
        for corpus in corupus_list:
            all_articles.extend(corpus.get_all_articles())
        return all_articles

    def get_tfidf_of_articles(self,which_tf='l',which_idf='t'):
 
      all_article_token_list,title2Document = self.get_all_article_token_list()

      from backend import score
      strategy = score.ScoreAlgorithm(self.token2id,score.get_tf_func(which_tf),score.get_idf_func(which_idf))
      
      title_tfidf_dict = {}

      articles = self.get_all_articles()
      for article in articles:
         title_tfidf_dict[article.getTitle()] = strategy.calculateOneWithIdfData(self.idf_dict[which_idf],article.getTokens())

      return title_tfidf_dict