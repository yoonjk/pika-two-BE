from flask import jsonify, request
from flask_restx import Resource, Namespace
from src.service.comment import delete_comment, post_comment, get_comment


Comment = Namespace('Comment')


@Comment.route('/<string:company_id>/comment')
class Review(Resource):

    #리뷰조회
    def get(self, company_id):
        print(company_id)
        return jsonify({"code": 200, "data": get_comment(company_id)})

    #리뷰등록
    def post(self, company_id):
        print(company_id)
        post_comment(company_id)
        return jsonify({"code": 200})

    #리뷰삭제
    def delete(self, company_id):
        delete_comment(request.get_json()['comment_id'])
        return jsonify({"code": 200})
