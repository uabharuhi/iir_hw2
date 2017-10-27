# -*- coding: utf-8 -*-
from flask import  url_for,redirect,render_template,flash,jsonify
from . import App

@App.route('/')
@App.route('/index', methods=['GET'])
def login():
    return render_template("index.html")

@App.route('/list_corpus')
def list_corpus():
    return 'list corpus'

@App.route('/query_system')
def query_system():
    return 'query_system'