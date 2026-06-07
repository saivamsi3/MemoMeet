from main import db
from models.user import User
from werkzeug.security import generate_password_hash


def seed_database():
    if User.query.filter_by(email="admin@memomeet.com").first():
        return

    admin = User(
        username="admin",
        email="admin@memomeet.com",
        password_hash=generate_password_hash("admin123"),
        theme="light",
    )
    db.session.add(admin)
    db.session.commit()
