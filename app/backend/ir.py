import os
import util
class IRSystem():
    def __init__(self):
        self.corpus_list = []
        self.corpus_names = {} # key is category ,value is name
        self.get_corpus_names()
        self.queryers = {}  # key is corpus name ,value is queryer
        self.initilize_queryer()

    def get_corpus_names(self):
        root =  os.path.join(os.path.join(os.path.dirname(__file__),'data'))
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
        self.corpus_names = corpus_names

   #build_corpus_and_indexer(cp_name, corpus_path, tokenizer):

    def initilize_queryer(self):
        for corpus_name in self.corpus_names:
            pass
            #_,index
            #self.queryers[corpus_name] =


    #def make_query(self,query,top_k=10):