from flask import Flask
from flask_restx import Api, Resource
from api.src.nickname_gen import nick_gen

app = Flask(__name__)
api = Api(app)  # Flask 객체에 Api 객체 등록

@api.route('/users/signup')
class SignUp(Resource):
    def get_signup(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

@app.route('/')

def hello():
    return nick_gen(1)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


