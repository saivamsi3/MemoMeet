from flask import Flask
from config import Config
from extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.context_processor
    def inject_unread_notifications():
        from flask_login import current_user
        from models.notification import Notification
        if current_user.is_authenticated:
            count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
            return {'unread_notifications_count': count}
        return {'unread_notifications_count': 0}

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.participants import participants_bp
    from routes.meetings import meetings_bp
    from routes.memories import memories_bp
    from routes.action_items import action_items_bp
    from routes.reports import reports_bp
    from routes.analytics import analytics_bp
    from routes.chatbot import chatbot_bp
    from routes.recommendations import recommendations_bp
    from routes.timeline import timeline_bp
    from routes.notifications import notifications_bp
    from routes.search import search_bp
    from routes.settings import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(participants_bp)
    app.register_blueprint(meetings_bp)
    app.register_blueprint(memories_bp)
    app.register_blueprint(action_items_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(timeline_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(settings_bp)

    with app.app_context():
        from database.db import init_db
        from database.seed import seed_database
        init_db()
        seed_database()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
