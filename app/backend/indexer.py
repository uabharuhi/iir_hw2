class Indexer():
    def __init__(self,corpus):
        self.corpus = corpus
        self.__build_index()
    def  __build_index(self):
        # key is token , value is list of file path
        self.index_dict = {}
        l = list(self.corpus.vocab)
        for  token in l:
            self.index_dict[token] = []
            paths  = [(path,articles) for path,articles in self.corpus.articles.items()]
            for path,articles in paths:
                if type(articles) is  list:
                    for article in articles:
                        self.index_dict[token].append(path)
                else:
                    self.index_dict[token].append(path)

        # for token in list(self.index_dict.keys())[0:10]:
        #     print('token')
        #     print(token)
        #     print('in files')
        #     print(self.index_dict[token])
    def search_files_by_index(self,token):
        return self.index_dict.setdefault(token,[])

    