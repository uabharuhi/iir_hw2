from backend.score import tf_logrithm
from backend.util import getLookupTables

def test_tf():
    vocab=['i','have','a','pen','.','i','have','a','dog','.']
    id2token,token2id  = getLookupTables(vocab)
    print(tf_logrithm(vocab,token2id))
    print(id2token)

test_tf()