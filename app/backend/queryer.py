from  backend  import util
from collections import Counter
class Queryer():
    def __init__(self,indexer):
        self.indexer  = indexer

    def spell_check(self,token,tolerance):
        ans = util.most_near_token(self.indexer.corpus, token)
        if ans[1] <= tolerance:
            return ans[0]
        return None

    #query a token --> return files which contain that token
    # error rate for tolerance , longer string can spell wrong more
    def query_files_by_token(self,tokens,error_rate=0.2,flag_spell_check=True):
        if flag_spell_check:
            tolerance = max(int(len(tokens)*error_rate),1)
            tokens = self.spell_check(tokens, tolerance)

        if tokens is None:
            return [],[]

        files = self.indexer.search_files_by_index(tokens)

        return files,tokens


    def get_spellchecked_tokens(self,sentence,tokenizer,error_rate=0.2):
        tokens = tokenizer.tokenize(sentence)
        return [  self.spell_check(token,max(int(len(token)*error_rate),1)) for token in tokens]

    def  query_files_by_sentence(self,sentence,tokenizer,error_rate=0.2,flag_spell_check=True):
        tokens = tokenizer.tokenize(sentence)
        results = set([]) 
        for token in tokens:
            (filenames,_) = self.query_files_by_token(token, error_rate, flag_spell_check)
            results = results|set(filenames)
        return list(results),tokens


    '''
    def count_matches(self,tokens):
        corpus = self.indexer.corpus
        articles = corpus.articles
        match_times = {} # key is article tilte  , value is match times
        match_detail  = {} # key is token name , value is  {tiltle:tolen_math_times in article with title}

        for article in articles:
            match_times[article.getTitle()] = 0
        print(tokens)
        for token in list(set(tokens)):
            print('!!!')
            print(token)
            detail_dict = {}
            match_detail[token] = detail_dict
            for article in articles:
                counter =  Counter( article.getTokens())
                occur_times = counter[token]
                detail_dict[article.getTitle()] = occur_times
                match_times[article.getTitle()]+= occur_times

        return match_detail,match_times
'''
