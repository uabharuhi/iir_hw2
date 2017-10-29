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
    self.text = ""

  def getType(self):
    return 'twitter'

  def setText(self,text):
    self.text = text
  def remove_url(self):
    pass
  def tokenize(self,tokenizer):
    pass
  def getTitle(self):
    return ""
  def getTokens(self):
    return ['1']