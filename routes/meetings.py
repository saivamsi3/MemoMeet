from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from extensions import db
from models.meeting import Meeting
from models.participant import Participant
from models.meeting_participant import MeetingParticipant
from ai.memory_engine import MemoryEngine

meetings_bp = Blueprint("meetings", __name__)


@meetings_bp.route("/meetings")
@login_required
def list_meetings():
    search = request.args.get("search", "")
    query = Meeting.query.filter_by(user_id=current_user.id)
    if search:
        query = query.outerjoin(MeetingParticipant).outerjoin(Participant).filter(
            (Meeting.title.ilike(f"%{search}%")) |
            (Meeting.discussion_summary.ilike(f"%{search}%")) |
            (Meeting.key_decisions.ilike(f"%{search}%")) |
            (Meeting.action_items.ilike(f"%{search}%")) |
            (Meeting.participant_observations.ilike(f"%{search}%")) |
            (Participant.name.ilike(f"%{search}%"))
        ).distinct()
    meetings = query.order_by(Meeting.date.desc()).all()
    return render_template("meetings/meetings.html", meetings=meetings, search=search)


@meetings_bp.route("/meetings/create", methods=["GET", "POST"])
@login_required
def create_meeting():
    participants = Participant.query.filter_by(user_id=current_user.id).all()
    if request.method == "POST":
        meeting = Meeting(
            user_id=current_user.id,
            title=request.form.get("title"),
            date=datetime.strptime(request.form.get("date"), "%Y-%m-%d"),
            discussion_summary=request.form.get("discussion_summary"),
            key_decisions=request.form.get("key_decisions"),
            action_items=request.form.get("action_items"),
            participant_observations=request.form.get("participant_observations"),
        )
        db.session.add(meeting)
        db.session.flush()

        participant_ids = request.form.getlist("participants")
        for pid in participant_ids:
            mp = MeetingParticipant(meeting_id=meeting.id, participant_id=int(pid))
            db.session.add(mp)

        db.session.commit()
        flash("Meeting created", "success")
        return redirect(url_for("meetings.list_meetings"))
    return render_template("meetings/create_meeting.html", participants=participants)


@meetings_bp.route("/meetings/<int:id>")
@login_required
def meeting_details(id):
    meeting = Meeting.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return render_template("meetings/meeting_details.html", meeting=meeting)


@meetings_bp.route("/meetings/<int:id>/analyze", methods=["POST"])
@login_required
def analyze_meeting(id):
    meeting = Meeting.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    engine = MemoryEngine()
    from ai.action_item_extractor import ActionItemExtractor
    from services.action_item_service import ActionItemService
    extractor = ActionItemExtractor()
    try:
        saved_memories = engine.save_memories(meeting)
        
        text_to_extract = f"Discussion Summary:\n{meeting.discussion_summary or ''}\n\nAction Items:\n{meeting.action_items or ''}"
        extracted_actions = extractor.extract(text_to_extract)
        
        participants_map = {}
        for mp in meeting.participants:
            if mp.participant:
                participants_map[mp.participant.name.strip().lower()] = mp.participant.id
                
        saved_actions = []
        for item in extracted_actions:
            owner = item.get("owner")
            participant_id = None
            if owner:
                owner_lower = owner.strip().lower()
                if owner_lower in participants_map:
                    participant_id = participants_map[owner_lower]
                else:
                    for p_name, p_id in participants_map.items():
                        if p_name in owner_lower or owner_lower in p_name:
                            participant_id = p_id
                            break
            
            ActionItemService.create(
                meeting_id=meeting.id,
                user_id=current_user.id,
                task=item["task"],
                owner=owner,
                deadline=item.get("deadline"),
                participant_id=participant_id
            )
            saved_actions.append(item)
            
        flash(f"Extracted and saved {len(saved_memories)} memories and {len(saved_actions)} action items.", "success")
    except Exception as e:
        flash(f"Failed to analyze meeting: {str(e)}", "danger")
    return redirect(url_for("meetings.meeting_details", id=id))


@meetings_bp.route("/meetings/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_meeting(id):
    meeting = Meeting.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    participants = Participant.query.filter_by(user_id=current_user.id).all()
    selected_participant_ids = [mp.participant_id for mp in meeting.participants]
    if request.method == "POST":
        meeting.title = request.form.get("title")
        meeting.date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")
        meeting.discussion_summary = request.form.get("discussion_summary")
        meeting.key_decisions = request.form.get("key_decisions")
        meeting.action_items = request.form.get("action_items")
        meeting.participant_observations = request.form.get("participant_observations")
        MeetingParticipant.query.filter_by(meeting_id=meeting.id).delete()
        participant_ids = request.form.getlist("participants")
        for pid in participant_ids:
            mp = MeetingParticipant(meeting_id=meeting.id, participant_id=int(pid))
            db.session.add(mp)
        db.session.commit()
        flash("Meeting updated", "success")
        return redirect(url_for("meetings.list_meetings"))
    return render_template("meetings/edit_meeting.html", meeting=meeting, participants=participants, selected_participant_ids=selected_participant_ids)


@meetings_bp.route("/meetings/<int:id>/delete")
@login_required
def delete_meeting(id):
    meeting = Meeting.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    MeetingParticipant.query.filter_by(meeting_id=meeting.id).delete()
    db.session.delete(meeting)
    db.session.commit()
    flash("Meeting deleted", "success")
    return redirect(url_for("meetings.list_meetings"))
