class Corpus():
  def __init__(self,name):
    # raw_text and articles, key is filepath value is content ,,
    self.name = name
    self.raw_texts = {}
    self.articles = {} # article , high level and encapsulation of raw_texts

  def add_raw_text(self,path,text):
    #print("adding %s ..."%(path))
    self.raw_texts[path] = text

  def parseAll(self,parserFactory):
    import re
    uppath = lambda _path, n: re.compile(r"[\\\/]").split(_path)[-1:-1-n:-1][-1]
    for path,text in self.raw_texts.items():
      filetype = uppath(path,3)
      func = parserFactory.createParseFunction(filetype)
      #print(text)
      #print(path)
      if 'twitter' == filetype:
        articles =  func(text)
        self.articles[path] = articles
      elif 'pubmed' == filetype:
       article = func(text)
       self.articles[path] = article
      else:
        assert  False
  # pat
  # def operate_on_article(self,path,func):
  #   if type(self.articles[path]) is list:  # twitter file
  #     for article in self.articles[path]:
  #       func(article)
  #   else:
  #     func(self.articles[path])


  def getArticlesByPaths(self,files) :
    l = []
    for path in files:
      if type(self.articles[path]) is list: # twitter file
        for article in self.articles[path]:
          l.append(article)
      else:
        l.append(self.articles[path])
    return l

  def tokenizeAll(self,tokenizer):
    for path in self.articles:
      if type(self.articles[path]) is list: # twitter file
        for article in self.articles[path]:
          article.tokenize(tokenizer)
      else:
        self.articles[path].tokenize(tokenizer)


  def build_vocab(self):
      self.vocab = set()
      for path in self.articles:
        if type(self.articles[path]) is list:  # twitter file
          for article in self.articles[path]:
            self.vocab = self.vocab | set(article.getTokens())
        else:
          self.vocab = self.vocab | set(self.articles[path].getTokens())







