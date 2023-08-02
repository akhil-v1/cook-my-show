import os

from flask import Flask, render_template
from flask_security import Security
from flask_cors import CORS

from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from application.security import user_datastore

import logging

logging.basicConfig(filename="./debug.log", level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

app = None

def create_app():
    app = Flask(__name__, template_folder="templates")
    CORS(app)

    if os.getenv('ENV', "development") == "production":
        app.logger.info("Currently no production config is setup")
        raise Exception("Currently no production config is setup")
    else:
        app.logger.info("Starting local development")
        app.logger.debug("Starting local development")
        print("Starting local development")
        app.config.from_object(LocalDevelopmentConfig)

    db.init_app(app)
    app.app_context().push()

    app.security = Security(app, user_datastore)

    app.logger.info("App setup complete")

    return app

app = create_app()

from application.controllers import *

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__=='__main__':
    log_path = os.path.abspath("./debug.log")
    app.run(host="127.0.0.1", port="5000")

