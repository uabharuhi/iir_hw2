from article import PubMedArticle,TwitterArticle
import json
class ParserFactory():
  def __init__(self):
    pass

  def createParseFunction(self,filetype):
    def parseTwitter(text):
      article = TwitterArticle()

      return article
    def parsePubmedJson(text):
      article = PubMedArticle()
      obj = json.loads(text, encoding="utf-8")
      article.setTitle(obj['title'])
      for text in obj['texts']:
        article.add_abstract_text(text)
      return article

    if filetype == "pubmed":
      return parsePubmedJson
    elif filetype == "twitter":
      return parseTwitter

    return None
