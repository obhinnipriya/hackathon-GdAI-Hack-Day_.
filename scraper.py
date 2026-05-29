import threading
import requests
from bs4 import BeautifulSoup
from database import upsert_grant

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

_scrape_status = {"running": False, "done": False, "found": 0, "error": None}


def get_status():
    return dict(_scrape_status)


def _scrape_grants_gov_au():
    """Fetch grants from GrantConnect (grants.gov.au) open search."""
    try:
        url = "https://www.grants.gov.au/Go/Public"
        params = {
            "Keywords": "domestic violence women safety community",
            "OrderBy": "CloseDate",
        }
        resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        count = 0
        for row in soup.select("table.search-results tr")[1:11]:
            cells = row.find_all("td")
            if len(cells) < 4:
                continue
            link_tag = cells[0].find("a")
            if not link_tag:
                continue
            title = link_tag.get_text(strip=True)
            href = link_tag.get("href", "")
            full_url = f"https://www.grants.gov.au{href}" if href.startswith("/") else href
            funder = cells[1].get_text(strip=True) if len(cells) > 1 else "Australian Government"
            deadline = cells[3].get_text(strip=True) if len(cells) > 3 else ""
            upsert_grant({
                "title": title,
                "funder": funder,
                "amount_min": 0,
                "amount_max": 0,
                "deadline": deadline,
                "geography": "National",
                "focus_areas": "domestic violence women safety community",
                "eligibility": "See grant details",
                "description": f"Live grant from GrantConnect. Title: {title}. Funder: {funder}.",
                "source_url": full_url,
                "source": "scraped",
            })
            count += 1
        return count
    except Exception as e:
        return 0


def _scrape_sa_gov():
    """Try to fetch SA Government community grants listing."""
    try:
        url = "https://www.sa.gov.au/topics/community-support/grants-and-funding"
        resp = requests.get(url, headers=HEADERS, timeout=12)
        soup = BeautifulSoup(resp.text, "html.parser")
        count = 0
        for link in soup.select("a")[:40]:
            text = link.get_text(strip=True)
            href = link.get("href", "")
            if any(kw in text.lower() for kw in ["grant", "fund", "community", "women", "safety"]):
                if len(text) > 10 and href.startswith("http"):
                    upsert_grant({
                        "title": text,
                        "funder": "SA Government",
                        "amount_min": 0,
                        "amount_max": 0,
                        "deadline": "",
                        "geography": "South Australia",
                        "focus_areas": "community south australia support",
                        "eligibility": "SA-based organisations",
                        "description": f"Grant opportunity from SA Government: {text}",
                        "source_url": href,
                        "source": "scraped",
                    })
                    count += 1
                    if count >= 3:
                        break
        return count
    except Exception:
        return 0


def run_scrape():
    global _scrape_status
    if _scrape_status["running"]:
        return
    _scrape_status = {"running": True, "done": False, "found": 0, "error": None}

    def _worker():
        total = 0
        total += _scrape_grants_gov_au()
        total += _scrape_sa_gov()
        _scrape_status["found"] = total
        _scrape_status["running"] = False
        _scrape_status["done"] = True

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
