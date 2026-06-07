from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.action_item import ActionItem

action_items_bp = Blueprint("action_items", __name__)


@action_items_bp.route("/action-items")
@login_required
def list_action_items():
    status = request.args.get("status", "")
    query = ActionItem.query.filter_by(user_id=current_user.id)
    if status:
        query = query.filter_by(status=status)
    items = query.order_by(ActionItem.deadline.asc()).all()
    return render_template("action_items/action_items.html", items=items, status=status)


@action_items_bp.route("/action-items/<int:id>/status", methods=["POST"])
@login_required
def update_status(id):
    item = ActionItem.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    item.status = request.form.get("status", item.status)
    db.session.commit()
    flash("Status updated", "success")
    return redirect(url_for("action_items.list_action_items"))


@action_items_bp.route("/action-items/<int:id>/delete")
@login_required
def delete_action_item(id):
    item = ActionItem.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    flash("Action item deleted", "success")
    return redirect(url_for("action_items.list_action_items"))
