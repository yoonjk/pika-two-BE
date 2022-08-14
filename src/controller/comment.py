from flask import jsonify, request
from flask_restx import Resource, Namespace
from src.service.comment import *


Comment = Namespace('Comment')


@Comment.route('/<int:company_id>/comment')
class Review(Resource):

    #리뷰조회
    def get(self, company_id):
        return jsonify({"code": 200, "data": get_comment(company_id)})

    #리뷰등록
    def post(self, company_id):
        post_comment(company_id,dict(request.get_json()))
        return jsonify({"code": 200})

@Comment.route('/<int:company_id>/comment/<int:commenter_id>')
class Review_delete(Resource):
    #리뷰삭제
    def delete(self, company_id, commenter_id):
        delete_comment(company_id, commenter_id)
        return jsonify({"code": 200})
