# -*- coding: utf-8 -*-
from flask import  url_for,redirect,render_template,flash,jsonify,request
from . import App,ir_sys
from backend import  util
import os,sys,inspect



@App.route('/detail_match/<article_title>/<token_string>')
def detail_match(article_title,token_string):
    tokens = token_string.split(",")
    corupus_list = [ queryer.indexer.corpus for  _,queryer in ir_sys.queryers.items()]
    article  = None
    for corpus in corupus_list:
        for path,a in corpus.articles.items():
            if a.title ==  article_title:
                article = a
                break
        if article is not None:
            break


    if article.getType()=='pubmed':
        return render_template("match_detail_pubmed.html", title=article_title, content=article.abstract_text)
    return 'unknown article type....'

@App.route('/query',methods=['POST'])
def query():
    query = request.form['query']
    print('query is')
    print(query)
    corpus_names, match_total, token_matches, tokens =   ir_sys.make_query(query, 3)
    return  render_template("query_list.html",corpus_names=corpus_names,match_total=match_total, token_matches=token_matches, tokens=tokens)




@App.route('/')
@App.route('/index', methods=['GET'])
def login():
    return render_template("index.html")

@App.route('/list_corpus')
def list_corpus():
    corpus_names = {key:[os.path.basename(path) for path in l] for key,l in ir_sys.corpus_names.items()}
    return render_template("list_corpus.html",corpus_names=corpus_names)

@App.route('/dist_figure/<corpus_category>/<corpus_name>')
def dist_figure(corpus_category,corpus_name):
   return render_template('dist_figure.html',corpus_category=corpus_category,corpus_name=corpus_name)
@App.route('/query_system')
def query_system():
    return render_template('query_index.html')