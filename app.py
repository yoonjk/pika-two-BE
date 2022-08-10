from flask import Flask
from os import environ
from src.config import DevConfig, PrdConfig
from src.database import db, migrate

def create_app():
    app = Flask(__name__)

    if environ.get("FLASK_ENV") == "prd":
        app.config.from_object(PrdConfig())
    else:
        app.config.from_object(DevConfig())

    @app.route('/')
    def hello():
        msg = ""
        for key, val in app.config["DB"].items():
            msg += f"{key}={val}<br>"
        msg += f"{app.config['DB_URI']}<br>"
        msg += f"{app.config['SQLALCHEMY_DATABASE_URI']}<br>"
        return msg

    db.init_app(app)
    migrate.init_app(app, db)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)

"""
app = Flask(__name__)

if environ.get("FLASK_ENV") == "prd":
    app.config.from_object(PrdConfig())
else:
    app.config.from_object(DevConfig())

@app.route('/')
def hello():
    msg = ""
    for key, val in app.config["DB"].items():
        msg += f"{key}={val}<br>"
    msg += f"{app.config['DB_URI']}<br>"
    msg += f"{app.config['SQLALCHEMY_DATABASE_URI']}<br>"
    return msg
    
if __name__ == '__main__':
    db.init_app(app)
    migrate.init_app(app, db)
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
"""