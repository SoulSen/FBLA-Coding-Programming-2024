from flask import jsonify, redirect, make_response
from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity, unset_jwt_cookies

from models.invalid_token import InvalidToken


class Logout(MethodView):
    @jwt_required(optional=True)
    def post(self):
        jti = get_jwt()['jti']

        if jti:
            invalid_token = InvalidToken(jti=jti)
            invalid_token.save()

            response = make_response(redirect('/login'))
            unset_jwt_cookies(response)

            return response
