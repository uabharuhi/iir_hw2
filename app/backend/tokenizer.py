from nltk import PorterStemmer
import re
from nltk.corpus import stopwords
#stop=[]
stop = set(stopwords.words('english'))


class SpaceTokenizer():
  def __init__(self):
    pass

  def get_name(self):
    return 'normal'
      
  def tokenize(self,text):
    text = re.sub('[^0-9a-zA-Z\-]+', ' ', text)
    tokens = text.lower().split()
    tokens = [token for token in tokens if token  not in stop and len(token)>1]
    return tokens

class PorterTokenizer():
    def __init__(self):
        pass

    def get_name(self):
        return 'porter'

    def tokenize(self,text):
        text = re.sub('[^0-9a-zA-Z\-]+', ' ', text)
        tokens = text.lower().split()
        stemmer = PorterStemmer()
        tokens =  [stemmer.stem(token) for token in  tokens if token not in stop and len(token)>1]
        return tokens


