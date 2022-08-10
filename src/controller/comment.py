from flask import jsonify, request, app
from flask_restx import Resource, Api


api = Api(app)


@api.route('/api/<string:company_id>/comment')
class FavList(Resource):

    #찜목록
    def get(self, user_id):
        print(user_id)
        return jsonify({"code": 200})

    #찜등록
    def post(self, user_id):
        print(user_id)
        request.get_json()
        return jsonify({"code": 200})


@api.route('/api/<string:company_id>/comment/<string:comment_id>')
class FavList(Resource):

    #찜삭제
    def delete(self, user_id, comment_id):
        print(user_id)
        return jsonify({"code": 200})
