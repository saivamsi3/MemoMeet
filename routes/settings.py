from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from main import db

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings")
@login_required
def index():
    return render_template("settings/settings.html")


@settings_bp.route("/settings/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        current_user.username = request.form.get("username", current_user.username)
        current_user.email = request.form.get("email", current_user.email)
        db.session.commit()
        flash("Account settings updated", "success")
        return redirect(url_for("settings.account"))
    return render_template("settings/account.html")


@settings_bp.route("/settings/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    if request.method == "POST":
        current_user.theme = request.form.get("theme", "light")
        db.session.commit()
        flash("Preferences updated", "success")
        return redirect(url_for("settings.preferences"))
    return render_template("settings/preferences.html")


@settings_bp.route("/settings/integrations")
@login_required
def integrations():
    return render_template("settings/integrations.html")
