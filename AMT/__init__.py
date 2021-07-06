from flask import Flask, session
import os


def create_app(test_config=None):

    from . import Auth
    from . import Arguments

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.register_blueprint(Auth.bp)
    app.register_blueprint(Arguments.bp)
    app.add_url_rule('/', endpoint='Home')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)

#not testing neo4j
        app.config['database']='neo4j'
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
        
#testing
        app.config['database']='testdatabase'

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    return app