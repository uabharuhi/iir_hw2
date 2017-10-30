class PubMedArticle():
  def __init__(self):
    self.title = ""
    self.abstract_text = []
    self.tokens = None
    self.tokenizer = None

  def setTitle(self,title):
    self.title = title
  def add_abstract_text(self,text):
    self.abstract_text.append(text)

  def getTitle(self):
    return self.title

  def getType(self):
    return 'pubmed'

  def getTokens(self):
    return self.tokens

  def tokenize(self,tokenizer):
    self.tokenizer = tokenizer

    self.tokens = []
    self.tokens += tokenizer.tokenize(self.title)
    for text in self.abstract_text:
      self.tokens+= tokenizer.tokenize(text)

  def show(self):
    print("title:")
    print(self.title)
    print('content ')
    for text in self.abstract_text:
      print(text)
      print('- '*50)
    print(self.abstract_text)


class TwitterArticle():
  def __init__(self):
    self.username =""
    self.date = ""
    self.text = ""
    self.tokens = []
    self.tokenizer = None

  def init_by_json(self,json_obj):
    self.username = json_obj['username']
    self.text = json_obj['text']
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
    self.tokens = tokenizer.tokenize(self.text)


  def getTitle(self): #for display on web
    return self.username+" "+self.date.replace('/','-')

  def getTokens(self):
    return self.tokens