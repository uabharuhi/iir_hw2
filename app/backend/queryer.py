import util
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
    def query_files_by_token(self,token,error_rate=0.2,flag_spell_check=True):
        if flag_spell_check:
            tolerance = max(int(len(token)*error_rate),1)
            token = self.spell_check(token, tolerance)

        if token is None:
            return []
        print('ya .....')
        print(token)
        files = self.indexer.search_files_by_index(token)

        return files


    def get_spellchecked_tokens(self,sentence,tokenizer,error_rate=0.2):
        tokens = tokenizer.tokenize(sentence)
        return [  self.spell_check(token,max(int(len(token)*error_rate),1)) for token in tokens]

    def  query_files_by_sentence(self,sentence,tokenizer,error_rate=0.2,flag_spell_check=True):
        tokens = tokenizer.tokenize(sentence)
        results = set([]) 
        for token in tokens:
            results = results|set(self.query_files_by_token(token, error_rate, flag_spell_check))
        return list(results)




