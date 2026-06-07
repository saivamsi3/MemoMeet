from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from main import db
from models.notification import Notification
from models.recommendation import Recommendation

notifications_bp = Blueprint("notifications", __name__)


@notifications_bp.route("/notifications")
@login_required
def list_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template("notifications/notifications.html", notifications=notifications)


@notifications_bp.route("/notifications/read/<int:id>")
@login_required
def mark_read(id):
    notification = Notification.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    notification.is_read = True
    db.session.commit()
    return redirect(url_for("notifications.list_notifications"))
