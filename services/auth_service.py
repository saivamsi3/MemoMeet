from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.user import User


class AuthService:
    @staticmethod
    def register(username, email, password):
        if User.query.filter_by(email=email).first():
            return None
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def authenticate(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            return user
        return None
