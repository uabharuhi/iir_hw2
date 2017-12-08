import math
from  collections import Counter


#def  
#self.id2token,self.token2id = util.getLookupTables(self.vocab) 
#    all_article_token_list,title2Document = self.get_all_article_token_list()
#    if which == 'n':
#      self.idf_dict[which] = [1 for i  in range(0,len(self.vocab)) ]
#    elif which == 't':
#      self.idf_dict[which] = score.idf_t(all_article_token_list,self.token2id)



#0.156 0.049 0.044
def cosine_sim_rank(vector,vectors):
    return sorted(range(len(vectors)),key=lambda k:  cosine_sim(vector,vectors[k]))

def cosine_sim(v1,v2):
    assert len(v1) == len(v2)
    import functools
    def norm(v):
        n = functools.reduce(lambda x,y:x+y*y,[0]+v)
        return math.sqrt(n)
    dot = 0
    for i in range(len(v1)):
        dot +=v1[i]*v2[i]
    try:
        assert (norm(v2)* norm(v1))!=0
    except:
        return -1


    return dot/(norm(v1)*norm(v2))

def get_tf_func(which):
    if which == 'n':
        return tf_natural
    elif which == 'l':
        return tf_logrithm
    elif which == 'a':
        return tf_augumented
    else:
        print('tf which %s'%(which))
        assert False



def get_idf_func(which):
    if which == 'n':
        return lambda token_list,token2id: [1 for i in range(len(token2id))]
    elif which == 't':
        return idf_t
    else:
        print('idf which %s'%(which))
        assert False
    
## input : 
#   document -- list of tokens
#   token2id -- key is token ,output is id


## output :  list of term frequency  output[0] = tf of token with id list
def tf_augumented(token_list,token2id):
    tf_list = [0 for i in range(len(token2id))]
    counter = Counter(token_list)

    tuples = counter.most_common()
    try:
        max_cnt =  counter.most_common(1)[0][1]
    except:
        print('except')
        print(counter.most_common(1))
    for token,cnt in tuples:

        if token in token2id:
            tf_list[token2id[token]] = 0.5+0.5*cnt/max_cnt
    return tf_list

def tf_natural(token_list,token2id):
    import collections
    tf_list = [0 for i in range(len(token2id))]
    if len(token_list) == 0:
        return tf_list
    tokens,freq_list = list(zip(*(collections.Counter(token_list).most_common())))
    for i,token in enumerate(tokens):
        if token in  token2id:
            tf_list[token2id[token]] =freq_list[i]
    return tf_list

## input : 
#   document -- list of tokens
#   token2id -- key is token ,output is id


## output :  list of term frequency  output[0] = tf of token with id list
def tf_logrithm(token_list,token2id):
    tf_list = [0 for i in range(len(token2id))]
    counter = Counter(token_list)
    tuples = counter.most_common()
    for token,cnt in tuples:
        if token in token2id:
            tf_list[token2id[token]] = 1+math.log(cnt)
    return tf_list

    #list(zip(*(counter.most_common())))

    #for token in token_list:
    #   tf_list.append(math.log())



def idf_t(document_list,token2id):
    idf_list = [0 for i in range(len(token2id))]

    for token,ID in token2id.items():
        cnt = 0
        for docuemnt_token_list in document_list:
            if  token in  docuemnt_token_list:
                cnt+=1
        idf_list[ID] = math.log(len(document_list)/(cnt+1))

    return idf_list

# t
def sort_tfidf_of_document(tfidf,k_top=50,id2token=None):

    sorted_indexs = sorted(range(len(tfidf)), key=lambda k: -1*tfidf[k])
    n = min(k_top,len(tfidf))
    sorted_indexs = sorted_indexs[0:n]
    if id2token is not None:
        return [ (id2token[ind],tfidf[ind])for ind in sorted_indexs ] 
    return [ (ind,tfidf[ind])for ind in sorted_indexs] 


class ScoreAlgorithm():
    def __init__(self,token2id,tf_func=tf_logrithm,idf_func=idf_t):
        self.token2id = token2id
        self.tf_func = tf_func
        self.idf_func = idf_func

    def calculateOne(self,document_list,document):
        print('idf')
        idf_list = self.idf_func(document_list, self.token2id)
        print('tf')
        tf_list = self.tf_func(document,self.token2id)
        for i,term_freq in enumerate(tf_list):
                tf_list[i]*= idf_list[i]
        return tf_list
    ## input : 
    #   document_list -- list of  document , each document is a list of token
    #  output :
    #   scores Llist of document vector,each document vector is a list of tf-idf value
    # 
    def calculateAll(self,document_list):
        print("idf of cough")
        print('calculate')

        idf_list = self.idf_func(document_list, self.token2id)
        scores = []
        for document in document_list:
            term_freq_list = self.tf_func(document, self.token2id)
            for i,term_freq in enumerate(term_freq_list):
                term_freq_list[i]*= idf_list[i]
            scores.append(term_freq_list)
        return scores
    # accelerate by idf_list pickle object
    def calculateOneWithIdfData(self,idf_list,tokens):
        tf_list = self.tf_func(tokens,self.token2id)
        for i,term_freq in enumerate(tf_list):
                tf_list[i]*= idf_list[i]
        return tf_list




































class TermFrequencyFactory():
    def __init__(self):
        pass
