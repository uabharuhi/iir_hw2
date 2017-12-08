from backend.article import PubMedArticle,TwitterArticle
import json
class ParserFactory():
  def __init__(self):
    pass

  def createParseFunction(self,filetype):
    def parseTwitter(text):
      articles = []
      l = json.loads(text)
      for article_json in l:
        article = TwitterArticle()
        article.init_by_json(article_json)
        
        if not article.isEmpty():
          articles.append(article)
      return articles

    def parsePubmedJson(text):

      article = PubMedArticle('') # dummy path first
      try:
        obj = json.loads(text, encoding="utf-8")
      except :
        return None
        
      article.setTitle(obj['title'])
      for text in obj['texts']:
        article.add_abstract_text(text)
      return article

    if filetype == "pubmed":
      return parsePubmedJson
    elif filetype == "twitter":
      return parseTwitter

    return None
