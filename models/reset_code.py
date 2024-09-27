from models import db
from models.user import User


class ResetCode(db.Model):
    __tablename__ = 'reset_code_table'

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('user_table.id'))
    code = db.Column(db.Float, unique=True, nullable=False)

    owner = db.relationship('User', back_populates='codes')

    def __init__(self, owner_id, code):
        self.owner_id = owner_id
        self.code = code

    @staticmethod
    def add_code(owner_id, code):
        if not User.query.filter_by(id=owner_id):
            return False

        if ResetCode.query.filter_by(code=code).count() > 0:
            return False

        reset_code = ResetCode(owner_id, code)
        reset_code.save()

        return True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<ResetCode: Code - {self.code}; Owner ID - {self.owner_id}; >"
