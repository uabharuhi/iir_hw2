from main import init_app
import os

basedir = os.path.dirname(os.path.realpath(__file__))
App = init_app()
from flask_script import Manager

manager = Manager(App)
if __name__ == '__main__':
    manager.run()