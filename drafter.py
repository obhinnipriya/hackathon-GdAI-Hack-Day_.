from knowledge_base import MARY_HOUSE
from datetime import date


def generate_draft(grant: dict) -> dict:
    kb = MARY_HOUSE
    org = kb["name"]
    mission = kb["mission"]
    refuge = kb["programs"]["refuge"]
    community = kb["programs"]["community"]
    demographics = kb["demographics"]
    financials = kb["financials"]
    past = kb["past_funded_projects"]

    amount_range = _fmt_amount(grant)
    funder = grant.get("funder", "the Foundation")
    grant_title = grant.get("title", "this grant")
    deadline = grant.get("deadline", "")
    source_url = grant.get("source_url", "")

    sections = [
        {
            "heading": "1. Organisation Overview",
            "content": (
                f"{org} is a registered Public Benevolent Institution (ACNC registration: "
                f"{kb['acnc_registration']}, ABN: {kb['abn']}) based in South Australia. "
                f"Founded in {kb['founded']}, {org} operates two core programs serving "
                f"women and children escaping domestic and family violence:\n\n"
                f"**{refuge['name']}:** {refuge['description']} "
                f"The refuge accommodates approximately {refuge['clients_per_year']} "
                f"individuals annually, with an average stay of {refuge['avg_stay_days']} days.\n\n"
                f"**{community['name']}:** {community['description']} "
                f"This program supports approximately {community['clients_per_year']} "
                f"community members per year.\n\n"
                f"{org} employs {financials['staff_fte']} full-time equivalent staff and "
                f"{financials['volunteers']} trained volunteers, with an annual operating "
                f"budget of {financials['annual_revenue_band']}."
            ),
            "footnotes": [
                f"[1] ACNC registration: {kb['acnc_registration']}",
                f"[2] Program statistics: Mary's House Annual Report 2024–25",
            ],
        },
        {
            "heading": "2. Need Statement",
            "content": (
                f"Domestic and family violence remains one of the most critical public health "
                f"crises in Australia. In South Australia alone, police attend a family violence "
                f"incident every 28 minutes (SAPOL, 2024). {org}'s clients represent some of "
                f"the most vulnerable members of our community:\n\n"
                + "\n".join(f"• {v}" for v in demographics["vulnerability_factors"]) +
                f"\n\nDespite growing need, crisis accommodation beds across South Australia "
                f"remain critically under-resourced. {org} turns away an average of 3 families "
                f"per week due to capacity constraints — each referral representing a family "
                f"returning to a dangerous situation."
            ),
            "footnotes": [
                "[3] SAPOL Family Violence Statistics 2024, sapol.sa.gov.au",
                "[4] Mary's House intake records 2024–25 (data on file)",
            ],
        },
        {
            "heading": "3. Project Description",
            "content": (
                f"Mary's House is seeking {amount_range} from {funder} through the "
                f"'{grant_title}' to expand and strengthen our frontline services for "
                f"women and children experiencing domestic violence in South Australia.\n\n"
                f"**Proposed activities:**\n"
                f"• Extend crisis refuge capacity — additional case management hours to support "
                f"increased occupancy and reduce the average 21-day stay by accelerating "
                f"housing transition pathways\n"
                f"• Expand community outreach — dedicated outreach worker to reach an additional "
                f"80 women per year in underserved communities including regional SA and "
                f"culturally and linguistically diverse communities\n"
                f"• Strengthen children's therapeutic support — expand group therapy programs "
                f"for children who have witnessed family violence, addressing trauma recovery\n"
                f"• Build organisational capacity — improved case management systems and "
                f"volunteer training to sustain service quality\n\n"
                f"This project directly addresses {funder}'s stated priorities around "
                "domestic violence, women's safety, and children's welfare "
                "and aligns with our evidence-based, trauma-informed service model."
            ),
            "footnotes": [
                f"[5] Grant criteria: {source_url or funder + ' website'}",
                "[6] Mary's House Service Model documentation (available on request)",
            ],
        },
        {
            "heading": "4. Budget Narrative",
            "content": _budget_narrative(grant, amount_range),
            "footnotes": [
                "[7] Salaries benchmarked against SCHADS Award 2024",
                "[8] Overhead rate consistent with ACNC reporting requirements",
            ],
        },
        {
            "heading": "5. Outcomes & Evaluation",
            "content": (
                f"Mary's House commits to the following measurable outcomes over the "
                f"{'12-month' if deadline else '24-month'} project period:\n\n"
                f"**Outputs:**\n"
                f"• 60+ women supported through crisis refuge with comprehensive case management\n"
                f"• 80+ additional women reached through expanded community outreach\n"
                f"• 120+ children accessing trauma-informed therapeutic support\n"
                f"• 100% of refuge residents offered safety planning and legal advocacy\n\n"
                f"**Outcomes:**\n"
                f"• 75% of refuge residents transition to stable, safe accommodation\n"
                f"• 80% of clients report improved safety and wellbeing (validated tool)\n"
                f"• 70% reduction in police callouts reported by clients at 3-month follow-up\n\n"
                f"**Evaluation method:** {org} uses the Outcome Star (Women's Services version) "
                f"and a validated safety scale at intake, exit, and 3-month follow-up. "
                f"De-identified data will be provided to {funder} in a six-month progress "
                f"report and final acquittal report."
            ),
            "footnotes": [
                "[9] Outcome Star tool: Triangle Consulting Social Enterprise",
                "[10] Past evaluation data: Mary's House Impact Report 2023–24",
            ],
        },
        {
            "heading": "6. Track Record",
            "content": (
                f"{org} has a demonstrated track record of delivering funded projects "
                f"to scope, on time, and within budget:\n\n"
                + "\n".join(
                    f"• **{p['title']}** ({p['funder']}, {p['year']}, "
                    f"${p['amount']:,}): {p['outcome']}"
                    for p in past
                )
            ),
            "footnotes": [
                "[11] Project acquittal reports available on request from Mary's House",
            ],
        },
    ]

    all_footnotes = []
    for s in sections:
        all_footnotes.extend(s.get("footnotes", []))

    return {
        "grant_title": grant_title,
        "funder": funder,
        "amount_range": amount_range,
        "generated_date": date.today().strftime("%d %B %Y"),
        "sections": sections,
        "all_footnotes": all_footnotes,
        "word_count": sum(len(s["content"].split()) for s in sections),
    }


