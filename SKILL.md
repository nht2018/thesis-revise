---
name: thesis-revision
description: Review and minimally revise LaTeX theses or dissertations for non-technical-logical issues before submission, defense, or expert re-review. Use when the user asks to handle examiner comments, run thesis-wide grammar/prose checks, polish abstracts, check bilingual consistency, normalize terminology/notation/style across stitched-together chapters, inspect BibTeX/reference quality, diagnose LaTeX/PDF compilation or cross-reference problems, or produce a review-first thesis revision plan.
---

# Thesis Revision

## Core Contract

Use this skill to run a review-first workflow for LaTeX thesis revision. Focus on non-logical parts: examiner-comment handling, grammar, structure, style consistency, terminology, notation, citations, bibliography, abstracts, cross-references, compilation, and PDF presentation.

Default to "report and plan first, edit after confirmation" unless the user explicitly requests direct edits. Preserve the thesis's technical claims, theorem statements, algorithms, experiments, and conclusions except for small language or reference corrections needed by the user.

Do not assume a fixed template, folder layout, discipline, old-version directory, terminology set, or citation package. Infer the thesis structure and style from the current project.

## Workflow

1. Ground in the project.
   - Identify the main TeX file, chapter/front-matter files, bibliography files, build scripts, generated PDF, and template/class files.
   - Check whether the worktree is dirty before making edits. Never revert unrelated user changes.
   - Treat template/class files, copyright pages, originality statements, publications lists, and old/submitted versions as sensitive; edit them only when the user explicitly asks.

2. Build a thesis style profile.
   - Extract chapter/section headings, abstract and keywords, notation sections, theorem/algorithm environments, cross-reference style, bibliography style, and recurring technical terms.
   - Derive preferred terminology and title style from the project; do not impose a discipline-specific vocabulary unless the user gives one.
   - If chapters are adapted from papers, look for duplicated introductions, inconsistent contribution wording, repeated definitions, notation collisions, and mixed style conventions.

3. Review before editing.
   - For examiner comments, produce a tracking table with: comment, location, proposed minimal fix, risk level, and verification method.
   - For thesis-wide grammar checks, inspect prose by chapter or section after filtering out LaTeX commands, formulas, citations, and bibliography noise.
   - Classify findings as "must fix", "should fix", or "leave/confirm".
   - Give concrete file/line references and distinguish real PDF issues from text-extraction artifacts.

4. Implement only after approval.
   - Make the smallest edits that satisfy the user goal.
   - Prefer local style and existing macros/packages over new conventions.
   - Keep prose edits academic but not verbose; avoid rewriting whole sections when a sentence-level fix is enough.
   - For bibliography changes, merge duplicates carefully and preserve keys when possible to avoid unnecessary citation churn.

5. Verify.
   - Run the project's normal build command if available.
   - Check logs for undefined references/citations, duplicate labels, rerun warnings, and BibTeX warnings.
   - Inspect PDF text or rendered pages for visible issues such as wrong TOC pages, broken cover title lines, repeated reference names, algorithm line-number references, malformed equation ranges, and bibliography formatting.
   - Report changed files, verification results, unresolved risks, and any issues intentionally left unchanged.

## References

Load only the reference file needed for the current task:

- `references/revision-workflow.md`: examiner-comment handling, risk classes, and review-first output format.
- `references/grammar-checklist.md`: thesis-wide grammar, academic prose, and LaTeX-aware language-review workflow.
- `references/consistency-checklist.md`: thesis-wide consistency across stitched chapters, abstracts, terms, notation, headings, and prose style.
- `references/bibliography-checklist.md`: BibTeX duplicate detection, formal-version preference, capitalization protection, and reference-field normalization.
- `references/latex-pdf-checklist.md`: LaTeX build, cross-reference, algorithm, TOC, PDF, and log checks.

## Optional Scripts

Use scripts as helpers, not as substitutes for reading the source:

```bash
python3 ~/.codex/skills/thesis-revision/scripts/scan_latex_thesis.py /path/to/thesis
python3 ~/.codex/skills/thesis-revision/scripts/check_bibliography.py /path/to/references.bib
```

The scripts emit Markdown reports with heuristic findings. Confirm each high-impact finding against the source or PDF before editing.
