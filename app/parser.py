def ParserFactory():
  def __init__(self):
    pass

  def createParseFunction(self,filetype):
    def parseTwitter(text):
      article = TwitterArticle()
      return article
    def parsePubmedJson(text):
      article = PubMedArticle()
      return article

    if filetype == "pubmed":
      return parsePubmedJson
    elif filetype == "twitter":
      return parseTwitter

    return None
