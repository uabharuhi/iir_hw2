from backend import util,corpus
from  backend import tokenizer as tk
import wikipedia
class WikiAnalizer():
    def __init__(self,topic):
        self.topic = topic
        self.text =  wikipedia.page(topic).content
        self.analyze()

    def analyze(self,tokenizer=tk.SpaceTokenizer()):
        self.zipf = util.Zipf()
        self.zipf.add_tokens(tokenizer.tokenize(self.text))



