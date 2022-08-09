from flask import Flask
from os import environ
from src.config import DevConfig, PrdConfig
from src.database import db, migrate

app = Flask(__name__)

if environ.get("FLASK_ENV") == "dev":
    app.config.from_object(DevConfig())
else:
    app.config.from_object(PrdConfig())

@app.route('/')
def hello():
    msg = ""
    for key, val in app.config["DB"].items():
        msg += f"{key}={val}\n"
    msg += f"{app.config['DB_URI']}"
    return msg
    
if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
    db.init_app(app)
    migrate.init_app(app, db)