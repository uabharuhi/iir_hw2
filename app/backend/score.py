import math
from  collections import Counter




#def make_tf_func(name):
#    log_count = lambda cnt:1+math.log(cnt)
#    
#    if name=='l':





## input : 
#   document -- list of tokens
#   token2id -- key is token ,output is id


## output :  list of term frequency  output[0] = tf of token with id list
def tf_logrithm(token_list,token2id):
    tf_list = [0 for i in range(len(token2id))]
    counter = Counter(token_list)
    tuples = counter.most_common()
    for token,cnt in tuples:
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


class ScoreAlgorithm():
    def __init__(self,token2id,tf_func=tf_logrithm,idf_func=idf_t):
        self.token2id = token2id
        self.tf_func = tf_func
        self.idf_func = idf_func
    ## input : 
    #   document_list -- list of  document , each document is a list of token
    #  output :
    #   scores Llist of document vector,each document vector is a list of tf-idf value
    #  
    def calculate(self,document_list):
        idf_list = self.idf_func(document_list, self.token2id)
        scores = []
        for document in document_list:
            term_freq_list = self.tf_func(document, self.token2id)
            for i,term_freq in enumerate(term_freq_list):
                term_freq_list[i]*= idf_list[i]
            scores.append(term_freq_list)
        return scores





































class TermFrequencyFactory():
    def __init__(self):
        pass
