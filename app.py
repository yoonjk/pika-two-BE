from flask import Flask
from config import DevConfig, PrdConfig
from src.database import db, migrate
from src.apis import api
from flask_cors import CORS
import logging
import os


def create_app():
    app = Flask(__name__)

    if os.environ.get("FLASK_ENV") == "prd":
        app.config.from_object(PrdConfig())
        my_cors = CORS(app,resources={r"*" : {"origins" : ["http://pikatwo.kbfg.kubepia.com"]}},supports_credentials=True)
    else:
        app.config.from_object(DevConfig())
        my_cors = CORS(app,resources={r"*" : {"origins" : ["http://127.0.0.1:5000", "http://localhost:5000"]}},supports_credentials=True)

    log_dir = app.config.get("LOGDIR")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(filename=f"{log_dir}pikatwo-be.log", level=logging.DEBUG)
    logging.info(f'DB: {app.config["DB"]}, DB_URI: {app.config["DB_URI"]}, SQLALCHEMY_DATABASE_URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    
    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
