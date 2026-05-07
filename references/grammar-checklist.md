# Grammar Checklist

Use this guide for full-thesis grammar and prose checks. Keep it separate from logical review: do not change mathematical meaning, assumptions, claims, theorem statements, algorithms, experiments, or conclusions.

## LaTeX-Aware Preparation

- Work from source files when making edits, but use compiled PDF or extracted text to spot visible prose problems.
- Ignore or manually protect LaTeX commands, labels, citations, equations, tables, code-like algorithm lines, and BibTeX entries during grammar scanning.
- If available, use tools such as `detex`, `pdftotext`, or LanguageTool only as aids. Treat their output as noisy in math-heavy text.
- Review chapter by chapter; do not apply global replacements without checking local context.

## Enhanced Full-Thesis Pass

Use an enhanced pass when the user asks for "全文语法检查" or a submission-ready language pass:

1. Extract prose by included TeX file rather than scanning every archived file.
2. Split prose into manageable paragraphs or section-level chunks.
3. Run a tool-assisted check when available, but verify every suggestion in the source.
4. Report findings by chapter with severity and exact source location when possible.
5. Apply only low-risk grammar fixes automatically after approval; keep claim-level rephrasing as suggestions.

Optional helper:

```bash
python3 ~/.codex/skills/thesis-revision/scripts/extract_thesis_prose.py /path/to/thesis > prose.md
```

## Must-Fix Grammar

Flag and correct:

- Missing verbs, wrong verb forms, subject-verb disagreement, article errors that change readability, and malformed sentence structure.
- Incorrect singular/plural agreement for mathematical objects, algorithms, assumptions, and results.
- Broken citation spacing or ungrammatical citation phrases.
- Obvious typo residues from editing, duplicated words, missing spaces, and wrong punctuation around clauses.
- Inconsistent tense within the same paragraph when it is not intentional.

## Academic Prose Polish

Suggest but do not force:

- More precise academic wording for vague phrases such as "good", "bad", "very", or unsupported "significant".
- Shorter sentences when nested clauses obscure the main claim.
- Consistent use of "this thesis", "this chapter", and "we" according to the local style.
- Smoother transitions between chapters adapted from papers.
- Removing redundant sentences introduced by paper stitching.

## Risk Control

- Classify edits that only fix grammar as low risk.
- Classify edits that rephrase claims, limitations, or contributions as medium risk and show the proposed wording before applying.
- Treat changes to theorem statements, assumptions, algorithm descriptions, and experimental claims as high risk unless the user explicitly requests them.

## Output

For a full grammar pass, report:

- Files or chapters reviewed.
- Must-fix grammar issues with locations.
- Optional prose-polish suggestions grouped by chapter.
- Any sections skipped because they are math-heavy, generated, administrative, or outside the requested scope.
