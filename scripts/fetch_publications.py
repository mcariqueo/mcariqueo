"""Fetch public publication metadata for the portfolio.

Sources:
- ORCID public API, using the ORCID iD listed in the institutional profile.
- Crossref public API as a fallback search by author name.

The script writes:
- source-materials/publications/publications.md
- source-materials/publications/publications.json
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


ORCID_ID = "0009-0005-1423-6932"
AUTHOR_NAME = "Marcial Cariqueo"
OUTPUT_DIR = Path("source-materials/publications")
USER_AGENT = "mcariqueo-portfolio-publication-fetcher/1.0 (mailto:marcial.cariqueo@gmail.com)"


@dataclass(frozen=True)
class Publication:
    title: str
    year: str
    journal: str = ""
    doi: str = ""
    url: str = ""
    source: str = ""


def get_json(url: str) -> dict[str, Any]:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = " ".join(str(item) for item in value if item)
    text = str(value)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def nested_text(value: dict[str, Any], *keys: str) -> str:
    current: Any = value
    for key in keys:
        if not isinstance(current, dict):
            return ""
        current = current.get(key)
    return clean_text(current)


def normalize_doi(doi: str) -> str:
    doi = clean_text(doi)
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    return doi


def publication_key(pub: Publication) -> str:
    title = re.sub(r"[^a-z0-9]+", " ", pub.title.lower()).strip()
    doi = normalize_doi(pub.doi).lower()
    return doi or title


def extract_orcid_year(work_summary: dict[str, Any]) -> str:
    pub_date = work_summary.get("publication-date") or {}
    for key in ("year", "month", "day"):
        value = pub_date.get(key, {}).get("value")
        if key == "year" and value:
            return clean_text(value)
    return ""


def extract_orcid_external_ids(work_summary: dict[str, Any]) -> tuple[str, str]:
    doi = ""
    url = ""
    external_ids = work_summary.get("external-ids", {}).get("external-id", []) or []
    for external_id in external_ids:
        id_type = clean_text(external_id.get("external-id-type")).lower()
        id_value = clean_text(external_id.get("external-id-value"))
        id_url = clean_text((external_id.get("external-id-url") or {}).get("value"))
        if id_type == "doi" and id_value:
            doi = normalize_doi(id_value)
            url = id_url or f"https://doi.org/{doi}"
        elif not url and id_url:
            url = id_url
    return doi, url


def fetch_orcid_publications() -> list[Publication]:
    url = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
    data = get_json(url)
    publications: list[Publication] = []

    for group in data.get("group", []) or []:
        summaries = group.get("work-summary", []) or []
        if not summaries:
            continue
        summary = summaries[0]
        title = nested_text(summary, "title", "title", "value")
        if not title:
            continue
        doi, external_url = extract_orcid_external_ids(summary)
        publications.append(
            Publication(
                title=title,
                year=extract_orcid_year(summary),
                journal=nested_text(summary, "journal-title", "value"),
                doi=doi,
                url=external_url or nested_text(summary, "url", "value"),
                source="ORCID",
            )
        )

    return publications


def crossref_year(item: dict[str, Any]) -> str:
    for key in ("published-print", "published-online", "published", "created"):
        date_parts = item.get(key, {}).get("date-parts", [])
        if date_parts and date_parts[0]:
            return clean_text(date_parts[0][0])
    return ""


def author_matches(item: dict[str, Any]) -> bool:
    authors = item.get("author", []) or []
    for author in authors:
        given = clean_text(author.get("given")).lower()
        family = clean_text(author.get("family")).lower()
        if "marcial" in given and "cariqueo" in family:
            return True
    return False


def fetch_crossref_publications(limit: int = 20) -> list[Publication]:
    query = quote(AUTHOR_NAME)
    url = f"https://api.crossref.org/works?query.author={query}&rows={limit}&select=title,container-title,DOI,URL,author,published-print,published-online,published,created"
    data = get_json(url)
    items = data.get("message", {}).get("items", []) or []
    publications: list[Publication] = []

    for item in items:
        if not author_matches(item):
            continue
        title = clean_text(item.get("title", [""])[0])
        if not title:
            continue
        doi = normalize_doi(item.get("DOI", ""))
        publications.append(
            Publication(
                title=title,
                year=crossref_year(item),
                journal=clean_text(item.get("container-title", [""])[0]),
                doi=doi,
                url=clean_text(item.get("URL")) or (f"https://doi.org/{doi}" if doi else ""),
                source="Crossref",
            )
        )

    return publications


def merge_publications(*groups: list[Publication]) -> list[Publication]:
    merged: dict[str, Publication] = {}
    for group in groups:
        for pub in group:
            key = publication_key(pub)
            if not key:
                continue
            existing = merged.get(key)
            if existing is None:
                merged[key] = pub
                continue
            merged[key] = Publication(
                title=existing.title or pub.title,
                year=existing.year or pub.year,
                journal=existing.journal or pub.journal,
                doi=existing.doi or pub.doi,
                url=existing.url or pub.url,
                source=", ".join(sorted(set((existing.source + ", " + pub.source).split(", ")))),
            )
    return sorted(merged.values(), key=lambda pub: (pub.year or "0000", pub.title), reverse=True)


def publication_to_markdown(pub: Publication) -> str:
    title = f"[{pub.title}]({pub.url})" if pub.url else pub.title
    details = [item for item in (pub.journal, pub.year, f"DOI: {pub.doi}" if pub.doi else "") if item]
    suffix = f" {' | '.join(details)}" if details else ""
    return f"- {title}. {suffix}".rstrip()


def write_outputs(publications: list[Publication]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "publications.json").write_text(
        json.dumps([asdict(pub) for pub in publications], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    markdown = [
        "# Publications",
        "",
        f"Generated from ORCID `{ORCID_ID}` and Crossref author search for `{AUTHOR_NAME}`.",
        "",
    ]
    markdown.extend(publication_to_markdown(pub) for pub in publications)
    markdown.append("")
    (OUTPUT_DIR / "publications.md").write_text("\n".join(markdown), encoding="utf-8")


def main() -> int:
    try:
        orcid_publications = fetch_orcid_publications()
    except Exception as exc:
        print(f"ORCID fetch failed: {exc}", file=sys.stderr)
        orcid_publications = []

    try:
        crossref_publications = fetch_crossref_publications()
    except Exception as exc:
        print(f"Crossref fetch failed: {exc}", file=sys.stderr)
        crossref_publications = []

    publications = merge_publications(orcid_publications, crossref_publications)
    write_outputs(publications)
    print(f"Wrote {len(publications)} publications to {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
