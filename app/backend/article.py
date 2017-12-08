class PubMedArticle():
  def __init__(self,path):
    self.path = ''
    self.title = ""
    self.abstract_text = []
    self.tokens = None
    self.tokenizer = None
    self.token_set =None

  def setTitle(self,title):
    self.title = title
  def add_abstract_text(self,text):
    self.abstract_text.append(text)

  def setPath(self,path):
    self.path = path

  def getTitle(self):
    return self.title

  def getType(self):
    return 'pubmed'

  def getTokens(self):
    return self.tokens

  def hasToken(self,token):
      return  token in self.token_set 

  def tokenize(self,tokenizer):
    self.tokenizer = tokenizer

    self.tokens = []
    self.tokens += tokenizer.tokenize(self.title)
    for text in self.abstract_text:
      self.tokens+= tokenizer.tokenize(text)

    self.token_set = set(self.tokens)

  def show(self):
    print("title:")
    print(self.title)
    print('content ')
    for text in self.abstract_text:
      print(text)
      print('- '*50)
    print(self.abstract_text)

  def isEmpty(self):
    for text in  self.abstract_text:
      if len(text)>0:
        return False
    return True


class TwitterArticle():
  def __init__(self):
    self.username =""
    self.date = ""
    self.text = ""
    self.tokens = []
    self.tokenizer = None
    self.token_set =None

  def init_by_json(self,json_obj):
    self.username = json_obj['username']
    self.text = str(json_obj['text']) #有些情況會只有數字?
    self.date = json_obj['date']
    #self.remove_url()

  def getType(self):
    return 'twitter'

  def remove_url(self):
    pass
    # import re
    # pat = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    # selfself.text.replace()

  def tokenize (self,tokenizer):

    self.tokenizer = tokenizer
     # remove url ....
    import re

    textForTokenize = re.sub('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})'
     ,'',self.text)
    #textForTokenize = self.text
  
    self.tokens = tokenizer.tokenize(textForTokenize)
    self.token_set = set(self.tokens)

  def hasToken(self,token):
      return  token in self.token_set 

  def getTitle(self): #for display on web
    return self.username+" "+self.date.replace('/','-')

  def getTokens(self):
    return self.tokens

  #當時間一樣的時候要比較

  def __lt__(self, other):
    return len(self.text)<len(other.text)

  def isEmpty(self):
    return len(self.text)==0