from backend.score import tf_logrithm, idf_t,ScoreAlgorithm
from backend.util import getLookupTables

def test_tf():
    print("term frequency")
    vocab = list(set(['i','have','a','pen','.','i','have','an','apple','.','oh','!','apple','pen']))
    id2token,token2id  = getLookupTables(vocab)
    print("i hava a pen.a")
    print(tf_logrithm(['i','have','a','pen','.','a'],token2id))
    print("i hava an apple.")
    print(tf_logrithm(['i','have','an','apple','.'],token2id))
    print("oh! apple pen")
    print(tf_logrithm(['oh','!','apple','pen'],token2id))
    print('- '*50)
    #print(id2token)
def test_idf():
    print("inverse document frequency")
    documents = [['i','have','a','pen','.'],
                ['i','have','an','apple','.'],
                ['i','oh','!','apple','pen']]
    vocab = list(set(['i','have','a','pen','.','i','have','an','apple','.','oh','!','apple','pen']))
    print(vocab)
    id2token,token2id  = getLookupTables(vocab)
    res = idf_t(documents,token2id)
    print(res)
    print('- '*50)
def test_tfidf():
    vocab = list(set(['i','have','a','pen','.','i','have','an','apple','.','oh','!','apple','pen']))
    id2token,token2id  = getLookupTables(vocab) 
    strategy = ScoreAlgorithm(token2id)
    documents = [['i','have','a','pen','.','a'],
                ['i','have','an','apple','.'],
                ['oh','!','apple','pen']]
    tfidf_scores = strategy.calculate(documents)
    print(tfidf_scores)
    assert  tfidf_scores[0][token2id['a']]==0.686512104608772
test_tf()
test_idf()
test_tfidf()
#test_idf()