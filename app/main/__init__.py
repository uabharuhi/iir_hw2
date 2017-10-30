from flask import Flask
from inspect import getsourcefile
import sys,os
from flask_bootstrap import Bootstrap
from pathlib import Path

current_path = os.path.abspath(getsourcefile(lambda:0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.append(parent_dir)

App = None
ir_sys = None
def init_app():
     global App,ir_sys
     App = Flask(__name__)
     App.config['DEBUG'] = True
     App.config['SECRET_KEY'] = 'super-secret'
     App.config['TEMPLATES_AUTO_RELOAD'] = True
     import backend
     #ir_sys = backend.init_ir_system()
     from . import view

     Bootstrap(App)
     return App
'''
     from .post import  blueprint_post
     App.register_blueprint(blueprint_post)

     login_manager.init_app(App)
     from .auth import  blueprint_auth
     App.register_blueprint(blueprint_auth)

     migrate = Migrate(App, db)
     # No cacheing at all for API endpoints.

     @App.context_processor
     def f():
         import app.auth.form
         login_form=app.auth.form.LoginForm()
         login_form.username.data="??"
         return dict(login_form=login_form)
		 @App.after_request
     def add_header(response):
        # response.cache_control.no_store = True
        if 'Cache-Control' not in response.headers:
            response.headers['Cache-Control'] = 'no-store'
        return response
 '''


