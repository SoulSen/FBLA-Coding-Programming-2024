from flask import render_template, request, jsonify, redirect
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from models.partner import Partner


class AddPartner(MethodView):
    def post(self):
        data = request.form

        name = data.get('name')
        organization_type = data.get('organizationType')
        resource_type = data.get('resourceType')
        description = data.get('description')
        contact_name = data.get('contactName')
        contact_email = data.get('contactEmail')
        contact_number = data.get('contactPhoneNumber')

        Partner.add_partner(name, organization_type, resource_type, description,
                            contact_name, contact_email, contact_number)

        return redirect('/')
