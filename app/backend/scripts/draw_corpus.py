import argparse
import os
from inspect import getsourcefile
import sys
current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
parent_dir  = parent_dir[:parent_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)
print(sys.path[0])
from backend import util
from backend import tokenizer as tk
import re

parser = argparse.ArgumentParser()
parser.add_argument("corpus", help="corpus name")
args = parser.parse_args()

#corpus name example pubmed/gene

f = lambda _path: re.compile(r"[\\\/]").split(_path)

corpus_name = args.corpus
corpus_path = os.path.join('./data',corpus_name)
corpus,indexer = util.build_corpus_and_indexer(corpus_name,corpus_path,tk.SpaceTokenizer())




save_path_root = '../main/static'
figure_dir = os.path.join(save_path_root ,corpus_name)
save_path = os.path.join(save_path_root ,corpus_name,'%s.png'%(f(corpus_name)[1]))
#print(figure_dir)
if  not os.path.isdir(figure_dir):
    #print('figures')
    #print(figure_dir)
    os.makedirs(figure_dir)
util.save_dist_figure(corpus,corpus_name,save_path)



corpus,indexer = util.build_corpus_and_indexer(corpus_name,corpus_path,tk.PorterTokenizer())

save_path = os.path.join(save_path_root ,corpus_name,'%s_porter.png'%(f(corpus_name)[1]))
util.save_dist_figure(corpus,corpus_name+" porter",save_path)
