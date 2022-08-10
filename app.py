from flask import Flask
from flask_restx import Api, Resource, Namespace
from os import environ
from src.config import DevConfig, PrdConfig
from src.controller.user import Todo
from src.database import db, migrate

app = Flask(__name__)
api = Api(app)
#
# api.add_namespace(Signup, '/user')
# api.add_namespace(DepositSummary, '/user/signup')
# api.add_namespace(AccountList, '/user/signup')
# api.add_namespace(AppliedList, '/user/signup')
# api.add_namespace(FavList, '/user/signup')


if environ.get("FLASK_ENV") == "dev":
    app.config.from_object(DevConfig())
else:
    app.config.from_object(PrdConfig())


@api.route('/')
class Hello(Resource):
    def get(self):
        msg = ""
        for key, val in app.config["DB"].items():
            msg += f"{key}={val}\n"
        msg += f"{app.config['DB_URI']}"
        return msg


api.add_namespace(Todo, '/api/user')



# @api.route('/hello/<string:name>')  # url pattern으로 name 설정
# class Hello(Resource):
#     def get(self, name):  # 멤버 함수의 파라미터로 name 설정
#         return {"message" : "Welcome, %s!" % name}


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], host="0.0.0.0", port=5000)
    print(app.config["DB_IP"])
    