class Corpus():
  def __init__(self,name):
    # raw_text and articles, key is filepath value is content ,,
    self.name = name
    self.raw_texts = {}
    self.articles = {} # article , high level and encapsulation of raw_texts
    self.vocab = None
    self.idf_dict = {} #{'n':,'t'}

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
        if  articles is not None:
          self.articles[path] = articles
      elif 'pubmed' == filetype:
        articles = func(text)
        if articles is not None:
          articles.setPath(path)
          self.articles[path] = articles
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
      self.build_idf('n')
      self.build_idf('t')


  def build_idf(self,which):
    from backend import score,util

    self.id2token,self.token2id = util.getLookupTables(self.vocab) 
    all_article_token_list,title2Document = self.get_all_article_token_list()
    if which == 'n':
      self.idf_dict[which] = [1 for i  in range(0,len(self.vocab)) ]
    elif which == 't':
      self.idf_dict[which] = score.idf_t(all_article_token_list,self.token2id)
   
  def get_idf(self,which):
    if which in self.idf_dict:
      return self.idf_dict[which]
    return None

  def get_all_articles(self):
    articles = []
    for path,a in self.articles.items():
      if type(a) is list:
        for  aa in a:
          articles.append(aa)
      else:
         articles.append(a)
    return articles

  def get_all_article_token_list(self):
    title2Document = {}
    all_article_token_list = []
    for path,a in self.articles.items():
      if type(a) is list:
        for  aa in a:
          tokens = aa.getTokens()
          title2Document[aa.getTitle()] =  tokens
          all_article_token_list.append( tokens)
      else:
        tokens = a.getTokens()
        title2Document[a.getTitle()] =  tokens
        all_article_token_list.append(tokens)
    return all_article_token_list,title2Document

  def get_tfidf_of_articles(self,which_tf='l',which_idf='t'):
 
      all_article_token_list,title2Document = self.get_all_article_token_list()

      from backend import score
      strategy = score.ScoreAlgorithm(self.token2id,score.get_tf_func(which_tf),score.get_idf_func(which_idf))
      
      title_tfidf_dict = {}

      articles = self.get_all_articles()
      for article in articles:
         title_tfidf_dict[article.getTitle()] = strategy.calculateOneWithIdfData(self.idf_dict[which_idf],article.getTokens())

      return title_tfidf_dict







