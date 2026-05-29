from datetime import datetime, date
from knowledge_base import MARY_HOUSE

CAUSE_KEYWORDS = set(k.lower() for k in MARY_HOUSE["scoring_keywords"]["cause"])
PROJECT_KEYWORDS = set(k.lower() for k in MARY_HOUSE["scoring_keywords"]["project_type"])
SA_KEYWORDS = {"south australia", "sa ", " sa,", "adelaide", "statewide sa"}
NATIONAL_KEYWORDS = {"national", "australia-wide", "all states", "australian"}

def _cause_score(grant: dict) -> tuple[int, str]:
    text = (
        (grant.get("title") or "") + " " +
        (grant.get("description") or "") + " " +
        (grant.get("focus_areas") or "")
    ).lower()
    hits = sum(1 for kw in CAUSE_KEYWORDS if kw in text)
    if hits >= 4:
        return 30, "Strong cause alignment (DV/women's safety/children)"
    if hits >= 2:
        return 20, "Moderate cause alignment"
    if hits >= 1:
        return 10, "Weak cause alignment"
    return 0, "No cause alignment detected"

def _geo_score(grant: dict) -> tuple[int, str]:
    text = (
        (grant.get("eligibility") or "") + " " +
        (grant.get("description") or "") + " " +
        (grant.get("geography") or "")
    ).lower()
    for kw in SA_KEYWORDS:
        if kw in text:
            return 20, "South Australia eligible"
    for kw in NATIONAL_KEYWORDS:
        if kw in text:
            return 15, "National/Australia-wide — Mary's House eligible"
    return 5, "Geographic eligibility unclear — check funder website"

def _size_score(grant: dict) -> tuple[int, str]:
    text = (
        (grant.get("eligibility") or "") + " " +
        (grant.get("description") or "")
    ).lower()
    small_terms = ["small organisation", "community organisation", "not-for-profit", "nfp",
                   "charity", "charitable", "any organisation", "all organisations"]
    large_only = ["university", "hospital", "local government only", "government body"]
    if any(t in text for t in large_only):
        return 2, "Likely restricted to large/government bodies"
    if any(t in text for t in small_terms):
        return 15, "Open to small community organisations"
    return 8, "Organisation size eligibility unconfirmed"

def _project_score(grant: dict) -> tuple[int, str]:
    text = (
        (grant.get("title") or "") + " " +
        (grant.get("description") or "") + " " +
        (grant.get("focus_areas") or "")
    ).lower()
    if any(kw in text for kw in ["refuge", "crisis", "accommodation", "shelter"]):
        return 20, "Directly funds refuge/crisis accommodation"
    if any(kw in text for kw in ["outreach", "prevention", "counselling", "support services", "community"]):
        return 15, "Funds community support/prevention programs"
    if "women" in text or "family" in text:
        return 10, "Relevant to women/family programs"
    return 5, "General funding — project fit unconfirmed"

def _deadline_score(grant: dict) -> tuple[int, str]:
    raw = grant.get("deadline") or ""
    if not raw or raw.lower() in ("ongoing", "rolling", "eoi", ""):
        return 12, "Rolling/ongoing — apply when ready"
    try:
        deadline = datetime.strptime(raw, "%Y-%m-%d").date()
        today = date.today()
        days = (deadline - today).days
        if days < 0:
            return 0, "Deadline passed"
        if days >= 56:
            return 15, f"{days} days remaining — strong feasibility"
        if days >= 28:
            return 10, f"{days} days remaining — feasible with prompt action"
        return 3, f"Only {days} days remaining — very tight"
    except ValueError:
        return 8, "Deadline format unclear — verify manually"

def score_grant(grant: dict) -> dict:
    cause_pts, cause_note = _cause_score(grant)
    geo_pts, geo_note = _geo_score(grant)
    size_pts, size_note = _size_score(grant)
    project_pts, project_note = _project_score(grant)
    deadline_pts, deadline_note = _deadline_score(grant)

    total = cause_pts + geo_pts + size_pts + project_pts + deadline_pts

    if total >= 70:
        band = "green"
        action = "Escalate to staff"
    elif total >= 40:
        band = "yellow"
        action = "Monitor"
    else:
        band = "grey"
        action = "Auto-archive"

    return {
        "total": total,
        "band": band,
        "action": action,
        "breakdown": {
            "cause": {"score": cause_pts, "max": 30, "note": cause_note},
            "geography": {"score": geo_pts, "max": 20, "note": geo_note},
            "org_size": {"score": size_pts, "max": 15, "note": size_note},
            "project_type": {"score": project_pts, "max": 20, "note": project_note},
            "deadline": {"score": deadline_pts, "max": 15, "note": deadline_note},
        },
    }
