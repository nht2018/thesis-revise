# Thesis Revision Skill

[English](README.md) | [中文](README.zh-CN.md)

`thesis-revision` is a Codex skill for review-ready revision of LaTeX theses and dissertations. It focuses on non-logical issues: examiner comments, thesis-wide grammar and consistency, bibliography quality, abstract polishing, LaTeX cross-references, build logs, and PDF presentation.

## Features

- Review examiner comments and produce a traceable minimal revision plan.
- Run thesis-wide grammar and academic prose checks while avoiding LaTeX, math, and citation noise.
- Check structure, terminology, notation, heading style, citations, and prose consistency across chapters assembled from multiple papers.
- Inspect BibTeX entries for duplicates, capitalization protection, official publication versions, venue formatting, URLs, editions, and malformed fields.
- Polish bilingual abstracts and check consistency between Chinese and English abstracts and keywords.
- Diagnose LaTeX/PDF issues such as undefined references, repeated auto-reference words, algorithm line-number references, TOC page numbers, and bibliography formatting.
- Default to a review-first workflow: report and plan before editing, unless the user explicitly asks for direct edits.

## Installation

Install or copy this repository as a Codex skill:

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/nht2018/thesis-revise.git ~/.codex/skills/thesis-revision
```

If a local copy already exists:

```bash
cd ~/.codex/skills/thesis-revision
git pull
```

## Usage

Example prompts:

```text
Use $thesis-revision to review this LaTeX thesis before submission.
Use $thesis-revision to handle these examiner comments and propose minimal edits.
Use $thesis-revision to run a full grammar and prose check on this thesis.
Use $thesis-revision to check bibliography duplicates and BibTeX capitalization.
Use $thesis-revision to polish the Chinese and English abstracts and check consistency.
```

## Helper Scripts

The skill includes heuristic scripts. They are helpers, not substitutes for manual review.

```bash
python3 scripts/scan_latex_thesis.py /path/to/thesis --pdf /path/to/thesis.pdf
python3 scripts/check_bibliography.py /path/to/references.bib
```

## Repository Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── bibliography-checklist.md
│   ├── consistency-checklist.md
│   ├── grammar-checklist.md
│   ├── latex-pdf-checklist.md
│   └── revision-workflow.md
└── scripts/
    ├── check_bibliography.py
    └── scan_latex_thesis.py
```

## Design Principles

- Be general: do not assume a specific thesis template, folder structure, discipline, or terminology set.
- Be conservative: preserve technical claims, theorems, algorithms, experiments, and conclusions.
- Be traceable: connect every expert comment to a location, action, and verification step.
- Be minimal: prefer local sentence-level edits and style normalization over broad rewrites.
- Be verifiable: compile the thesis and inspect logs/PDF output after edits.
