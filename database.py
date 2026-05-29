import sqlite3
import os
from scorer import score_grant

DB_PATH = os.path.join(os.path.dirname(__file__), "fundmatch.db")

SEED_GRANTS = [
    {
        "id": 1,
        "title": "Families Safety Fund",
        "funder": "Australian Government — Dept of Social Services",
        "amount_min": 50000,
        "amount_max": 500000,
        "deadline": "2026-08-15",
        "geography": "National — all Australian organisations eligible",
        "focus_areas": "domestic violence women's safety family violence crisis refuge support services",
        "eligibility": "Not-for-profit organisations and charities providing frontline DV services",
        "description": (
            "The Families Safety Fund supports frontline services for women and children "
            "experiencing domestic and family violence. Priority given to crisis accommodation, "
            "outreach, and wraparound support services. South Australia and national organisations eligible."
        ),
        "source_url": "https://www.dss.gov.au/our-responsibilities/families-and-children/programmes-services/family-safety",
        "source": "seed",
    },
    {
        "id": 2,
        "title": "Strong and Resilient Communities",
        "funder": "Australian Government — Dept of Social Services",
        "amount_min": 20000,
        "amount_max": 200000,
        "deadline": "2026-09-30",
        "geography": "National",
        "focus_areas": "community women children family safety social cohesion",
        "eligibility": "Not-for-profit organisations, charities, community organisations",
        "description": (
            "Supports community organisations delivering services that build stronger, safer "
            "communities. Eligible projects include women's safety, children's programs, and "
            "prevention of family violence."
        ),
        "source_url": "https://www.dss.gov.au/grants",
        "source": "seed",
    },
    {
        "id": 3,
        "title": "Community Benefit Fund — Priority Grants",
        "funder": "SA Government — Office for Recreation, Sport and Racing",
        "amount_min": 10000,
        "amount_max": 100000,
        "deadline": "2026-07-31",
        "geography": "South Australia — SA-based organisations only",
        "focus_areas": "community welfare women children safety south australia outreach support",
        "eligibility": "SA-based not-for-profit organisations serving disadvantaged communities",
        "description": (
            "SA Government priority grants for community organisations addressing disadvantage "
            "in South Australia. Eligible activities include women's safety services, "
            "crisis support, children's welfare, and community outreach programs."
        ),
        "source_url": "https://www.sa.gov.au/topics/arts-sport-and-recreation/grants-and-funding/community-benefit-fund",
        "source": "seed",
    },
    {
        "id": 4,
        "title": "Paul Ramsay Foundation — Breaking Cycles",
        "funder": "Paul Ramsay Foundation",
        "amount_min": 100000,
        "amount_max": 1000000,
        "deadline": "2026-10-01",
        "geography": "National — Australian organisations",
        "focus_areas": "disadvantage poverty children family women safety community prevention",
        "eligibility": "Charitable organisations addressing entrenched disadvantage in Australia",
        "description": (
            "The Breaking Cycles initiative funds organisations working to interrupt cycles of "
            "disadvantage. Priority areas include children's safety, family violence prevention, "
            "and community-based support for women experiencing crisis."
        ),
        "source_url": "https://paulramsayfoundation.org.au/our-grants/",
        "source": "seed",
    },
    {
        "id": 5,
        "title": "Helen Macpherson Smith Trust — Social Impact Grants",
        "funder": "Helen Macpherson Smith Trust",
        "amount_min": 30000,
        "amount_max": 150000,
        "deadline": "2026-08-01",
        "geography": "Victoria and South Australia",
        "focus_areas": "women children social impact community welfare counselling outreach",
        "eligibility": "Not-for-profit organisations in Victoria and South Australia",
        "description": (
            "Helen Macpherson Smith Trust funds social impact projects improving quality of life "
            "for women and children in Victoria and South Australia. Eligible projects include "
            "refuge services, outreach, counselling, and prevention programs."
        ),
        "source_url": "https://www.hmstrust.org.au/grants",
        "source": "seed",
    },
    {
        "id": 6,
        "title": "Perpetual Foundation — IMPACT Philanthropy",
        "funder": "Perpetual Foundation",
        "amount_min": 20000,
        "amount_max": 100000,
        "deadline": "ongoing",
        "geography": "National",
        "focus_areas": "women children family domestic violence community education support services not-for-profit",
        "eligibility": "Australian charities and not-for-profit organisations",
        "description": (
            "Perpetual's IMPACT Philanthropy program connects charitable organisations with "
            "philanthropic funding. Priority areas include women's safety, children's welfare, "
            "domestic violence support, and community education programs."
        ),
        "source_url": "https://www.perpetual.com.au/advice/philanthropic-services/impact-philanthropy/",
        "source": "seed",
    },
    {
        "id": 7,
        "title": "Foundation for Rural & Regional Renewal — Investing in Rural Community Futures",
        "funder": "Foundation for Rural & Regional Renewal (FRRR)",
        "amount_min": 5000,
        "amount_max": 50000,
        "deadline": "2026-09-15",
        "geography": "Rural and regional Australia — SA regional communities eligible",
        "focus_areas": "community rural regional women safety support services outreach",
        "eligibility": "Not-for-profit organisations serving rural and regional Australian communities",
        "description": (
            "FRRR supports community organisations in rural and regional Australia addressing "
            "local needs. Eligible projects include women's safety services, community support, "
            "and outreach programs in rural South Australia."
        ),
        "source_url": "https://frrr.org.au/funding/",
        "source": "seed",
    },
    {
        "id": 8,
        "title": "Channel 7 Telethon Trust — Community Grants",
        "funder": "Channel 7 Telethon Trust (SA)",
        "amount_min": 5000,
        "amount_max": 50000,
        "deadline": "2026-07-01",
        "geography": "South Australia",
        "focus_areas": "children women community welfare south australia safety support",
        "eligibility": "SA-based charitable organisations serving children, families, and communities",
        "description": (
            "Channel 7 Telethon Trust provides community grants to SA organisations supporting "
            "children, families, and vulnerable community members. Projects addressing women's "
            "safety and children's welfare are prioritised."
        ),
        "source_url": "https://www.7telethonsa.com.au/telethon-trust/community-grants/",
        "source": "seed",
    },
    {
        "id": 9,
        "title": "Sidney Myer Fund — Social Innovation Grants",
        "funder": "Sidney Myer Fund",
        "amount_min": 50000,
        "amount_max": 300000,
        "deadline": "2026-11-30",
        "geography": "National — Australian organisations",
        "focus_areas": "social innovation community women children welfare arts education",
        "eligibility": "Australian charitable organisations with innovative community programs",
        "description": (
            "The Sidney Myer Fund supports innovative social programs that strengthen communities. "
            "Eligible areas include women's safety, children's programs, and community services "
            "demonstrating evidence-based impact and innovation."
        ),
        "source_url": "https://www.myerfoundation.org.au/grants",
        "source": "seed",
    },
    {
        "id": 10,
        "title": "Commonwealth Safety and Justice Research Hub — Practice Grants",
        "funder": "Australia's National Research Organisation for Women's Safety (ANROWS)",
        "amount_min": 30000,
        "amount_max": 80000,
        "deadline": "2026-08-31",
        "geography": "National",
        "focus_areas": "domestic violence women safety research practice evidence DV family violence refuge",
        "eligibility": "Organisations working in domestic and family violence response sector",
        "description": (
            "ANROWS practice grants support frontline DV organisations to develop and evaluate "
            "evidence-based programs addressing domestic and family violence. Open to service "
            "providers, refuge operators, and community organisations in the DV sector."
        ),
        "source_url": "https://www.anrows.org.au/grants/",
        "source": "seed",
    },
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS grants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            funder TEXT,
            amount_min INTEGER,
            amount_max INTEGER,
            deadline TEXT,
            geography TEXT,
            focus_areas TEXT,
            eligibility TEXT,
            description TEXT,
            source_url TEXT,
            source TEXT DEFAULT 'seed',
            fit_score INTEGER DEFAULT 0,
            fit_band TEXT DEFAULT 'grey',
            score_breakdown TEXT,
            pipeline_stage TEXT DEFAULT 'discovered',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # migrate existing db if pipeline_stage column missing
    try:
        c.execute("ALTER TABLE grants ADD COLUMN pipeline_stage TEXT DEFAULT 'discovered'")
        conn.commit()
    except Exception:
        pass
    c.execute("""
        CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            grant_id INTEGER,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # seed if empty
    existing = c.execute("SELECT COUNT(*) FROM grants").fetchone()[0]
    if existing == 0:
        import json
        for g in SEED_GRANTS:
            scoring = score_grant(g)
            c.execute("""
                INSERT INTO grants
                (id, title, funder, amount_min, amount_max, deadline, geography,
                 focus_areas, eligibility, description, source_url, source,
                 fit_score, fit_band, score_breakdown)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                g["id"], g["title"], g["funder"],
                g["amount_min"], g["amount_max"], g["deadline"],
                g["geography"], g["focus_areas"], g["eligibility"],
                g["description"], g["source_url"], g["source"],
                scoring["total"], scoring["band"],
                json.dumps(scoring),
            ))
        conn.commit()
    conn.close()


