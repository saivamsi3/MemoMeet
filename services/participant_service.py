from main import db
from models.participant import Participant


class ParticipantService:
    @staticmethod
    def create(user_id, name, email=None, organization=None, role=None, interests=None, goals=None, preferences=None, notes=None):
        p = Participant(
            user_id=user_id, name=name, email=email,
            organization=organization, role=role,
            interests=interests, goals=goals,
            preferences=preferences, notes=notes,
        )
        db.session.add(p)
        db.session.commit()
        return p

    @staticmethod
    def get_by_user(user_id, search=None):
        query = Participant.query.filter_by(user_id=user_id)
        if search:
            query = query.filter(Participant.name.ilike(f"%{search}%"))
        return query.order_by(Participant.name).all()

    @staticmethod
    def update(participant_id, user_id, **kwargs):
        p = Participant.query.filter_by(id=participant_id, user_id=user_id).first_or_404()
        for key, value in kwargs.items():
            if hasattr(p, key):
                setattr(p, key, value)
        db.session.commit()
        return p

    @staticmethod
    def delete(participant_id, user_id):
        p = Participant.query.filter_by(id=participant_id, user_id=user_id).first_or_404()
        db.session.delete(p)
        db.session.commit()
