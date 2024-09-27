from models import db


class InvalidToken(db.Model):
    __tablename__ = 'invalid_token_table'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String)

    @classmethod
    def is_invalid(cls, jti):
        query = cls.query.filter_by(jti=jti).first()

        return bool(query)

    def save(self):
        db.session.add(self)
        db.session.commit()
