from flask_restx import Api
from src.controller import CommentAPI, UserAPI, MydataAPI, CompanyAPI

api = Api(version='1.0', title='API 문서', description='Swagger 문서', doc="/api-docs")

api.add_namespace(CommentAPI,'/api/comment')
api.add_namespace(UserAPI,'/api/user')
api.add_namespace(MydataAPI,'/api/mydata')
api.add_namespace(CompanyAPI, '/api/company')