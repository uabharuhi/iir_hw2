import textloader as tl
import parse 
import tokenizer
import indexer
loader = tl.TextLoader()
corpus = loader.load_corpus_from_directory('./data/pubmed/')
factory = parse.ParserFactory()
corpus.parseAll(factory)
articles = corpus.articles
tokenizer = tokenizer.SpaceTokenizer()
corpus.tokenizeAll(tokenizer)
corpus.build_vocab()
indexer = indexer.Indexer(corpus)
# files = indexer.search_files_by_index('the')
# print(len(files))
#for p,article in articles.items():
    #print('1')
    #article.show()
    #print(article.getTokens())
    #break
