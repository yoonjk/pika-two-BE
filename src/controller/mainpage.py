from flask import request, jsonify
from flask_restx import Resource, Namespace
from src.service.mainpage import *

Mainpage = Namespace('Mainpage')

@Mainpage.route('/')
class MainPage(Resource):
    def get(self):

        response = get_main_page_jobposts()

        return jsonify({"code": 200,"data" : response})
