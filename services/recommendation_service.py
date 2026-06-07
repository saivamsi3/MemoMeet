from extensions import db
from models.recommendation import Recommendation


class RecommendationService:
    @staticmethod
    def create(user_id, recommendation_type, content, participant_id=None, priority="medium"):
        r = Recommendation(
            user_id=user_id, recommendation_type=recommendation_type,
            content=content, participant_id=participant_id, priority=priority,
        )
        db.session.add(r)
        db.session.commit()
        return r

    @staticmethod
    def get_by_user(user_id):
        return Recommendation.query.filter_by(user_id=user_id).order_by(Recommendation.created_at.desc()).all()
