import os

from flask import (Flask, Blueprint, render_template, redirect, request, url_for)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    """
    @app.route('/', methods=('GET', 'POST'))
    def hello():
        
        if request.method == 'POST':
            term = request.form['query']
            return redirect(url_for('apiCall.results'), term= term
        else:    
            return render_template('index.html')
    """
            
        

    from . import apiCall
    app.register_blueprint(apiCall.bp)

    return app