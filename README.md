# FundMatch — AI Grant Research Pipeline for Mary's House

Built at the Mary's House Hackathon 2025.

FundMatch is an internal grant research and writing tool that replaces hours of manual searching with an automated 5-layer pipeline — finding grants, scoring fit, monitoring donor signals, and generating application drafts for staff review.

---

## The 5-Layer Pipeline

| Layer | What it does |
|---|---|
| **Know** | Loads Mary's House profile — ACNC registration, programs, demographics, past grants |
| **Search** | Crawls GrantConnect (grants.gov.au) + curated Australian foundations |
| **Score** | Scores every grant 0–100 across 5 dimensions against Mary's House profile |
| **Signal** | Monitors philanthropists and corporates signalling interest in DV/women's safety |
| **Draft** | Generates a full 6-section application draft with source footnotes |

---

## Features

- Ranked grant prospects dashboard with fit score badges
- 5-dimension eligibility scoring (cause, geography, org size, project type, deadline)
- Grant pipeline Kanban board (Discovered → Shortlisted → Drafting → Submitted → Won/Lost)
- Philanthropic signal monitoring with real source links
- AI-generated application drafts with full audit trail
- Email alerts via Resend when high-fit grants are discovered
- Weekly digest email of all active prospects
- Live deadline countdown badges
- Mary's House brand design

---

## Tech Stack

- **Backend:** Python / Flask
- **Database:** SQLite
- **Frontend:** Jinja2 templates + Tailwind CSS + Phosphor Icons
- **Email:** Resend API
- **Scraping:** requests + BeautifulSoup

---

## Setup

**1. Clone the repo**
```
git clone https://github.com/YOUR_USERNAME/fundmatch.git
cd fundmatch
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

Get a free API key at resend.com

**4. Run the app**
```
python app.py
```

Open http://localhost:5000

---

## Project Structure

```
fundmatch/
├── app.py               # Flask routes
├── knowledge_base.py    # Mary's House profile data
├── scorer.py            # Fit scoring engine
├── scraper.py           # Grant discovery (live + curated)
├── signals.py           # Philanthropic signal monitoring
├── drafter.py           # Application draft generator
├── email_service.py     # Resend email alerts + digest
├── database.py          # SQLite setup + seed grants
├── requirements.txt
├── templates/           # HTML pages
└── static/              # Logos + CSS
```

---

## Demo Flow

1. **Dashboard** — ranked prospects with deadline countdowns
2. **Knowledge Base** — Mary's House profile powering all scoring
3. **Search** — trigger live grant scrape
4. **Prospects** — all grants scored and colour-coded
5. **Signals** — philanthropic monitoring with source links
6. **Pipeline** — drag-and-drop Kanban board
7. **Draft** — one-click application draft with footnotes
8. **Email** — live alert lands in staff inbox during demo

---

Built for Mary's House · All drafts require human sign-off before submission
