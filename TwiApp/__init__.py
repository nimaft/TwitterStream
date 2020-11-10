import os

from flask import (Flask, Blueprint, render_template, redirect, request, url_for)

def page_not_found(e):
    return render_template('404.html'), 404

def create_app(test_config=None):
    # create and configure the app (DB part is not used so it is commented out)
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'#,
        #DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
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

    from . import apiCall
    app.register_blueprint(apiCall.bp)
    app.register_error_handler(404, page_not_found)

    return app