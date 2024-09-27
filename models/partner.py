from models import db
from models.enums.type_organization import OrganizationType


class Partner(db.Model):
    __tablename__ = 'partner_table'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True, nullable=False)
    type_organization = db.Column(db.String, unique=False, nullable=False)
    resources = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False)
    contact_name = db.Column(db.String, unique=False, nullable=False)
    contact_email = db.Column(db.String, unique=False, nullable=False)
    contact_phone = db.Column(db.String, unique=False, nullable=False)

    def __init__(self, name: str, type_organization: str, resources: str, description: str,
                 contact_name: str, contact_email: str, contact_phone: str):
        self.name = name
        self.type_organization = type_organization
        self.resources = resources
        self.description = description
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone

    @staticmethod
    def get_partner_by_name(name):
        return Partner.query.filter_by(name=name).first()

    @staticmethod
    def add_partner(name: str, type_organization: str, resources: str, description: str,
                    contact_name: str, contact_email: str, contact_phone: str):
        if Partner.query.filter_by(name=name).first():
            return False

        partner = Partner(name, type_organization, resources, description, contact_name, contact_email, contact_phone)
        partner.save()

        return True

    @staticmethod
    def delete_partner(partner_id):
        user = Partner.query.get(partner_id)
        user.delete()

        return True

    @staticmethod
    def get_partners():
        partners = Partner.query.all()

        return partners

    @staticmethod
    def filter_partners(**kwargs):
        partners = Partner.query.filter_by(**kwargs).all()

        return partners

    @staticmethod
    def business_partner_count():
        return len(Partner.query.filter_by(type_organization=OrganizationType.BUSINESS.value).all())

    @staticmethod
    def community_partner_count():
        return len(Partner.query.filter_by(type_organization=OrganizationType.COMMUNITY.value).all())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
