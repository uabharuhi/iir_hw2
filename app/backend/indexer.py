import _pickle as pickle
class Indexer():
    def __init__(self,corpus=None,load_from_pkl=False,pkl_dirpath=None):
        if load_from_pkl:
            self.load_index(pkl_dirpath)
        else:
            assert corpus is not None
            self.corpus = corpus
            self.__build_index()

    def  __build_index(self):
        # key is token , value is list of file path
        print('indexer')
        print(self.corpus.name)
        self.index_dict = {}
        l = list(self.corpus.vocab)
        paths  = [(path,articles) for path,articles in self.corpus.articles.items()]
        print('length')
        print(len(l))
        for  i,token in enumerate(l):
            self.index_dict[token] = []
            for path,articles in paths:
                if type(articles) is  list:
                    for article in articles:
                        if  article.hasToken(token):
                            self.index_dict[token].append(path)
                else:
                    if  articles.hasToken(token):
                        self.index_dict[token].append(path)
            if i%100 ==0:
                print('check')
                print(i)
        print('end')

        # for token in list(self.index_dict.keys())[0:10]:
        #     print('token')
        #     print(token)
        #     print('in files')
        #     print(self.index_dict[token])


    def dump_index_corpus(self,dirpath):
        with open('%s/corpus.pkl'%(dirpath), mode='wb') as f:
            assert self.corpus is not None
            pickle.dump(self.corpus,f)
            
        with open('%s/index.pkl'%(dirpath), mode='wb') as f:
            assert self.index_dict is not None
            pickle.dump(self.index_dict,f)
            

    def load_index_corpus(self,pkl_dirpath):
        with open('%s/corpus.pkl'%(pkl_dirpath), mode='rb') as f:
            self.corpus = pickle.load(f)

        with open('%s/index.pkl'%(pkl_dirpath), mode='rb') as f:
            self.index_dict = pickle.load(f)

    def search_files_by_index(self,token):
        return self.index_dict.setdefault(token,[])

    