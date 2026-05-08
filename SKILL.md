---
name: thesis-revision
description: Review and minimally revise LaTeX theses or dissertations for non-technical-logical issues before submission, defense, or expert re-review. Use when the user asks to handle examiner comments, draft official Chinese revision/advisor-response materials, run thesis-wide grammar/prose checks, generate a project style sheet, polish abstracts, check bilingual consistency, normalize terminology/notation/style across stitched-together chapters, inspect BibTeX/reference quality, verify formal publication versions, diagnose LaTeX/PDF compilation or cross-reference problems, produce a review-first thesis revision plan, or coordinate approved thesis edits through the companion revision-check approval skill.
---

# Thesis Revision

## Core Contract

Use this skill to run a review-first workflow for LaTeX thesis revision. Focus on non-logical parts: examiner-comment handling, grammar, structure, style consistency, terminology, notation, citations, bibliography, abstracts, cross-references, compilation, and PDF presentation.

Default to "report and plan first, edit after confirmation" unless the user explicitly requests direct edits. Preserve the thesis's technical claims, theorem statements, algorithms, experiments, and conclusions except for small language or reference corrections needed by the user.

Do not assume a fixed template, folder layout, discipline, old-version directory, terminology set, or citation package. Infer the thesis structure and style from the current project.

Use `revision-check` as the approval skill when edits need user approval. `thesis-revision` owns thesis-specific diagnosis and edit planning; `revision-check` owns approval-page generation, approval JSON handling, ignored-item suppression, and applying only approved edits. If `revision-check` is not installed and the user wants click-based approval, ask the user to install it from `https://github.com/nht2018/revision-check.git` as `revision-check`.

## Workflow

1. Ground in the project.
   - Identify the main TeX file, chapter/front-matter files, bibliography files, build scripts, generated PDF, and template/class files.
   - Check whether the worktree is dirty before making edits. Never revert unrelated user changes.
   - Treat template/class files, copyright pages, originality statements, publications lists, and old/submitted versions as sensitive; edit them only when the user explicitly asks.

2. Build a thesis style profile.
   - Extract chapter/section headings, abstract and keywords, notation sections, theorem/algorithm environments, cross-reference style, bibliography style, and recurring technical terms.
   - Derive preferred terminology and title style from the project; do not impose a discipline-specific vocabulary unless the user gives one.
   - When the user asks for consistency work, create or update a project style sheet and use it as the local source of truth.
   - If chapters are adapted from papers, look for duplicated introductions, inconsistent contribution wording, repeated definitions, notation collisions, and mixed style conventions.

3. Review before editing.
   - For examiner comments, produce a tracking table with: comment, location, proposed minimal fix, risk level, and verification method.
   - When requested, draft a Chinese "revision or non-revision explanation for examiner comments" and a separate "advisor opinion" draft for official thesis materials. Mark advisor text as a draft that must be confirmed and signed by the advisor.
   - For official examiner-response materials, base each item's wording on approval status: approved and applied items become "修改说明"; unapproved, ignored, cancelled, or not-yet-approved items become "不修改说明" or "暂未修改说明". Never describe an examiner comment as revised unless the corresponding edit was approved and verified.
   - For thesis-wide grammar checks, inspect prose by chapter or section after filtering out LaTeX commands, formulas, citations, and bibliography noise.
   - Classify findings as "must fix", "should fix", or "leave/confirm".
   - Give concrete file/line references and distinguish real PDF issues from text-extraction artifacts.

4. Route approval through `revision-check` when approval is required.
   - For any nontrivial source edits after a review plan, use the installed `$revision-check` workflow unless the user explicitly asks for direct edits without an approval page.
   - Convert thesis findings into `revision-check` review items with concrete locations, occurrence counts, issue types, current/proposed text, reasons, and priorities.
   - Let `revision-check` open the local `Revision Review` approval page and apply only the approved items.
   - Preserve the mapping between examiner comments and `revision-check` item IDs so that official response materials can distinguish approved modifications from unapproved or ignored proposals.
   - Do not duplicate or bypass `revision-check` approval logic inside this skill.

5. Implement only after approval.
   - Make the smallest edits that satisfy the user goal.
   - Prefer local style and existing macros/packages over new conventions.
   - Keep prose edits academic but not verbose; avoid rewriting whole sections when a sentence-level fix is enough.
   - For bibliography changes, merge duplicates carefully and preserve keys when possible to avoid unnecessary citation churn.

6. Verify.
   - Run the project's normal build command if available.
   - Check logs for undefined references/citations, duplicate labels, rerun warnings, and BibTeX warnings.
   - Inspect PDF text or rendered pages for visible issues such as wrong TOC pages, broken cover title lines, repeated reference names, algorithm line-number references, malformed equation ranges, and bibliography formatting.
   - Before drafting official examiner-response materials, reconcile the final approval JSON, applied edits, ignored items, and validation results into a per-comment status table.
   - Report changed files, verification results, unresolved risks, and any issues intentionally left unchanged.

## References

Load only the reference file needed for the current task:

- `references/revision-workflow.md`: examiner-comment handling, risk classes, and review-first output format.
- `references/examiner-response.md`: Chinese official revision-explanation and advisor-opinion templates.
- `references/grammar-checklist.md`: thesis-wide grammar, academic prose, and LaTeX-aware language-review workflow.
- `references/style-sheet.md`: project-level style sheet generation for terms, notation, headings, citations, and bilingual wording.
- `references/consistency-checklist.md`: thesis-wide consistency across stitched chapters, abstracts, terms, notation, headings, and prose style.
- `references/bibliography-checklist.md`: BibTeX duplicate detection, formal-version preference, capitalization protection, and reference-field normalization.
- `references/latex-pdf-checklist.md`: LaTeX build, cross-reference, algorithm, TOC, PDF, and log checks.

## Optional Scripts

Use scripts as helpers, not as substitutes for reading the source:

```bash
python3 ~/.codex/skills/thesis-revision/scripts/scan_latex_thesis.py /path/to/thesis
python3 ~/.codex/skills/thesis-revision/scripts/check_bibliography.py /path/to/references.bib
python3 ~/.codex/skills/thesis-revision/scripts/extract_thesis_prose.py /path/to/thesis
python3 ~/.codex/skills/thesis-revision/scripts/generate_style_sheet.py /path/to/thesis
python3 ~/.codex/skills/thesis-revision/scripts/generate_examiner_response.py comments.txt --out revision-response.md
```

The scripts emit Markdown reports with heuristic findings. Confirm each high-impact finding against the source or PDF before editing.
