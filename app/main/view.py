# -*- coding: utf-8 -*-
from flask import  url_for,redirect,render_template,flash,jsonify
from . import App,ir_sys
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

@App.route('/')
@App.route('/index', methods=['GET'])
def login():
    return render_template("index.html")

@App.route('/list_corpus')
def list_corpus():
    print('1234')
    print(ir_sys.corpus_names)
    return 'list corpus'

@App.route('/query_system')
def query_system():
    return 'query_system'