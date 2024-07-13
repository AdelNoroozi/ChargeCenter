from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'JWT53cR3TK3y'
api = Api(app)
jwt = JWTManager(app)

"""
this APIs are designed to mock a charge service API's basic behaviors.
"""


class GetAccessToken(Resource):

    def post(self):
        headers = dict(request.headers)
        if headers.get("Token") != "ChArG3C3nT3Rt0k3n" or headers.get("Token-Issuer") != "1":
            return {"error": f"token error"}, 403
        access_token = create_access_token(identity="ChargeCenter")
        return jsonify(access_token=access_token)


class ChargeAPI(Resource):

    @jwt_required()
    def post(self):
        data = request.get_json()
        if "amount" not in data:
            return {"error": "missing field amount"}, 400
        if "phone_number" not in data:
            return {"error": "missing field phone_number"}, 400
        if type(data.get("amount")) != int:
            return {"error": "amount must be an integer"}, 400
        # fake charging process
        return {"message": "done"}


api.add_resource(GetAccessToken, '/apis/token/')
api.add_resource(ChargeAPI, '/apis/charge/')
