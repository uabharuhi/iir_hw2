import math
from  collections import Counter



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
        idf_list[ID] = math.log(len(token2id)/(cnt+1))

    return idf_list


class ScoreAlgorithm():
    def __init__(self,tf_func,idf_func):
        pass


































class TermFrequencyFactory():
    def __init__(self):
        pass
