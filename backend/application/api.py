from flask import jsonify
from flask_restful import Api, Resource
from flask_restful import reqparse, fields, marshal_with, abort

from .models import *

api = Api()

create_user_req = reqparse.RequestParser()
create_user_req.add_argument("username", type=str, required=True)
create_user_req.add_argument("email", type=str, required=True)
create_user_req.add_argument("pwd", type=str, required=True)
create_user_req.add_argument("role", type=str, required=True)


class UserAPI(Resource):

    def get(self):
        '''
        Getting user information
        '''
        pass

    def put(self):
        '''
        Updating user information
        '''
        pass

    def delete(self):
        '''
        Deleting a user
        '''
        pass

    def post(self):
        '''
        
        '''
        pass