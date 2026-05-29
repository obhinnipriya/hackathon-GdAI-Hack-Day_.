# FundMatch — AI Grant Research Pipeline for Mary's House

Built at the Mary's House Hackathon 2025.

FundMatch is an internal grant research and writing tool built specifically for Mary's House. It replaces hours of manual searching with an automated 5-layer pipeline — finding Australian grants, scoring eligibility, monitoring philanthropic signals, generating application drafts, and tracking every prospect through to submission.

---

## The 5-Layer Pipeline

| Layer | What it does |
|---|---|
| **1 — Know** | Loads the Mary's House knowledge base — ACNC registration, programs, client demographics, staff capacity, and past funded projects. This powers all scoring and drafting. |
| **2 — Search** | Crawls GrantConnect (grants.gov.au) and SA Government portals in real time, plus a curated database of 10 real Australian foundations. |
| **3 — Score** | Scores every grant 0–100 across 5 dimensions against the Mary's House profile. Anything ≥70 is escalated to staff. Anything below 40 is auto-archived. |
| **4 — Signal** | Monitors philanthropists and corporates actively signalling interest in DV, women's safety, and children's welfare — so staff know who to approach before a grant even opens. |
| **5 — Draft** | Generates a full 6-section application draft using the knowledge base and grant criteria. Every claim is footnoted with its source. Nothing is submitted without staff sign-off. |

---

## Features

### Grant Discovery
- Live scraping of GrantConnect (grants.gov.au) and SA Government grant portals
- Curated database of 10 real Australian foundations including Paul Ramsay Foundation, FRRR, Perpetual, Gandel Foundation, Channel 7 Telethon Trust (SA), ANROWS, and more
- All discovered grants automatically scored and ranked on arrival

### Eligibility Scoring Engine
- 5-dimension scoring: cause alignment (30pts), geographic eligibility (20pts), organisation size fit (15pts), project type match (20pts), deadline feasibility (15pts)
- Colour-coded results: green ≥70 (escalate), amber 40–69 (monitor), grey <40 (auto-archive)
- Full score breakdown shown per grant with plain-English reasoning

### Grant Pipeline — Kanban Board
- Drag-and-drop board with 6 stages: Discovered → Shortlisted → Drafting → Submitted → Won → Lost
- Stage updates persist to database in real time
- Toast notification confirms every move

