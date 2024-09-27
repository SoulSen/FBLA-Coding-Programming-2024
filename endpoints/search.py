import difflib

from flask import render_template, redirect, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.partner import Partner
from models.user import User


class SearchDashboard(MethodView):
    @jwt_required(optional=True)
    def post(self):
        user_id = get_jwt_identity()

        user = User.get_user(user_id)

        data = request.form

        user_info = user.as_dict()

        partners = Partner.get_partners()

        if data.get('searchQuery') != "":
            partner_names = [partner.name for partner in partners]

            matches = difflib.get_close_matches(data.get('searchQuery'), partner_names, 100, 0.25)
            partners = filter(lambda partner: partner.name in matches, partners)

        if user_id:
            return render_template('dashboard.html', partners=partners,
                                   first_name=user_info['first_name'], last_name=user_info['last_name'],
                                   community_count=Partner.community_partner_count(),
                                   business_count=Partner.business_partner_count())
        else:
            return redirect("/login")
