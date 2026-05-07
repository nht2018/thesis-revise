#!/usr/bin/env python3
"""Heuristic BibTeX checker for thesis revision.

The parser is deliberately lightweight and flags candidates for manual review.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path


STOPWORDS = {"and", "of", "the", "in", "on", "for", "to", "with", "a", "an", "by", "from"}


def read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def extract_entries(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    pos = 0
    while True:
        match = re.search(r"@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,", text[pos:])
        if not match:
            break
        start = pos + match.start()
        body_start = pos + match.end()
        depth = 1
        i = body_start
        while i < len(text) and depth:
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
            i += 1
        body = text[body_start : i - 1]
        entries.append({
            "type": match.group(1).lower(),
            "key": match.group(2).strip(),
            "body": body,
            "line": str(text.count("\n", 0, start) + 1),
        })
        pos = i
    return entries


def split_fields(body: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    i = 0
    n = len(body)
    while i < n:
        while i < n and body[i] in " \t\r\n,":
            i += 1
        name_start = i
        while i < n and re.match(r"[A-Za-z0-9_\-]", body[i]):
            i += 1
        if i == name_start:
            i += 1
            continue
        name = body[name_start:i].lower()
        while i < n and body[i].isspace():
            i += 1
        if i >= n or body[i] != "=":
            continue
        i += 1
        while i < n and body[i].isspace():
            i += 1
        if i >= n:
            break
        if body[i] == "{":
            depth = 1
            i += 1
            value_start = i
            while i < n and depth:
                if body[i] == "{":
                    depth += 1
                elif body[i] == "}":
                    depth -= 1
                i += 1
            value = body[value_start : i - 1]
        elif body[i] == '"':
            i += 1
            value_start = i
            escaped = False
            while i < n:
                ch = body[i]
                if ch == '"' and not escaped:
                    break
                escaped = (ch == "\\" and not escaped)
                if ch != "\\":
                    escaped = False
                i += 1
            value = body[value_start:i]
            i += 1
        else:
            value_start = i
            while i < n and body[i] != ",":
                i += 1
            value = body[value_start:i].strip()
        fields[name] = " ".join(value.split())
    return fields


def normalize_title(title: str) -> str:
    title = re.sub(r"[{}\\]", "", title).lower()
    return re.sub(r"[^a-z0-9]+", " ", title).strip()


def is_braced_at(text: str, start: int, end: int) -> bool:
    before = text[:start]
    after = text[end:]
    return before.endswith("{") and after.startswith("}")


def unprotected_caps(title: str) -> list[str]:
    words: list[str] = []
    for match in re.finditer(r"\b[A-Z][A-Z0-9]{1,}\b", title):
        if not is_braced_at(title, match.start(), match.end()):
            words.append(match.group(0))
    return sorted(set(words))


def suspicious_venue_case(value: str) -> bool:
    clean = re.sub(r"[{}]", "", value)
    words = re.findall(r"[A-Za-z][A-Za-z\-]*", clean)
    content = [w for w in words if w.lower() not in STOPWORDS]
    if len(content) < 2:
        return False
    lower_initial = [w for w in content if w[0].islower()]
    return len(lower_initial) >= max(1, len(content) // 2)


def is_preprint(fields: dict[str, str]) -> bool:
    venue = " ".join(fields.get(k, "") for k in ("journal", "booktitle", "archiveprefix", "eprinttype", "note")).lower()
    return "arxiv" in venue or "preprint" in venue or "eprint" in fields


def has_formal_venue(fields: dict[str, str]) -> bool:
    venue = " ".join(fields.get(k, "") for k in ("journal", "booktitle", "publisher")).lower()
    return bool(venue.strip()) and "arxiv" not in venue and "preprint" not in venue


def main() -> int:
    parser = argparse.ArgumentParser(description="Check BibTeX files for thesis revision candidates.")
    parser.add_argument("bib", nargs="+", help="BibTeX file(s)")
    args = parser.parse_args()

    records: list[tuple[Path, dict[str, str], dict[str, str]]] = []
    for bib in args.bib:
        path = Path(bib).expanduser().resolve()
        text = read_text(path)
        for entry in extract_entries(text):
            records.append((path, entry, split_fields(entry["body"])))

    by_title: dict[str, list[tuple[Path, dict[str, str], dict[str, str]]]] = defaultdict(list)
    by_doi: dict[str, list[tuple[Path, dict[str, str], dict[str, str]]]] = defaultdict(list)
    by_eprint: dict[str, list[tuple[Path, dict[str, str], dict[str, str]]]] = defaultdict(list)
    findings: list[str] = []

    for path, entry, fields in records:
        title = fields.get("title", "")
        if title:
            by_title[normalize_title(title)].append((path, entry, fields))
            caps = unprotected_caps(title)
            if caps:
                findings.append(f"`{path.name}:{entry['line']}` title may need capitalization braces for: {', '.join(caps)} (key `{entry['key']}`)")
        doi = fields.get("doi", "").lower().strip()
        if doi:
            by_doi[doi].append((path, entry, fields))
        eprint = fields.get("eprint", "").lower().strip()
        if eprint:
            by_eprint[eprint].append((path, entry, fields))

        for field in ("journal", "booktitle"):
            if field in fields and suspicious_venue_case(fields[field]):
                findings.append(f"`{path.name}:{entry['line']}` suspicious {field} capitalization: {fields[field]} (key `{entry['key']}`)")

        url = fields.get("url", "")
        if re.search(r"https?://\S*\s+\S*", url):
            findings.append(f"`{path.name}:{entry['line']}` URL contains whitespace (key `{entry['key']}`)")

        edition = fields.get("edition", "")
        if re.search(r"\b[0-9]+\s+edition\b", edition, re.I):
            findings.append(f"`{path.name}:{entry['line']}` edition style may be nonstandard: {edition} (key `{entry['key']}`)")

    duplicate_groups = []
    for label, groups in (("DOI", by_doi), ("eprint", by_eprint), ("title", by_title)):
        for value, group in groups.items():
            if value and len(group) > 1:
                keys = ", ".join(f"`{entry['key']}`" for _, entry, _ in group)
                duplicate_groups.append(f"{label} duplicate candidate `{value}`: {keys}")

    version_groups = []
    for title, group in by_title.items():
        if len(group) > 1 and any(is_preprint(fields) for _, _, fields in group) and any(has_formal_venue(fields) for _, _, fields in group):
            keys = ", ".join(f"`{entry['key']}`" for _, entry, _ in group)
            version_groups.append(f"Formal-version preference candidate `{title}`: {keys}")

    print("# Bibliography Check")
    print()
    print(f"- Entries parsed: {len(records)}")
    print()
    print("## Duplicate Candidates")
    if duplicate_groups:
        for item in duplicate_groups:
            print(f"- {item}")
    else:
        print("- No exact duplicate candidates by DOI/eprint/normalized title.")
    print()
    print("## Preprint vs Formal Version Candidates")
    if version_groups:
        for item in version_groups:
            print(f"- {item}")
    else:
        print("- No exact title match between preprint and formal-version candidates.")
    print()
    print("## Field and Capitalization Findings")
    if findings:
        for item in findings:
            print(f"- {item}")
    else:
        print("- No heuristic field/capitalization findings.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
