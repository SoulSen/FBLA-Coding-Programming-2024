from flask import render_template, request, jsonify, after_this_request, redirect
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from models.partner import Partner


class RemovePartner(MethodView):
    @jwt_required(optional=True)
    def post(self):
        @after_this_request
        def add_header(response):
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response

        data = request.get_json()

        name = data.get('name')

        partner_obj = Partner.get_partner_by_name(name)
        partner_id = partner_obj.id
        Partner.delete_partner(partner_id)

        return redirect('/')