def get_all_grants(include_archived=False):
    conn = get_db()
    if include_archived:
        rows = conn.execute(
            "SELECT * FROM grants ORDER BY fit_score DESC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM grants WHERE fit_band != 'grey' ORDER BY fit_score DESC"
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_grant(grant_id: int):
    conn = get_db()
    row = conn.execute("SELECT * FROM grants WHERE id=?", (grant_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def update_pipeline_stage(grant_id: int, stage: str):
    conn = get_db()
    conn.execute("UPDATE grants SET pipeline_stage=? WHERE id=?", (stage, grant_id))
    conn.commit()
    conn.close()


def get_grants_by_stage():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM grants WHERE fit_band != 'grey' ORDER BY fit_score DESC"
    ).fetchall()
    conn.close()
    stages = {"discovered": [], "shortlisted": [], "drafting": [], "submitted": [], "won": [], "lost": []}
    for r in rows:
        d = dict(r)
        stage = d.get("pipeline_stage") or "discovered"
        if stage in stages:
            stages[stage].append(d)
        else:
            stages["discovered"].append(d)
    return stages


def upsert_grant(g: dict):
    import json
    scoring = score_grant(g)
    conn = get_db()
    existing = conn.execute(
        "SELECT id FROM grants WHERE source_url=?", (g.get("source_url", ""),)
    ).fetchone()
    if existing:
        conn.close()
        return
    conn.execute("""
        INSERT INTO grants
        (title, funder, amount_min, amount_max, deadline, geography,
         focus_areas, eligibility, description, source_url, source,
         fit_score, fit_band, score_breakdown)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        g.get("title"), g.get("funder"),
        g.get("amount_min", 0), g.get("amount_max", 0),
        g.get("deadline", ""), g.get("geography", ""),
        g.get("focus_areas", ""), g.get("eligibility", ""),
        g.get("description", ""), g.get("source_url", ""),
        g.get("source", "scraped"),
        scoring["total"], scoring["band"],
        json.dumps(scoring),
    ))
    conn.commit()
    conn.close()
