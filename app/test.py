from backend import textloader as tl
from backend import parse
from backend import tokenizer as tk
from backend import indexer as idx
from backend import util
from backend import queryer as q
#from backend import ir
#todo spell check by not only editdistance but also term frequency

#example test_top_n_rel('pubmed\\gene')
def test_top_n_rel(full_corpus_name):
    import _pickle as pickle
    print('loading corpus...')
    with open("./temp/corpus.pkl", mode='rb') as f:
        corpus_list = pickle.load(f)
    print('loading end .....')
    corpus = [corpus for corpus in corpus_list if full_corpus_name==corpus.name][0]
    util.top_n_relevant_articles(corpus, 10)

def test_part_group():
    from backend import article as a
    article = a.PubMedArticle()
    article.setTitle("i don't want to do any ... !dog  pen!")
    article.add_abstract_text("a pen-pen  pen is a #dog")
    article.add_abstract_text("i have a \n pen")
    article.tokenize(tk.SpaceTokenizer())
    tokens = ["i","have","a","dog","pen"]
    title_group,abstract_group = util.find_token_pos_in_pubmed_article(tokens, article)

    print(title_group)
    print(abstract_group)


def test_ir_sys2():
    ir_sys = ir.IRSystem()
    corpusname, _,match_total, token_matchtimes,tokens = ir_sys.make_query("i have a pen gene",3)
    print(corpusname)
    print(match_total)
    print(token_matchtimes)


def test_ir_sys():
    ir_sys = ir.IRSystem()
    print(ir_sys.corpus_names['pubmed'][0])
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
    l = queryer.query_files_by_sentence("i have a pen",tokenizer,0.2,False)[0]
    print_res(l)
    l2 = list(
        set(queryer.query_files_by_token("i",0.2,False)[0]+queryer.query_files_by_token("have",0.2,False)[0]
    +queryer.query_files_by_token("a",0.2,False)[0]+queryer.query_files_by_token("pen",0.2,False)[0]))
    print(len(l))
    print(len(l2))
    #沒sort會不一樣
    assert sorted(l)==sorted(l2)

    print('------ spell check')
    print_res(queryer.query_files_by_token("gne",1,True)[0])
    #query_files_by_sentence
#def test_query_token(token,error_rate,flag_spell_check=True))
#    query_token(self,token,error_rate,flag_spell_check=True):
#def test_query_sentence(indexer,sentence,tokenizer,error_rate,flag_spell_check):
#    pass
    #queryer = Queryer(indexer).query_sentence(self,sentence,tokenizer,error_rate,flag_spell_check=True):


def main_test():
    loader = tl.TextLoader()
    print('main test')
    corpus = loader.load_corpus_from_directory('foo','./backend/data/pubmed/gene')
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
    test_query_sentence(tokenizer,indexer)
    #files = indexer.search_files_by_index('the')
    #print(len(files))
    #for p,article in articles.items():
        #print('1')
        #article.show()
        #print(article.getTokens())
        #break

test_top_n_rel('twitter\\zika')
#test_ir_sys()
#test_edit_distance1()