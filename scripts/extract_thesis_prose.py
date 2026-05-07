#!/usr/bin/env python3
"""Extract rough prose chunks from a LaTeX thesis for grammar review."""

from __future__ import annotations

import argparse
import os
import re
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


def strip_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        chars = []
        escaped = False
        for ch in line:
            if ch == "%" and not escaped:
                break
            chars.append(ch)
            escaped = (ch == "\\" and not escaped)
            if ch != "\\":
                escaped = False
        lines.append("".join(chars))
    return "\n".join(lines)


def latex_to_prose(text: str) -> str:
    text = strip_comments(text)
    for env in ("equation", "align", "align*", "gather", "multline", "table", "figure", "algorithm", "tikzpicture"):
        text = re.sub(r"\\begin\{" + re.escape(env) + r"\}.*?\\end\{" + re.escape(env) + r"\}", "\n", text, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\\[[\s\S]*?\\\]", " ", text)
    text = re.sub(r"\\\([\s\S]*?\\\)", " ", text)
    text = re.sub(r"\\(?:cite|citep|citet|ref|eqref|cref|Cref|label|url|href)(?:\[[^\]]*\])?\{[^{}]*\}", " ", text)
    text = re.sub(r"\\(?:chapter|section|subsection|subsubsection|paragraph)\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r"\n\1.\n", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}_^~&]", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def chunks(text: str, min_words: int) -> list[str]:
    paras = []
    for para in re.split(r"\n\s*\n", text):
        para = " ".join(para.split())
        if len(para.split()) >= min_words:
            paras.append(para)
    return paras


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract rough thesis prose for grammar review.")
    parser.add_argument("root", nargs="?", default=".", help="Thesis project root")
    parser.add_argument("--all", action="store_true", help="Include archived or unused TeX files")
    parser.add_argument("--min-words", type=int, default=18, help="Minimum words per emitted paragraph")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    tex_files = iter_tex(root)
    main_candidates = [p for p in tex_files if "\\documentclass" in read_text(p) and "\\begin{document}" in read_text(p)]
    scan_files = tex_files
    if not args.all and len(main_candidates) == 1:
        scan_files = sorted(referenced_tex_files(main_candidates[0], set(tex_files)))

    print("# Extracted Thesis Prose")
    print()
    print(f"- Root: `{root}`")
    print(f"- Files scanned: {len(scan_files)}")
    print()
    for path in scan_files:
        prose = latex_to_prose(read_text(path))
        paras = chunks(prose, args.min_words)
        if not paras:
            continue
        rel = path.relative_to(root) if path.is_relative_to(root) else path
        print(f"## {rel}")
        print()
        for para in paras:
            print(f"- {para}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
