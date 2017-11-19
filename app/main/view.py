# -*- coding: utf-8 -*-
from flask import  url_for,redirect,render_template,flash,jsonify,request
from . import App,ir_sys,ir_sys_porter
from backend import  util
from  backend import tokenizer as tk
import os,sys,inspect
import _pickle as  pickle
from backend import util

#a part group is a tuple (token_number,string) #the string is a regular expression group
@App.route('/detail_match/<article_title>/<token_string>/<token_algorithm>')
def detail_match(article_title,token_string,token_algorithm):
    ir_sys_for_query = None
    if token_algorithm == 'normal':
        ir_sys_for_query = ir_sys
    elif token_algorithm == 'porter':
        ir_sys_for_query = ir_sys_porter
    else:
        assert False

    tokens = token_string.split(",")
    corupus_list = [ queryer.indexer.corpus for  _,queryer in ir_sys_for_query.queryers.items()]
    article  = None
    for corpus in corupus_list:
        for path,a in corpus.articles.items():
            if type(a) is list:
                for  aa in a:
                    if aa.getTitle() == article_title:
                        article = aa
                        break
            elif a.getTitle() ==  article_title:
                article = a
                break
        if article is not None:
            break

    if article is None:
        return 'cannot find article'
    #
    if article.getType()=='pubmed':
        title_part_group,abstracts_part_groups =util.find_token_pos_in_pubmed_article(tokens, article)
        print(abstracts_part_groups)
        return render_template("match_detail_pubmed.html", title=article_title, content=article.abstract_text,
                               tokens=tokens,
                               title_part_group=title_part_group,
                               abstracts_part_groups=abstracts_part_groups)
    elif article.getType()=='twitter':
        text_part_group = util.find_token_pos_in_twitter_article(tokens, article)
        return render_template("match_detail_twitter.html", title=article_title, content=article.text,
                               tokens=tokens,
                               text_part_groups= text_part_group)
    else:
        return 'unknown article type'

    return 'unknown article type....'

@App.route('/query',methods=['POST'])
def query():
    item_per_page = 10
    query = request.form['query']

    if 'page_idx' in  request.form: 
        page_idx = int(request.form['page_idx'])
    else:
        page_idx = 1

    try:
        k_num = int(request.form['top_k_num'])
    except:
        k_num = 10

    token_algorithm = request.form['token_algorithm']

    ir_sys_for_query = None #
    if token_algorithm == 'normal':
        ir_sys_for_query = ir_sys
    elif token_algorithm=='porter':
        ir_sys_for_query = ir_sys_porter
    else:
        assert False



    titles_by_order,abstracts_by_order,corpus_names, match_total, token_matches, tokens =   ir_sys_for_query .make_query(query,k_num)
    total_item_num =  len(titles_by_order) 

    tokenizer = tk.SpaceTokenizer()
    alternative_query = ''

    start_idx = (page_idx-1)*item_per_page
    if start_idx >= total_item_num:
        page_idx =  (total_item_num-1)//item_per_page+1
        start_idx = (page_idx-1)*item_per_page
    if start_idx<=0:
        page_idx = 1
        start_idx = 0
    end_idx = start_idx + item_per_page

    if end_idx>= total_item_num:
        end_idx = total_item_num-1

    titles_by_order = titles_by_order[start_idx:end_idx+1]

    if not ir_sys.all_in_vocab_set(tokenizer.tokenize(query)):
        alternative_query_tokens =  ir_sys.alternative_query(query,tokenizer)
        alternative_query = " ".join(alternative_query_tokens)
    #pagination
   
    return  render_template("query_list.html",
                            query = query,
                            page_idx = page_idx,
                            last_page =  (total_item_num-1)//item_per_page+1,
                            top_k_num = k_num,
                            token_algorithm=token_algorithm ,
                            alternaive_query=alternative_query,
                            titles_by_order=titles_by_order,
                            abstracts_by_order=abstracts_by_order,
                            corpus_names=corpus_names,
                            match_total=match_total,
                            token_matches=token_matches,
                            tokens=tokens,
                            list_result_flag=True)




@App.route('/')
@App.route('/index', methods=['GET'])
def login():
    return render_template("index.html")

@App.route('/list_corpus')
def list_corpus():
    with open('./temp/normal/corpus_names.pkl', mode='rb') as f:
        _dict = pickle.load(f)
    corpus_names = {key:[os.path.basename(path) for path in l] for key,l in _dict.items()}
    return render_template("list_corpus.html",corpus_names=corpus_names)

