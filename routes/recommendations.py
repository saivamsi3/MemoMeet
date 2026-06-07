from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.recommendation import Recommendation

recommendations_bp = Blueprint("recommendations", __name__)


@recommendations_bp.route("/recommendations")
@login_required
def list_recommendations():
    recs = Recommendation.query.filter_by(user_id=current_user.id).order_by(Recommendation.created_at.desc()).all()
    return render_template("recommendations/recommendations.html", recommendations=recs)