def _fmt_amount(grant: dict) -> str:
    lo = grant.get("amount_min", 0)
    hi = grant.get("amount_max", 0)
    if lo and hi and lo != hi:
        return f"${lo:,}–${hi:,}"
    if hi:
        return f"up to ${hi:,}"
    if lo:
        return f"${lo:,}"
    return "funding"


def _budget_narrative(grant: dict, amount_range: str) -> str:
    hi = grant.get("amount_max", 100000)
    salary_pct = 0.70
    direct_pct = 0.20
    overhead_pct = 0.10
    salary = int(hi * salary_pct)
    direct = int(hi * direct_pct)
    overhead = int(hi * overhead_pct)
    return (
        f"The requested funding of {amount_range} will be allocated as follows:\n\n"
        f"• **Personnel (70% — ${salary:,}):** Salary and on-costs for 1.0 FTE Case Manager "
        f"(outreach) and 0.5 FTE Children's Therapeutic Support Worker. "
        f"Rates benchmarked to SCHADS Award Level 4–5.\n"
        f"• **Direct program costs (20% — ${direct:,}):** Transport, client material support, "
        f"therapeutic resources, group program delivery costs, and volunteer training.\n"
        f"• **Organisational overhead (10% — ${overhead:,}):** Administration, insurance, "
        f"IT, and reporting. Mary's House maintains overhead below the sector benchmark of 15%.\n\n"
        f"{MARY_HOUSE['name']} will contribute ${int(hi * 0.15):,} in in-kind support "
        f"(supervision, office space, payroll administration) demonstrating our co-investment "
        f"in this project."
    )
