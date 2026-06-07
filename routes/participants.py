from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from models.participant import Participant
from models.relationship import Relationship
from services.timeline_service import TimelineService

participants_bp = Blueprint("participants", __name__)


@participants_bp.route("/participants")
@login_required
def list_participants():
    search = request.args.get("search", "")
    query = Participant.query.filter_by(user_id=current_user.id)
    if search:
        query = query.filter(
            (Participant.name.ilike(f"%{search}%")) |
            (Participant.email.ilike(f"%{search}%")) |
            (Participant.organization.ilike(f"%{search}%")) |
            (Participant.role.ilike(f"%{search}%")) |
            (Participant.interests.ilike(f"%{search}%")) |
            (Participant.goals.ilike(f"%{search}%")) |
            (Participant.preferences.ilike(f"%{search}%")) |
            (Participant.notes.ilike(f"%{search}%"))
        )
    participants = query.order_by(Participant.name).all()
    return render_template("participants/participants.html", participants=participants, search=search)


@participants_bp.route("/participants/add", methods=["GET", "POST"])
@login_required
def add_participant():
    if request.method == "POST":
        participant = Participant(
            user_id=current_user.id,
            name=request.form.get("name"),
            email=request.form.get("email"),
            organization=request.form.get("organization"),
            role=request.form.get("role"),
            interests=request.form.get("interests"),
            goals=request.form.get("goals"),
            preferences=request.form.get("preferences"),
            notes=request.form.get("notes"),
        )
        db.session.add(participant)
        db.session.commit()
        flash("Participant added", "success")
        return redirect(url_for("participants.list_participants"))
    return render_template("participants/add_participant.html")


@participants_bp.route("/participants/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_participant(id):
    participant = Participant.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    if request.method == "POST":
        participant.name = request.form.get("name")
        participant.email = request.form.get("email")
        participant.organization = request.form.get("organization")
        participant.role = request.form.get("role")
        participant.interests = request.form.get("interests")
        participant.goals = request.form.get("goals")
        participant.preferences = request.form.get("preferences")
        participant.notes = request.form.get("notes")
        db.session.commit()
        flash("Participant updated", "success")
        return redirect(url_for("participants.list_participants"))
    return render_template("participants/edit_participant.html", participant=participant)


@participants_bp.route("/participants/<int:id>")
@login_required
def participant_details(id):
    participant = Participant.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    # load related meetings and relationship data
    meetings = TimelineService.get_meetings_for_participant(participant.id, current_user.id)
    relationship = Relationship.query.filter_by(participant_id=participant.id, user_id=current_user.id).first()
    return render_template("participants/participant_details.html", participant=participant, meetings=meetings, relationship=relationship)


@participants_bp.route("/participants/<int:id>/delete")
@login_required
def delete_participant(id):
    participant = Participant.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(participant)
    db.session.commit()
    flash("Participant deleted", "success")
    return redirect(url_for("participants.list_participants"))
