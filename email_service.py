import resend
import os
from datetime import date, datetime

# Load .env file if present
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
STAFF_EMAIL = os.environ.get("STAFF_EMAIL", "priyaobhinni1226@gmail.com")

# Resend requires a verified sender — for demo we use their sandbox address
# Once you verify a domain, change this to: grants@maryshouse.org.au
FROM_EMAIL = "FundMatch <onboarding@resend.dev>"


def _configure():
    resend.api_key = RESEND_API_KEY


def _score_color(score: int) -> str:
    if score >= 70:
        return "#00A99D"
    if score >= 40:
        return "#F59E0B"
    return "#94A3B8"


def _band_label(band: str) -> str:
    return {"green": "Escalate to Staff", "yellow": "Monitor", "grey": "Auto-archived"}.get(band, band)


def send_grant_alert(grant: dict, base_url: str = "http://localhost:5000") -> bool:
    """Send an instant alert email when a high-fit grant is discovered."""
    if not RESEND_API_KEY:
        print("[Email] No API key set — skipping alert email")
        return False

    _configure()
    score = grant.get("fit_score", 0)
    color = _score_color(score)
    deadline = grant.get("deadline", "")
    deadline_display = deadline if deadline and deadline not in ["ongoing", "rolling", ""] else "Ongoing / Rolling"
    amount = ""
    if grant.get("amount_max"):
        amount = f"Up to ${grant['amount_max']:,}"
    elif grant.get("amount_min"):
        amount = f"From ${grant['amount_min']:,}"

    grant_url = f"{base_url}/grant/{grant['id']}"
    draft_url = f"{base_url}/draft/{grant['id']}"

    html = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background: #F0F4F8; padding: 32px 16px; }}
    .container {{ max-width: 560px; margin: 0 auto; }}
    .header {{ background: #1B2B3B; border-radius: 16px 16px 0 0; padding: 28px 32px; text-align: center; }}
    .header-logo {{ display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 8px; }}
    .logo-icon {{ width: 36px; height: 36px; background: {color}; border-radius: 10px; display: flex; align-items: center; justify-content: center; }}
    .card {{ background: white; padding: 32px; border-left: 1px solid #E2E8F0; border-right: 1px solid #E2E8F0; }}
    .score-badge {{ display: inline-block; background: {color}20; color: {color}; border: 2px solid {color}40; border-radius: 12px; padding: 12px 20px; font-size: 28px; font-weight: 800; margin: 20px 0 8px; }}
    .score-label {{ color: {color}; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; }}
    .grant-title {{ font-size: 20px; font-weight: 700; color: #1B2B3B; margin: 20px 0 6px; line-height: 1.3; }}
    .funder {{ color: #64748B; font-size: 14px; margin-bottom: 24px; }}
    .meta-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 20px 0 28px; }}
    .meta-item {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 14px; }}
    .meta-label {{ font-size: 10px; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }}
    .meta-value {{ font-size: 15px; font-weight: 700; color: #1B2B3B; }}
    .btn-primary {{ display: block; background: {color}; color: white; text-decoration: none; text-align: center; padding: 14px 24px; border-radius: 12px; font-weight: 700; font-size: 15px; margin-bottom: 10px; }}
    .btn-secondary {{ display: block; background: white; color: #1B2B3B; text-decoration: none; text-align: center; padding: 13px 24px; border-radius: 12px; font-weight: 600; font-size: 14px; border: 2px solid #E2E8F0; }}
    .warning {{ background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 14px 16px; margin-top: 24px; }}
    .warning-text {{ color: #92400E; font-size: 12px; line-height: 1.5; }}
    .footer {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-top: none; border-radius: 0 0 16px 16px; padding: 20px 32px; text-align: center; }}
    .footer-text {{ color: #94A3B8; font-size: 11px; line-height: 1.6; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-logo">
        <div style="width:36px;height:36px;background:{color};border-radius:10px;display:inline-flex;align-items:center;justify-content:center;">
          <span style="color:white;font-size:18px;">✓</span>
        </div>
        <div style="text-align:left;">
          <div style="color:white;font-weight:700;font-size:16px;">FundMatch</div>
          <div style="color:#00A99D;font-size:11px;opacity:0.85;">for Mary's House</div>
        </div>
      </div>
      <div style="color:#94A3B8;font-size:13px;margin-top:4px;">New High-Fit Grant Discovered</div>
    </div>

    <div class="card">
      <div style="text-align:center;">
        <div class="score-badge">{score}</div>
        <div class="score-label">Fit Score · {_band_label(grant.get('fit_band',''))}</div>
      </div>

      <div class="grant-title">{grant.get('title','')}</div>
      <div class="funder">{grant.get('funder','')}</div>

      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">💰 Funding Amount</div>
          <div class="meta-value">{amount or 'See funder'}</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">📅 Deadline</div>
          <div class="meta-value">{deadline_display}</div>
        </div>
        <div class="meta-item" style="grid-column:1/-1;">
          <div class="meta-label">📍 Geography</div>
          <div class="meta-value" style="font-size:13px;">{grant.get('geography','—')}</div>
        </div>
      </div>

      <a href="{draft_url}" class="btn-primary">✍️ Generate Application Draft</a>
      <a href="{grant_url}" class="btn-secondary">View Full Prospect Details</a>

      <div class="warning">
        <div class="warning-text">
          ⚠️ <strong>Staff action required.</strong> FundMatch has identified this as a strong match for Mary's House.
          Review the full details and generate a draft — no submission happens without your sign-off.
        </div>
      </div>
    </div>

    <div class="footer">
      <div class="footer-text">
        This alert was sent by FundMatch · Built for Mary's House<br>
        Fit score {score}/100 · Discovered {date.today().strftime('%d %B %Y')}<br>
        <span style="color:#CBD5E1;">All grant applications require human verification before submission.</span>
      </div>
    </div>
  </div>
</body>
</html>
"""

    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [STAFF_EMAIL],
            "subject": f"FundMatch Alert: New {score}/100 Grant — {grant.get('title','')[:50]}",
            "html": html,
        })
        print(f"[Email] Alert sent to {STAFF_EMAIL} for grant: {grant.get('title')}")
        return True
    except Exception as e:
        print(f"[Email] Failed to send alert: {e}")
        return False


def send_weekly_digest(grants: list, base_url: str = "http://localhost:5000") -> bool:
    """Send a weekly digest of all active prospects ranked by fit score."""
    if not RESEND_API_KEY:
        print("[Email] No API key set — skipping digest email")
        return False

    _configure()
    green = [g for g in grants if g.get("fit_band") == "green"]
    yellow = [g for g in grants if g.get("fit_band") == "yellow"]
    today = date.today().strftime("%d %B %Y")

    def grant_row(g):
        score = g.get("fit_score", 0)
        color = _score_color(score)
        band = g.get("fit_band", "")
        deadline = g.get("deadline", "")
        deadline_str = deadline if deadline and deadline not in ["ongoing", "rolling", ""] else "Ongoing"
        amount = f"${g['amount_max']:,}" if g.get("amount_max") else "—"
        return f"""
        <tr style="border-bottom:1px solid #F1F5F9;">
          <td style="padding:14px 16px;">
            <div style="font-weight:600;color:#1B2B3B;font-size:14px;margin-bottom:2px;">{g['title'][:52]}{'…' if len(g['title'])>52 else ''}</div>
            <div style="font-size:12px;color:#94A3B8;">{g['funder'][:45]}{'…' if len(g['funder'])>45 else ''}</div>
          </td>
          <td style="padding:14px 8px;text-align:center;">
            <span style="background:{color}20;color:{color};border:1px solid {color}40;border-radius:8px;padding:4px 10px;font-weight:700;font-size:13px;">{score}</span>
          </td>
          <td style="padding:14px 8px;text-align:center;font-size:13px;color:#475569;">{amount}</td>
          <td style="padding:14px 16px;text-align:center;font-size:13px;color:#475569;">{deadline_str}</td>
          <td style="padding:14px 16px;text-align:right;">
            <a href="{base_url}/draft/{g['id']}" style="background:{color};color:white;text-decoration:none;padding:6px 14px;border-radius:8px;font-size:12px;font-weight:600;">Draft</a>
          </td>
        </tr>"""

    green_rows = "".join(grant_row(g) for g in green)
    yellow_rows = "".join(grant_row(g) for g in yellow)

    def section(title, color, rows, count):
        if not rows:
            return ""
        return f"""
        <div style="margin-bottom:28px;">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
            <div style="width:10px;height:10px;background:{color};border-radius:50%;"></div>
            <span style="font-weight:700;color:#1B2B3B;font-size:14px;text-transform:uppercase;letter-spacing:0.05em;">{title}</span>
            <span style="background:{color}20;color:{color};border-radius:6px;padding:2px 8px;font-size:11px;font-weight:700;">{count}</span>
          </div>
          <table style="width:100%;border-collapse:collapse;border:1px solid #E2E8F0;border-radius:12px;overflow:hidden;">
            <thead>
              <tr style="background:#F8FAFC;">
                <th style="padding:10px 16px;text-align:left;font-size:11px;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">Grant</th>
                <th style="padding:10px 8px;text-align:center;font-size:11px;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">Fit</th>
                <th style="padding:10px 8px;text-align:center;font-size:11px;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">Amount</th>
                <th style="padding:10px 16px;text-align:center;font-size:11px;color:#94A3B8;font-weight:700;text-transform:uppercase;letter-spacing:0.06em;">Deadline</th>
                <th style="padding:10px 16px;"></th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>"""

    html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Inter',sans-serif;background:#F0F4F8;padding:32px 16px;margin:0;">
  <div style="max-width:620px;margin:0 auto;">

    <div style="background:#1B2B3B;border-radius:16px 16px 0 0;padding:28px 32px;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <div style="width:40px;height:40px;background:#00A99D;border-radius:10px;display:flex;align-items:center;justify-content:center;">
          <span style="color:white;font-size:20px;">✓</span>
        </div>
        <div>
          <div style="color:white;font-weight:800;font-size:18px;">FundMatch</div>
          <div style="color:#00A99D;font-size:12px;">for Mary's House</div>
        </div>
      </div>
      <div style="color:white;font-weight:700;font-size:22px;margin-bottom:4px;">Weekly Grant Digest</div>
      <div style="color:#94A3B8;font-size:14px;">{today} · {len(green)+len(yellow)} active prospects ranked by fit score</div>
    </div>

    <div style="background:white;padding:32px;border-left:1px solid #E2E8F0;border-right:1px solid #E2E8F0;">

      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-bottom:28px;">
        <div style="background:#F0FDF4;border:1px solid #BBF7D0;border-radius:12px;padding:16px;text-align:center;">
          <div style="font-size:28px;font-weight:800;color:#15803D;">{len(green)}</div>
          <div style="font-size:11px;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">Escalate to Staff</div>
        </div>
        <div style="background:#FFFBEB;border:1px solid #FDE68A;border-radius:12px;padding:16px;text-align:center;">
          <div style="font-size:28px;font-weight:800;color:#D97706;">{len(yellow)}</div>
          <div style="font-size:11px;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">Monitoring</div>
        </div>
        <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:12px;padding:16px;text-align:center;">
          <div style="font-size:28px;font-weight:800;color:#1B2B3B;">{len(grants)}</div>
          <div style="font-size:11px;color:#64748B;font-weight:600;text-transform:uppercase;letter-spacing:0.06em;">Total Discovered</div>
        </div>
      </div>

      {section("Escalate to Staff", "#00A99D", green_rows, len(green))}
      {section("Monitoring", "#F59E0B", yellow_rows, len(yellow))}

      <div style="text-align:center;margin-top:28px;">
        <a href="{base_url}" style="display:inline-block;background:#1B2B3B;color:white;text-decoration:none;padding:14px 32px;border-radius:12px;font-weight:700;font-size:15px;">
          Open FundMatch Dashboard →
        </a>
      </div>
    </div>

    <div style="background:#F8FAFC;border:1px solid #E2E8F0;border-top:none;border-radius:0 0 16px 16px;padding:20px 32px;text-align:center;">
      <div style="color:#94A3B8;font-size:11px;line-height:1.6;">
        FundMatch Weekly Digest · Mary's House Grant Research Pipeline<br>
        All applications require human review and sign-off before submission.
      </div>
    </div>

  </div>
</body>
</html>"""

    try:
        resend.Emails.send({
            "from": FROM_EMAIL,
            "to": [STAFF_EMAIL],
            "subject": f"FundMatch Weekly Digest — {len(green)+len(yellow)} prospects ready for review · {today}",
            "html": html,
        })
        print(f"[Email] Digest sent to {STAFF_EMAIL} ({len(green)+len(yellow)} prospects)")
        return True
    except Exception as e:
        print(f"[Email] Failed to send digest: {e}")
        return False
