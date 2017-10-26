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
      article = func(text)
      self.articles[path] = article


  def tokenizeAll(self,tokenizer):
    for path,article in self.articles.items():
      article.tokenize(tokenizer)

  def build_vocab(self):
      self.vocab = set()
      for path, article in self.articles.items():
        self.vocab = self.vocab |set(article.getTokens())






