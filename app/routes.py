import secrets
from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template_string, request, url_for

from .models import Message, db

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    # render template from templates/index.html
    return render_template_string(
        open("app/templates/index.html", "r", encoding="utf-8").read()
    )


@bp.route("/create", methods=["POST"])
def create():
    data = request.get_json() or {}
    encrypted = data.get("encrypted_msg")
    lifetime = data.get("lifetime", "day")
    webhook = data.get("notify_webhook")
    if not encrypted:
        return jsonify({"error": "encrypted_msg required"}), 400

    lifetimes = {"hour": 1, "day": 24, "week": 24 * 7}
    hours = lifetimes.get(lifetime, 24)
    msg = Message(
        token=secrets.token_urlsafe(20),
        encrypted=encrypted,
        expires_at=datetime.utcnow() + timedelta(hours=hours),
        views_left=1,
        webhook=webhook,
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"url": url_for("main.view", token=msg.token, _external=True)})

@bp.route("/m/<token>")
def view(token):
    msg = Message.query.filter_by(token=token).first()
    if not msg:
        return "<h3>Not found or expired</h3>", 404
    return f"<h3>Encrypted: {msg.encrypted}</h3>"
