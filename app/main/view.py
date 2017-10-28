# -*- coding: utf-8 -*-
from flask import  url_for,redirect,render_template,flash,jsonify
from . import App,ir_sys
import os,sys,inspect
from pathlib import Path



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
    return 'query_system'