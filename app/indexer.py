class Indexer():
    def __init__(self,corpus):
        self.corpus = corpus
        self.__build_index()
    def  __build_index(self):
        # key is token , value is list of file path
        self.index_dict = {}
        l = list(self.corpus.vocab)
        for  token in l:
            self.index_dict[token] = [path for path,article in self.corpus.articles.items() if token in article.getTokens()]
        # for token in list(self.index_dict.keys())[0:10]:
        #     print('token')
        #     print(token)
        #     print('in files')
        #     print(self.index_dict[token])
    def search_files_by_index(self,token):
        return self.index_dict.setdefault(token,[])

    