import _pickle as  pickle
from  backend.ir import  IRSystem
print('load')
ir_sys = IRSystem()
print('dump1')
with open("./temp/ir_sys.pkl", mode='wb') as f:
   pickle.dump(ir_sys,f)
print('dump2')
with open("./temp/corpus_names.pkl", mode='wb') as f:
   pickle.dump(ir_sys.corpus_names,f)

with open("./temp/corpus.pkl", mode='wb') as f:
   corpus_list = [ q.indexer.corpus  for _,q in ir_sys.queryers.items()]
   pickle.dump(corpus_list,f)

