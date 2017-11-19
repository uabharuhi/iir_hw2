import _pickle as  pickle 
from  backend.ir import  IRSystem
from backend import tokenizer as tk
from backend import util


ir_sys1 = IRSystem(tk.SpaceTokenizer())
ir_sys2 = IRSystem(tk.PorterTokenizer())

def dump_ir_sys(ir_sys,direcroty_layer2):
    print('load')
    print('dump1')
    with open("./temp/%s/ir_sys.pkl"%(direcroty_layer2), mode='wb') as f:
       pickle.dump(ir_sys,f)

    print('dump2')
    with open("./temp/%s/corpus_names.pkl"%(direcroty_layer2), mode='wb') as f:
       pickle.dump(ir_sys.corpus_names,f)

    with open("./temp/%s/corpus.pkl"%(direcroty_layer2), mode='wb') as f:
       corpus_list = [ q.indexer.corpus  for _,q in ir_sys.queryers.items()]
       pickle.dump(corpus_list,f)



dump_ir_sys(ir_sys1, 'normal')
dump_ir_sys(ir_sys2, 'porter')

#with open('./temp/normal/pubmed/gene/indexer.pkl', mode='rb') as f:
#  indexer = pickle.load(f)
#  for path,articles in indexer.corpus.articles.items():
#    if type(articles) is list:
#      for article in articles:
#        print(path)
#        #print(article.getTitle())
#    else:
#        print(path)
#        #print(articles.getTitle())

def dump_by_name(corpus_name,tokenizer):
  path = './temp/%s/%s'%(tokenizer.get_name(),corpus_name)
  util.dump_corpus_and_indexer(path,corpus_name,tokenizer)


