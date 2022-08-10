from flask import Flask
from flask_restx import Api, Resource
from os import environ
from src.config import DevConfig, PrdConfig
from src.database import db, migrate

from api.src.nickname_gen import nick_gen

def create_app():
    app = Flask(__name__)
    api = Api(app)  # Flask 객체에 Api 객체 등록

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
        
    @api.route('/users/signup')
    class SignUp(Resource):
        def get_signup(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
            return {"hello": "world!"}

    db.init_app(app)
    migrate.init_app(app, db)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)

"""
app = Flask(__name__)
api = Api(app)  # Flask 객체에 Api 객체 등록

@api.route('/users/signup')
class SignUp(Resource):
    def get_signup(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

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