#!/usr/bin/env python3
"""Heuristic scanner for LaTeX thesis revision issues.

This script is intentionally conservative. It flags candidates that an agent
should confirm against source or PDF before editing.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


SKIP_DIRS = {".git", ".svn", ".hg", "__pycache__", "node_modules", ".venv"}
TEX_EXTS = {".tex", ".ltx"}


def iter_files(root: Path, suffixes: set[str]) -> list[Path]:
    out: list[Path] = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = Path(current) / name
            if path.suffix.lower() in suffixes:
                out.append(path)
    return sorted(out)


def read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def referenced_tex_files(root: Path, main: Path, all_tex: set[Path]) -> set[Path]:
    seen: set[Path] = set()
    stack = [main]
    include_pattern = re.compile(r"\\(?:include|input)\{([^{}]+)\}")
    while stack:
        path = stack.pop()
        if path in seen or path.suffix.lower() not in TEX_EXTS:
            continue
        seen.add(path)
        text = read_text(path)
        for match in include_pattern.finditer(text):
            raw = match.group(1).strip()
            if not raw or raw.startswith("|"):
                continue
            candidate = (path.parent / raw).resolve()
            candidates = [candidate]
            if candidate.suffix == "":
                candidates.append(candidate.with_suffix(".tex"))
            for item in candidates:
                if item in all_tex and item not in seen:
                    stack.append(item)
    return seen


def add_hits(findings: list[tuple[str, str, int, str]], root: Path, path: Path, text: str, patterns: list[tuple[str, str]]):
    for label, pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.MULTILINE):
            snippet = " ".join(match.group(0).split())
            findings.append((label, rel(path, root), line_no(text, match.start()), snippet[:160]))


def title_style_warnings(root: Path, tex_files: list[Path]) -> list[str]:
    sections: list[tuple[str, str, int]] = []
    for path in tex_files:
        text = read_text(path)
        for match in re.finditer(r"\\(?:chapter|section|subsection)\*?\{([^{}]+)\}", text):
            sections.append((match.group(1), rel(path, root), line_no(text, match.start())))

    warnings: list[str] = []
    numerical = [s for s in sections if re.search(r"Numerical (Results|Experiments|Experiment|Simulation|Simulations)", s[0], re.I)]
    if len({s[0].lower() for s in numerical}) > 1:
        values = "; ".join(f"{title} ({path}:{line})" for title, path, line in numerical)
        warnings.append(f"Mixed numerical-section names: {values}")

    notation = [s for s in sections if s[0].lower() in {"notation", "notations"}]
    if len({s[0].lower() for s in notation}) > 1:
        values = "; ".join(f"{title} ({path}:{line})" for title, path, line in notation)
        warnings.append(f"Mixed Notation/Notations headings: {values}")

    endings = [s for s in sections if s[0].lower() in {"summary", "conclusion", "conclusion and future work"}]
    if len({s[0].lower() for s in endings}) > 2:
        values = "; ".join(f"{title} ({path}:{line})" for title, path, line in endings)
        warnings.append(f"Many different chapter-ending headings: {values}")

    return warnings


def pdf_text(root: Path, pdf: Path | None) -> str:
    if pdf is None:
        candidate = root / "thesis.pdf"
        pdf = candidate if candidate.exists() else None
    if pdf is None or not pdf.exists() or shutil.which("pdftotext") is None:
        return ""
    try:
        result = subprocess.run(
            ["pdftotext", str(pdf), "-"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=60,
        )
    except Exception:
        return ""
    return result.stdout if result.returncode == 0 else ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a LaTeX thesis for revision candidates.")
    parser.add_argument("root", nargs="?", default=".", help="Thesis project root")
    parser.add_argument("--pdf", help="Optional generated PDF path")
    parser.add_argument("--all", action="store_true", help="Scan every TeX file under root, including archived or unused files")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    pdf_path = Path(args.pdf).expanduser().resolve() if args.pdf else None

    tex_files = iter_files(root, TEX_EXTS)
    bib_files = iter_files(root, {".bib"})
    build_files = [p for p in (root / "compile.sh", root / "Makefile", root / "latexmkrc") if p.exists()]

    main_candidates = []
    for path in tex_files:
        text = read_text(path)
        if "\\documentclass" in text and "\\begin{document}" in text:
            main_candidates.append(path)

    scan_files = tex_files
    if not args.all and len(main_candidates) == 1:
        scan_files = sorted(referenced_tex_files(root, main_candidates[0], set(tex_files)))

    patterns = [
        ("Possible repeated auto-reference word", r"\b(Theorem|Lemma|Proposition|Corollary|Algorithm|Figure|Table|Equation)\s+\1\b"),
        ("Possible algorithm line reference", r"\bLine~?\\(?:ref|cref|Cref)\{[^{}]+\}|\bLine\s+1\b"),
        ("Possible hard-coded theorem/algorithm reference", r"\b(Theorem|Lemma|Proposition|Corollary|Algorithm|Figure|Table)\s+[0-9]+(?:\.[0-9]+)?\b"),
        ("Missing space before citation", r"\bin\\cite\{[^{}]+\}"),
        ("Theorem note should probably use optional argument", r"\\begin\{(?:theorem|lemma|proposition|corollary|definition|remark|assumption)\}\([^)]{3,}\)"),
        ("Doubled punctuation candidate", r"\.;"),
        ("Equation range wording candidate", r"Equation\s+\([^)]*\)\s*[-\u2013]\s*Equation\s+\([^)]*\)"),
        ("This paper in thesis body", r"\b[Tt]his paper\b"),
    ]

    findings: list[tuple[str, str, int, str]] = []
    for path in scan_files:
        add_hits(findings, root, path, read_text(path), patterns)

    pdf_findings: list[str] = []
    text = pdf_text(root, pdf_path)
    if text:
        pdf_patterns = [
            ("Line 1", r"\bLine 1\b"),
            ("Repeated Lemma", r"\bLemma Lemma\b"),
            ("Repeated Corollary", r"\bCorollary Corollary\b"),
            ("Equation-to-Equation range", r"Equation\s+\([^)]*\)\s*[-\u2013]\s*Equation\s+\([^)]*\)"),
            ("Citation spacing artifact", r"\bin\[[0-9, ]+\]"),
        ]
        for label, pattern in pdf_patterns:
            matches = list(re.finditer(pattern, text))
            if matches:
                pdf_findings.append(f"{label}: {len(matches)} occurrence(s)")

    print("# LaTeX Thesis Scan")
    print()
    print(f"- Root: `{root}`")
    print(f"- TeX files: {len(tex_files)} total, {len(scan_files)} scanned")
    print(f"- Bib files: {', '.join(rel(p, root) for p in bib_files) or 'none found'}")
    print(f"- Main TeX candidates: {', '.join(rel(p, root) for p in main_candidates) or 'none found'}")
    print(f"- Build files: {', '.join(rel(p, root) for p in build_files) or 'none found'}")
    print()

    print("## Source Findings")
    if not findings:
        print("- No heuristic source findings.")
    else:
        for label, path, line, snippet in findings:
            print(f"- `{path}:{line}` {label}: {snippet}")
    print()

    print("## Heading Consistency")
    heading_warnings = title_style_warnings(root, scan_files)
    if not heading_warnings:
        print("- No headline-level heading consistency warning.")
    else:
        for warning in heading_warnings:
            print(f"- {warning}")
    print()

    print("## PDF Text Findings")
    if not text:
        print("- PDF text not checked; provide --pdf or keep thesis.pdf in the root with pdftotext installed.")
    elif not pdf_findings:
        print("- No heuristic PDF text findings.")
    else:
        for finding in pdf_findings:
            print(f"- {finding}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
