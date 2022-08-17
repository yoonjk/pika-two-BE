from flask import jsonify, request
from flask_restx import Resource, Namespace
from src.service.financialproduct import *
from src.util.ml import *

Financialproduct = Namespace('Financialproduct')


@Financialproduct.route('/<int:user_id>')
class financialproduct(Resource):
    #추천상품 조회
    def get(self, user_id):
        result = ml(user_id)

        return jsonify({"code": 200, "data": result})
