import json
from flask import Flask, render_template, redirect, url_for, jsonify, request
from database import (init_db, get_all_grants, get_grant, update_pipeline_stage,
                      get_grants_by_stage)
from scraper import run_scrape, get_status
from signals import get_donor_signals
from drafter import generate_draft
from knowledge_base import MARY_HOUSE
from email_service import send_grant_alert, send_weekly_digest, STAFF_EMAIL

app = Flask(__name__)


@app.route("/")
def dashboard():
    grants = get_all_grants(include_archived=False)
    green = [g for g in grants if g["fit_band"] == "green"]
    yellow = [g for g in grants if g["fit_band"] == "yellow"]
    all_with_archived = get_all_grants(include_archived=True)
    archived = [g for g in all_with_archived if g["fit_band"] == "grey"]
    donors = get_donor_signals()
    next_deadline = _next_deadline(grants)
    return render_template(
        "dashboard.html",
        grants=grants,
        green_count=len(green),
        yellow_count=len(yellow),
        archived_count=len(archived),
        total_count=len(all_with_archived),
        donors=donors,
        next_deadline=next_deadline,
        staff_email=STAFF_EMAIL,
    )


@app.route("/knowledge")
def knowledge():
    return render_template("knowledge.html", kb=MARY_HOUSE)


@app.route("/search")
def search():
    run_scrape()
    status = get_status()
    grants = get_all_grants(include_archived=True)
    return render_template("search.html", status=status, grants=grants)


@app.route("/search/status")
def search_status():
    return jsonify(get_status())


@app.route("/grants")
def grants_list():
    all_grants = get_all_grants(include_archived=True)
    green = [g for g in all_grants if g["fit_band"] == "green"]
    yellow = [g for g in all_grants if g["fit_band"] == "yellow"]
    grey = [g for g in all_grants if g["fit_band"] == "grey"]
    return render_template("grants.html", green=green, yellow=yellow, grey=grey, total=len(all_grants))


@app.route("/grant/<int:grant_id>")
def grant_detail(grant_id):
    grant = get_grant(grant_id)
    if not grant:
        return redirect(url_for("dashboard"))
    scoring = json.loads(grant.get("score_breakdown") or "{}")
    return render_template("grant_detail.html", grant=grant, scoring=scoring)


@app.route("/signals")
def signals():
    donors = get_donor_signals()
    return render_template("signals.html", donors=donors)


@app.route("/draft/<int:grant_id>")
def draft(grant_id):
    grant = get_grant(grant_id)
    if not grant:
        return redirect(url_for("dashboard"))
    draft_data = generate_draft(grant)
    return render_template("draft.html", grant=grant, draft=draft_data)


# ── Pipeline Kanban ──────────────────────────────────────────────────────────

@app.route("/pipeline")
def pipeline():
    stages = get_grants_by_stage()
    return render_template("pipeline.html", stages=stages)


@app.route("/pipeline/update", methods=["POST"])
def pipeline_update():
    data = request.get_json()
    grant_id = data.get("grant_id")
    stage = data.get("stage")
    valid_stages = ["discovered", "shortlisted", "drafting", "submitted", "won", "lost"]
    if grant_id and stage in valid_stages:
        update_pipeline_stage(int(grant_id), stage)
        return jsonify({"ok": True})
    return jsonify({"ok": False, "error": "Invalid stage"}), 400


# ── Email routes ─────────────────────────────────────────────────────────────

@app.route("/email/alert/<int:grant_id>", methods=["POST"])
def email_alert(grant_id):
    grant = get_grant(grant_id)
    if not grant:
        return jsonify({"ok": False, "error": "Grant not found"}), 404
    base_url = request.host_url.rstrip("/")
    ok = send_grant_alert(grant, base_url)
    return jsonify({"ok": ok, "to": STAFF_EMAIL})


@app.route("/email/digest", methods=["POST"])
def email_digest():
    grants = get_all_grants(include_archived=False)
    base_url = request.host_url.rstrip("/")
    ok = send_weekly_digest(grants, base_url)
    return jsonify({"ok": ok, "to": STAFF_EMAIL, "count": len(grants)})


# ── Helpers ──────────────────────────────────────────────────────────────────

def _next_deadline(grants):
    from datetime import datetime, date
    soonest, soonest_title = None, ""
    for g in grants:
        dl = g.get("deadline", "")
        if not dl or dl.lower() in ("ongoing", "rolling", "eoi", ""):
            continue
        try:
            d = datetime.strptime(dl, "%Y-%m-%d").date()
            if d >= date.today() and (soonest is None or d < soonest):
                soonest, soonest_title = d, g.get("title", "")
        except ValueError:
            continue
    if soonest:
        return {"date": soonest.strftime("%d %B %Y").lstrip("0"), "title": soonest_title}
    return None


if __name__ == "__main__":
    init_db()
    print("\n  FundMatch is running at http://localhost:5000\n")
    app.run(debug=True, port=5000)