@App.route('/dist_figure/<corpus_category>/<corpus_name>',methods=['POST','GET'])
def dist_figure(corpus_category,corpus_name):
    if 'num'   not in request.form or len(request.form['num'])==0: 
        num = 100
    else:
        try :
            num = int(request.form['num'])
        except:
            num = 100
    print('corpus name %s num:%d'%(corpus_name,num))

    if num<10:
        num = 10

    print('loading corpus...')
    with open("./temp/normal/corpus.pkl", mode='rb') as f:
        corpus_list = pickle.load(f)
    print('loading end .....')

    #top_words1, down_words1, random_words1,top_freqs1,down_freqs1,random_freqs1, random_idx1=[],[],[],[],[],[],[]
    #top_words2, down_words2, random_words2,top_freqs2,down_freqs2,random_freqs2, random_idx2 = [],[],[],[],[],[],[]

    corpus = [corpus for corpus in corpus_list if (corpus_category+'\\'+corpus_name)==corpus.name][0]



    save_path_root = './main/static'

    articles = util.top_n_relevant_articles(corpus,num)
    zipf = util.Zipf()
    zipf.add_articles(articles)


    filename_prefix = '%s/%s/%s/%d'%(save_path_root,corpus_category,corpus_name,num)
    zipf.save_dist_figure('%s/%s first %d artilces'%(corpus_category,corpus_name,num),
                            '%s.png'%(filename_prefix))

    top_words1, down_words1, random_words1,top_freqs1,down_freqs1,random_freqs1, random_idx1 = util.get_top_down_random_words(zipf)

    # for porter
    zipf = util.Zipf()

    print('loading corpus...')
    with open("./temp/porter/corpus.pkl", mode='rb') as f:
        corpus_list = pickle.load(f)
    print('loading end .....')
    
    corpus = [corpus for corpus in corpus_list if (corpus_category+'\\'+corpus_name)==corpus.name][0]

    articles = util.top_n_relevant_articles(corpus,num)
    zipf = util.Zipf()
    zipf.add_articles(articles)  
    zipf.save_dist_figure('%s/%s first %d articles (Porter)'%(corpus_category,corpus_name,num),
                        '%s_porter.png'%(filename_prefix))

    top_words2, down_words2, random_words2,top_freqs2,down_freqs2,random_freqs2, random_idx2 = util.get_top_down_random_words(zipf)
    
    #tops = ([(),()],[(),()])
    tops,downs,randoms,random_idxs = \
        (list(zip(top_words1,top_freqs1)),list(zip(top_words2,top_freqs2))),\
        (list(zip(down_words1, down_freqs1)), list(zip(down_words2, down_freqs2))),\
        (list(zip(random_words1,  random_freqs1)), list(zip( random_words2,  random_freqs2))),\
        (random_idx1,random_idx2)

    #tokenizeAll
    #zipf.save_dist_figure(title,save_path)
    #util.save_dist_figure(corpus, corpus_name + " porter", save_path)
    return render_template('dist_figure.html',corpus_category=corpus_category,corpus_name=corpus_name,
                           filename_prefix='%s/%s/%d'%(corpus_category,corpus_name,num),
                           tops=tops,downs=downs,randoms=randoms,random_idxs=random_idxs)


@App.route('/query_system')
def query_system():
    return render_template('query_list.html',list_result_flag=False,page_idx=1,last_page=0)

@App.route('/wiki')
def wiki():
    return render_template('wiki.html')


@App.route('/wiki_anayize',methods=["POST"])
def wiki_anayize():
    topic = request.form['topic']
    from backend import WikiAnalizer as wa
    topic_analyzer = wa.WikiAnalizer(topic)
    zipf = topic_analyzer.zipf
    save_path_root = './main/static/wiki'
    zipf.save_dist_figure('wiki  for %s' % (topic_analyzer.topic), '%s/%s.png' % (save_path_root,topic_analyzer.topic))
    top_words, down_words, random_words, top_freqs, down_freqs, random_freqs, random_idx = util.get_top_down_random_words( zipf)
    tops,downs,randoms = list(zip(top_words,top_freqs)),list(zip(down_words,down_freqs)),list(zip(random_words,random_freqs))
    return render_template('wiki_dist.html',text=topic_analyzer.text,topic=topic,tops=tops,downs=downs,randoms=randoms,random_idxs=random_idx)

