from nltk import PorterStemmer
import re


class SpaceTokenizer():
  def __init__(self):
    pass

  def tokenize(self,text):
    text = re.sub('[^0-9a-zA-Z\-]+', ' ', text)
    tokens = text.lower().split()
    return tokens

class PorterTokenizer():
    def __init__(self):
        pass
    def tokenize(self,text):
        text = re.sub('[^0-9a-zA-Z\-]+', ' ', text)
        tokens = text.lower().split()
        stemmer = PorterStemmer()
        tokens =  [stemmer.stem(token) for token in  tokens]
        return tokens


