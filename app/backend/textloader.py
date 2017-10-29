from  backend  import corpus as cp
import os
import glob
class TextLoader():
  def __init__(self):
    pass

  def load_corpus_from_directory(self,cp_name,dirpath):
    corpus  = cp.Corpus(cp_name)

    for filepath in glob.glob(os.path.join(dirpath, '*')):

        self.add_file2corpus(filepath,corpus)
    return corpus

  def add_file2corpus(self,corpus_path,corpus):

    with open(corpus_path,"r",encoding="utf-8") as f:
        corpus.add_raw_text(corpus_path,f.read())




