from nltk import PorterStemmer

class SpaceTokenizer():
  def __init__(self):
    pass

  def tokenize(self,text):
    tokens = text.lower().split()
    return tokens

class PorterTokenizer():
    def __init__(self):
        pass
    def tokenize(self,text):
        tokens = text.lower().split()
        stemmer = PorterStemmer()
        tokens =  [stemmer.stem(token) for token in  tokens]

