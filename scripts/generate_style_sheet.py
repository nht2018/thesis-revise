#!/usr/bin/env python3
"""Generate a draft thesis style sheet from LaTeX sources."""

from __future__ import annotations

import argparse
import os
import re
from collections import Counter
from pathlib import Path


SKIP_DIRS = {".git", ".svn", ".hg", "__pycache__", "node_modules", ".venv"}
TEX_EXTS = {".tex", ".ltx"}


def read_text(path: Path) -> str:
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    return path.read_text(errors="replace")


def iter_tex(root: Path) -> list[Path]:
    out: list[Path] = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            path = Path(current) / name
            if path.suffix.lower() in TEX_EXTS:
                out.append(path)
    return sorted(out)


def referenced_tex_files(main: Path, all_tex: set[Path]) -> set[Path]:
    seen: set[Path] = set()
    stack = [main]
    include_pattern = re.compile(r"\\(?:include|input)\{([^{}]+)\}")
    while stack:
        path = stack.pop()
        if path in seen:
            continue
        seen.add(path)
        text = read_text(path)
        for match in include_pattern.finditer(text):
            raw = match.group(1).strip()
            candidate = (path.parent / raw).resolve()
            candidates = [candidate]
            if candidate.suffix == "":
                candidates.append(candidate.with_suffix(".tex"))
            for item in candidates:
                if item in all_tex and item not in seen:
                    stack.append(item)
    return seen


def clean_latex(text: str) -> str:
    text = re.sub(r"%.*", " ", text)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r" \1 ", text)
    text = re.sub(r"\\[A-Za-z]+\*?", " ", text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a draft style sheet from a LaTeX thesis.")
    parser.add_argument("root", nargs="?", default=".", help="Thesis project root")
    parser.add_argument("--all", action="store_true", help="Include archived or unused TeX files")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    tex_files = iter_tex(root)
    main_candidates = [p for p in tex_files if "\\documentclass" in read_text(p) and "\\begin{document}" in read_text(p)]
    scan_files = tex_files
    if not args.all and len(main_candidates) == 1:
        scan_files = sorted(referenced_tex_files(main_candidates[0], set(tex_files)))

    heading_counter: Counter[str] = Counter()
    ref_counter: Counter[str] = Counter()
    cite_counter: Counter[str] = Counter()
    acronym_counter: Counter[str] = Counter()
    command_counter: Counter[str] = Counter()

    for path in scan_files:
        text = read_text(path)
        for match in re.finditer(r"\\(?:chapter|section|subsection|subsubsection)\*?(?:\[[^\]]*\])?\{([^{}]+)\}", text):
            heading_counter[match.group(1).strip()] += 1
        for match in re.finditer(r"\\(cref|Cref|ref|eqref|autoref)\b", text):
            ref_counter[match.group(1)] += 1
        for match in re.finditer(r"\\(cite|citep|citet)\b", text):
            cite_counter[match.group(1)] += 1
        for match in re.finditer(r"\\(?:newcommand|DeclareMathOperator)\*?\{\\([A-Za-z]+)\}", text):
            command_counter[match.group(1)] += 1
        clean = clean_latex(text)
        for word in re.findall(r"\b[A-Z][A-Z0-9]{1,}\b", clean):
            acronym_counter[word] += 1

    print("# Thesis Style Sheet Draft")
    print()
    print("## Scope")
    print()
    print(f"- Root: `{root}`")
    print(f"- Main file candidates: {', '.join(str(p.relative_to(root)) for p in main_candidates) or 'none found'}")
    print(f"- Files scanned: {len(scan_files)}")
    print()
    print("## Heading Conventions")
    print()
    print("| Observed heading | Count |")
    print("| --- | --- |")
    for heading, count in heading_counter.most_common(40):
        safe_heading = heading.replace("|", "\\|")
        print(f"| {safe_heading} | {count} |")
    print()
    print("## Cross-Reference and Citation Commands")
    print()
    print(f"- Reference commands: {dict(ref_counter)}")
    print(f"- Citation commands: {dict(cite_counter)}")
    print()
    print("## Acronym Candidates")
    print()
    print("| Candidate | Count | Preferred form / note |")
    print("| --- | --- | --- |")
    for word, count in acronym_counter.most_common(40):
        print(f"| {word} | {count} | 待确认 |")
    print()
    print("## Macro / Notation Candidates")
    print()
    print("| Macro | Count | Meaning / note |")
    print("| --- | --- | --- |")
    for command, count in command_counter.most_common(60):
        print(f"| `\\{command}` | {count} | 待确认 |")
    print()
    print("## Decisions To Fill")
    print()
    print("- Preferred heading capitalization:")
    print("- Preferred numerical-experiment section name:")
    print("- Preferred notation section name:")
    print("- Preferred cross-reference command:")
    print("- Preferred bibliography policy:")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
