import os
from  backend import util
from  backend  import tokenizer as tk
from  backend import  queryer as q
from  collections import Counter

class IRSystem():
    def __init__(self):
        self.corpus_list = []
        self.corpus_names = {} # key is category ,value is name
        self.queryers = {}  # key is corpus name ,value is queryer
        self.tokenizer = tk.SpaceTokenizer()
        self.root = os.path.join(os.path.join(os.path.dirname(__file__), 'data'))

        self.create_corpus_names()
        self.initilize_queryer()


    def create_corpus_names(self):
        corpus_category_paths = [os.path.join(self.root,path) for path in os.listdir(self.root)]
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
        self.corpus_names = corpus_names


   #build_corpus_and_indexer(cp_name, corpus_path, tokenizer):

    def initilize_queryer(self):
        #corpus_paths = [ os.path.join(root,corpus_name)   for corpus_name in self.corpus_names]
        for cat,corpus_names in self.corpus_names.items():
            for corpus_name in corpus_names:
                corpus_path =   os.path.join(self.root,corpus_name)
                _,indexer = util.build_corpus_and_indexer(corpus_name,corpus_path,self.tokenizer)
                self.queryers[corpus_name] = q.Queryer(indexer)




    def make_query(self,query,top_k=10):

        article_corpusname  = {}
        article_match_total = {}
        article_token_matchtimes ={}
        occur_pos = {} #key is  token ,value is the pos occur in the origin text
        import queue
        q = queue.PriorityQueue()
        for corpus_name,queryer in self.queryers.items():
            files, tokens = queryer.query_files_by_sentence(query, self.tokenizer, error_rate=0.0, flag_spell_check=False)
            articles =  [queryer.indexer.corpus.articles[path] for path in files]
            for article in articles:
                match_times,match_details = self.count_matches_in_article(article,tokens)
                article_match_total[article.getTitle()] = match_times
                article_corpusname[article.getTitle()] = corpus_name
                article_token_matchtimes[article.getTitle()] = match_details
                q.put((-1*match_times,article.getTitle()),False)
        ret_article_titles =[]
        ret_num = min(top_k,q.qsize())
        for i in range(ret_num):
            title = q.get(False)[1]
            ret_article_titles.append(title)
        print(ret_article_titles)

        k_article_corpusname ={ k:v for k,v in article_corpusname.items() if k in ret_article_titles}
        k_article_match_total = {k: v for k, v in article_match_total.items() if k in ret_article_titles}
        k_article_token_matchtimes = {k: v for k, v in article_token_matchtimes.items() if k in ret_article_titles}

        return  k_article_corpusname,k_article_match_total, k_article_token_matchtimes,tokens



    def count_matches_in_article(self, article, tokens):
        match_times = 0
        match_detail = {}
        for token in list(set(tokens)):
            #print(token)
            counter = Counter(article.getTokens())
            occur_times = counter[token]
            match_detail[token] = occur_times
            match_times += occur_times

        return match_times,match_detail