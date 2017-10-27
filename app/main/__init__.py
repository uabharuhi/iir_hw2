from flask import Flask

App=None

def init_app():
     global App
     App = Flask(__name__)
     App.config['DEBUG'] = True
     App.config['SECRET_KEY'] = 'super-secret'
     App.config['TEMPLATES_AUTO_RELOAD'] = True

     from . import view

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


