from flask import Blueprint, render_template, request, send_file, flash, redirect, url_for
from flask_login import login_required, current_user
from models.participant import Participant
from models.meeting import Meeting
from models.memory import Memory
from ai.preparation_engine import PreparationEngine
from services.pdf_service import PDFService

reports_bp = Blueprint("reports", __name__)


@reports_bp.route("/reports/preparation/<int:meeting_id>", methods=["GET", "POST"])
@login_required
def preparation_report(meeting_id):
    meeting = Meeting.query.filter_by(id=meeting_id, user_id=current_user.id).first_or_404()
    engine = PreparationEngine()
    # determine selected participants and options
    if request.method == "POST":
        selected = request.form.getlist("participants")
        sections = request.form.getlist("sections")
        limit = int(request.form.get("limit") or 10)
        output = request.form.get("output_format") or "print"
        participant_reports = []
        for mp in meeting.participants:
            if not mp.participant:
                continue
            if selected and str(mp.participant.id) not in selected:
                continue
            try:
                report_text = engine.generate_report(mp.participant, current_user.id)
            except Exception:
                report_text = engine._generate_fallback(mp.participant, None, [], [])
            participant_reports.append({"participant": mp.participant, "report": report_text})

        if output == "pdf" and participant_reports:
            # build PDF content sections
            sections_for_pdf = []
            for pr in participant_reports:
                title = f"Preparation: {pr['participant'].name}"
                body = pr['report']
                sections_for_pdf.append((title, body))
            pdf_buffer = PDFService.generate_report(f"Preparation Report - {meeting.title}", sections_for_pdf)
            return send_file(pdf_buffer, as_attachment=True, download_name=f"preparation_{meeting.id}.pdf", mimetype='application/pdf')

        return render_template("reports/preparation_report.html", meeting=meeting, participant_reports=participant_reports)

    # GET default: generate reports for all participants
    participant_reports = []
    for mp in meeting.participants:
        if not mp.participant:
            continue
        try:
            report_text = engine.generate_report(mp.participant, current_user.id)
        except Exception:
            report_text = engine._generate_fallback(mp.participant, None, [], [])
        participant_reports.append({"participant": mp.participant, "report": report_text})
    return render_template("reports/preparation_report.html", meeting=meeting, participant_reports=participant_reports)


@reports_bp.route("/reports/participant/<int:participant_id>")
@login_required
def participant_report(participant_id):
    participant = Participant.query.filter_by(id=participant_id, user_id=current_user.id).first_or_404()
    memories = Memory.query.filter_by(participant_id=participant_id, user_id=current_user.id).all()
    return render_template("reports/participant_report.html", participant=participant, memories=memories)
