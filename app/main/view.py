# -*- coding: utf-8 -*-
from flask import  url_for,redirect,render_template,flash,jsonify,request
from . import App,ir_sys
from backend import  util
from  backend import tokenizer as tk
import os,sys,inspect


#a part group is a tuple (token_number,string) #the string is a regular expression group
@App.route('/detail_match/<article_title>/<token_string>')
def detail_match(article_title,token_string):
    tokens = token_string.split(",")
    corupus_list = [ queryer.indexer.corpus for  _,queryer in ir_sys.queryers.items()]
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
    query = request.form['query']
    titles_by_order,corpus_names, match_total, token_matches, tokens =   ir_sys.make_query(query,3)
    tokenizer = tk.SpaceTokenizer()
    alternative_query = ''

    if not ir_sys.all_in_vocab_set(tokenizer.tokenize(query)):
        print(44)
        alternative_query_tokens =  ir_sys.alternative_query(query,tokenizer)
        print(alternative_query_tokens)
        alternative_query = " ".join(alternative_query_tokens)
    return  render_template("query_list.html",
                            alternaive_query=alternative_query,
                            titles_by_order=titles_by_order,
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
    with open('./temp/corpus_names.pkl', mode='rb') as f:
        import _pickle as  pickle
        _dict = pickle.load(f)
    corpus_names = {key:[os.path.basename(path) for path in l] for key,l in _dict.items()}
    return render_template("list_corpus.html",corpus_names=corpus_names)

@App.route('/dist_figure/<corpus_category>/<corpus_name>')
def dist_figure(corpus_category,corpus_name):
   return render_template('dist_figure.html',corpus_category=corpus_category,corpus_name=corpus_name)
@App.route('/query_system')
def query_system():
    return render_template('query_list.html',list_result_flag=False)