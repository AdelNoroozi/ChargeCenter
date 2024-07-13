from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token
from flask_restful import Resource, Api

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'JWT53cR3TK3y'
api = Api(app)
jwt = JWTManager(app)

"""
this APIs are designed to mock a charge service API's basic behaviors. 
more info about the original API: https://podium.ir/s/mobile-payment/docs?code=
"""


class GetAccessToken(Resource):

    def post(self):
        headers = dict(request.headers)
        print(headers)
        if headers.get("Token") != "ChArG3C3nT3Rt0k3n" or headers.get("Token-Issuer") != "1":
            return {"error": f"token error"}, 403
        access_token = create_access_token(identity="ChargeCenter")
        return jsonify(access_token=access_token)


api.add_resource(GetAccessToken, '/apis/token/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8822)
