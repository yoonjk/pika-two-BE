from flask import Flask
from config import DevConfig, PrdConfig
from src.database import db, migrate
from src.apis import api
from src.model.models import User
import logging
import os

logging.basicConfig(filename="logs/pikatwo-be.log", level=logging.DEBUG)

def create_app():
    app = Flask(__name__)

    if os.environ.get("FLASK_ENV") == "prd":
        app.config.from_object(PrdConfig())
    else:
        app.config.from_object(DevConfig())

    log_dir = app.config.get("BASEDIR") + "/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    @app.route('/')
    def hello():
        msg = ""
        for key, val in app.config["DB"].items():
            msg += f"{key}={val}<br>"
        msg += f"{app.config['DB_URI']}<br>"
        msg += f"{app.config['SQLALCHEMY_DATABASE_URI']}<br>"
        return msg

    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