### Philanthropic Signal Monitoring
- 5 live philanthropic signals from real organisations (ANZ Foundation, Our Watch, Lord Mayor's Charitable Foundation, Minderoo Foundation, Gandel Foundation)
- Each signal links to the real source page
- Shows relevance to Mary's House and recommended next action

### AI Application Draft Generator
- One-click draft generation for any shortlisted grant
- 6 sections: Organisation Overview, Need Statement, Project Description, Budget Narrative, Outcomes & Evaluation, Track Record
- Every claim sourced and footnoted
- Staff review checklist built into the draft page
- Print / Export to PDF built in
- Human sign-off banner — nothing is submitted without staff approval

### Email Notifications via Resend
- Instant staff alert email when a grant scores ≥70 — shows score, funder, amount, deadline, and direct links to view and draft
- One-click weekly digest email — ranked HTML table of all active prospects delivered to staff inbox
- Both emails use Mary's House branding

### Dashboard
- Ranked prospects table with live deadline countdown badges (turns amber <30 days, red <7 days)
- Stats summary: total grants found, escalate count, monitoring count, next deadline
- Philanthropic signals sidebar showing latest 3 donor signals
- Send Digest button and Run New Search button

### Design
- Mary's House Services branding — official logo (white + colour) served locally
- Mary's House colour palette: dark navy (#1B2B3B) + teal (#00A99D)
- Phosphor Icons throughout
- Inter font
- Smooth fade-in and slide-up animations, card hover transitions, pulse indicators

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 / Flask |
| Database | SQLite (auto-created on first run) |
| Frontend | Jinja2 templates + Tailwind CSS (CDN) + Phosphor Icons |
| Email | Resend API |
| Scraping | requests + BeautifulSoup |
| Signal feeds | feedparser (RSS) |

---

## Setup

**1. Clone the repo**
```
git clone https://github.com/obhinnipriya/hackathon-GdAI-Hack-Day_.git
cd hackathon-GdAI-Hack-Day_.
```

**2. Install dependencies**
```
pip install -r requirements.txt
```

**3. Add your Resend API key**

Create a `.env` file in the project root:
```
RESEND_API_KEY=re_your_key_here
STAFF_EMAIL=your@email.com
```

Get a free API key at resend.com — free tier allows 3,000 emails/month.
Without a key the app still runs fully; email buttons show a "no key" toast.

**4. Run the app**
```
python app.py
```

Open **http://localhost:5000**

The database seeds automatically on first run — no setup needed.

---

## Project Structure

```
fundmatch/
├── app.py                # Flask routes + app entry point
├── knowledge_base.py     # Mary's House profile (ACNC, programs, demographics)
├── scorer.py             # 5-dimension fit scoring engine
├── scraper.py            # Live grant scraper (GrantConnect + SA Gov)
├── signals.py            # Philanthropic signal data + RSS monitoring
├── drafter.py            # 6-section application draft generator
├── email_service.py      # Resend alert + weekly digest emails
├── database.py           # SQLite init + 10 seeded Australian grants
├── requirements.txt      # Python dependencies
├── templates/
│   ├── base.html         # Nav layout with MHS logos + Phosphor Icons
│   ├── dashboard.html    # Main prospects dashboard
│   ├── knowledge.html    # Mary's House knowledge base view
│   ├── search.html       # Live grant search + results
│   ├── grants.html       # All scored prospects (green / amber / grey)
│   ├── grant_detail.html # Single grant — score breakdown + checklist
│   ├── signals.html      # Philanthropic signal monitoring
│   ├── pipeline.html     # Drag-and-drop Kanban pipeline board
│   └── draft.html        # AI-generated draft + source audit trail
└── static/
    ├── mhs-logo-white.svg   # Mary's House Services logo (white)
    ├── mhs-logo-colour.svg  # Mary's House Services logo (colour)
    └── style.css
```

---

## Demo Flow

1. **Dashboard** — show ranked prospects, live deadline countdowns, philanthropic signals sidebar
2. **Knowledge Base** — show the Mary's House profile powering all scoring and drafting
3. **Search** — trigger live scrape, watch new grants arrive and get scored
4. **Prospects** — show colour-coded scoring with green/amber/grey bands
5. **Grant Detail** — click any grant, show 5-dimension score breakdown and eligibility checklist
6. **Draft** — click Generate Draft, show full 6-section application with footnotes in seconds
7. **Pipeline** — drag a grant from Discovered → Shortlisted → Drafting, toast confirms the move
8. **Signals** — show 5 philanthropic signals with real source links
9. **Email** — click the envelope icon on a green grant, show branded alert landing in inbox live

---

## Scoring Dimensions

| Dimension | Max Points | How it works |
|---|---|---|
| Cause alignment | 30 | Keyword match against DV / women's safety / children's welfare |
| Geographic eligibility | 20 | SA-specific = 20, national = 15, other state = 5 |
| Organisation size fit | 15 | Community / small NFP = 15, any org = 8 |
| Project type match | 20 | Refuge / crisis = 20, community / prevention = 15, general = 5 |
| Deadline feasibility | 15 | >8 weeks = 15, 4–8 weeks = 10, <4 weeks = 3, closed = 0 |

---

## Seeded Australian Grants

10 real Australian funders pre-loaded with real URLs and deadlines:

- Australian Government — Families Safety Fund
- Australian Government — Strong and Resilient Communities
- SA Government — Community Benefit Fund
- Paul Ramsay Foundation — Breaking Cycles
- Helen Macpherson Smith Trust — Social Impact Grants
- Perpetual Foundation — IMPACT Philanthropy
- Foundation for Rural & Regional Renewal (FRRR)
- Channel 7 Telethon Trust (SA)
- Sidney Myer Fund — Social Innovation Grants
- ANROWS — Practice Grants

---

Built for Mary's House · Hackathon 2025
All drafts require human verification before submission — built into the architecture, not just a disclaimer.
