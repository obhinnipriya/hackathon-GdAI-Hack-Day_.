import feedparser
from datetime import datetime

RSS_FEEDS = [
    "https://www.abc.net.au/news/feed/51120/rss.xml",
    "https://www.theguardian.com/australia-news/rss",
    "https://www.theguardian.com/society/rss",
]

SIGNAL_KEYWORDS = [
    "domestic violence", "family violence", "women's safety", "gender-based violence",
    "women shelter", "refuge", "DV", "FDV", "philanthropist", "corporate giving",
    "women's rights", "child safety", "community grant", "charity funding",
]

MOCK_DONOR_SIGNALS = [
    {
        "platform": "ANZ Community Hub",
        "source_url": "https://www.anz.com.au/about-us/esg/community/",
        "actor": "ANZ Foundation",
        "actor_type": "Corporate Foundation",
        "signal": (
            "ANZ Foundation has committed $2M to women's economic safety initiatives "
            "across Australia in 2026. Applications open Q3."
        ),
        "relevance": "Direct match — women's economic safety, Australia-wide",
        "time_ago": "2 hours ago",
        "action": "Approach ANZ Foundation grants team",
        "icon": "🏦",
    },
    {
        "platform": "Our Watch",
        "source_url": "https://www.ourwatch.org.au/",
        "actor": "Our Watch",
        "actor_type": "National DV Prevention Body",
        "signal": (
            "Our Watch released new research showing primary prevention programs "
            "reduce DV rates by 38% when paired with crisis refuge services. "
            "Calling for co-investment from philanthropic sector."
        ),
        "relevance": "Evidence base directly supports Mary's House refuge + outreach model",
        "time_ago": "5 hours ago",
        "action": "Use Our Watch data to strengthen grant applications",
        "icon": "👁️",
    },
    {
        "platform": "Lord Mayor's Charitable Foundation",
        "source_url": "https://www.lmcf.org.au/grants",
        "actor": "Lord Mayor's Charitable Foundation",
        "actor_type": "Community Foundation",
        "signal": (
            "LMCF opened a new grants round with a focus on women's safety and "
            "children's wellbeing across Victoria and South Australia. "
            "EOIs close in 6 weeks."
        ),
        "relevance": "SA eligibility confirmed — directly funds women's safety and children's programs",
        "time_ago": "1 day ago",
        "action": "Submit EOI before deadline — strong fit",
        "icon": "🏛️",
    },
    {
        "platform": "Minderoo Foundation",
        "source_url": "https://www.minderoo.org/walk-free/",
        "actor": "Minderoo Foundation",
        "actor_type": "Private Foundation",
        "signal": (
            "Minderoo's Walk Free initiative expanded scope to include domestic "
            "and family violence as a form of modern-day coercion. New funding round expected."
        ),
        "relevance": "DV scope expansion — watch for grant round opening",
        "time_ago": "2 days ago",
        "action": "Register for Minderoo grants newsletter",
        "icon": "🌿",
    },
    {
        "platform": "Gandel Foundation",
        "source_url": "https://www.gandelfoundation.org.au/",
        "actor": "Gandel Foundation",
        "actor_type": "Private Foundation",
        "signal": (
            "Gandel Foundation published its 2026 funding priorities, listing "
            "women's safety infrastructure and children's trauma recovery as "
            "key investment areas for the coming year."
        ),
        "relevance": "Strong alignment — women's safety + children's trauma matches Mary's House programs",
        "time_ago": "3 days ago",
        "action": "Prepare introductory letter for Gandel Foundation",
        "icon": "💛",
    },
]


def get_news_signals(limit=12):
    articles = []
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries:
                title = getattr(entry, "title", "")
                summary = getattr(entry, "summary", "")
                link = getattr(entry, "link", "")
                published = getattr(entry, "published", "")
                text = (title + " " + summary).lower()
                if any(kw.lower() in text for kw in SIGNAL_KEYWORDS):
                    articles.append({
                        "title": title,
                        "summary": summary[:200] + "..." if len(summary) > 200 else summary,
                        "url": link,
                        "published": published,
                        "source": feed.feed.get("title", feed_url),
                    })
        except Exception:
            continue

    seen = set()
    unique = []
    for a in articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    return unique[:limit]


def get_donor_signals():
    return MOCK_DONOR_SIGNALS
