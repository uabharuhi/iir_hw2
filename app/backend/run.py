import textloader as tl
import parse
import tokenizer as tk
import indexer as idx
import util
import queryer as q

#todo spell check by not only editdistance but also term frequency

def test_edit_distance1():
   d = util.minEditDist("the","h")
   print("edit distance:%d"%(d))

def test_near_corpus_token(token,corpus):
    ans = util.most_near_token(corpus,token)
    print("nearest corpus token of [%s] is :"%(token))
    print(ans)

def test_query_token(indexer):
    def print_res(l):
        print("found %d results:"%(len(l)))
        print(l)
    queryer = q.Queryer(indexer)
    print_res(queryer.query_files_by_token("the",0.2,False))
    print_res(queryer.query_files_by_token("gene",0.2,False))
    print_res(queryer.query_files_by_token("zika",0.2,False))
    print_res(queryer.query_files_by_token("protein",0.2,False))

    print('------ spell check')
    print_res(queryer.query_files_by_token("gne",1,True))
    
def test_query_sentence(tokenizer,indexer):
    def print_res(l):
        print("found %d results:"%(len(l)))
        print(l)
    queryer = q.Queryer(indexer)
    l = queryer.query_files_by_sentence("i have a pen",tokenizer,0.2,False)
    print_res(l)
    l2 = list(set(queryer.query_files_by_token("i",0.2,False)+queryer.query_files_by_token("have",0.2,False)
    +queryer.query_files_by_token("a",0.2,False)+queryer.query_files_by_token("pen",0.2,False)))
    print(len(l))
    print(len(l2))
    #沒sort會不一樣
    assert sorted(l)==sorted(l2)

    print('------ spell check')
    print_res(queryer.query_files_by_token("gne",1,True))
    #query_files_by_sentence
#def test_query_token(token,error_rate,flag_spell_check=True))
#    query_token(self,token,error_rate,flag_spell_check=True):
#def test_query_sentence(indexer,sentence,tokenizer,error_rate,flag_spell_check):
#    pass
    #queryer = Queryer(indexer).query_sentence(self,sentence,tokenizer,error_rate,flag_spell_check=True):


def main_test():
    loader = tl.TextLoader()
    corpus = loader.load_corpus_from_directory('./data/pubmed/gene')
    factory = parse.ParserFactory()
    corpus.parseAll(factory)
    #articles = corpus.articles
    tokenizer = tk.SpaceTokenizer()
    corpus.tokenizeAll(tokenizer)
    corpus.build_vocab()
    #test_near_corpus_token("the",corpus)
    #test_near_corpus_token("hte",corpus)
    #test_near_corpus_token("genetic",corpus)
    #test_near_corpus_token("ganetic",corpus)
    #test_near_corpus_token("gan",corpus)
    #util.zip_dist_corpus(corpus,'test')
    indexer = idx.Indexer(corpus)
    #test_query_sentence(tokenizer,indexer)
    #queryer = q.Queryer(indexer)
    #print(queryer.get_spellchecked_tokens("gane is pretein",tokenizer,error_rate=0.6))
    files = indexer.search_files_by_index('the')
    print(len(files))
    #for p,article in articles.items():
        #print('1')
        #article.show()
        #print(article.getTokens())
        #break
main_test()
#test_edit_distance1()