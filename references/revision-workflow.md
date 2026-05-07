# Revision Workflow

Use this guide when the user provides examiner comments, asks for a thesis-wide pass, or requests edits after a review plan.

## Intake

- Collect the source of truth: current thesis files, examiner comments, any submitted/old versions, and the generated PDF if present.
- If old/submitted versions exist, use them only for comparison unless the user asks to restore content.
- Identify sensitive files before editing: class/template files, copyright pages, originality statements, publication lists, acknowledgments, and administrative metadata.

## Comment Tracking

For each comment, record:

- `Comment`: quote or paraphrase the examiner request.
- `Location`: chapter/section/page/file line if available.
- `Action`: minimal change needed.
- `Risk`: low for typos and formatting, medium for prose additions, high for technical content or template/admin changes.
- `Verification`: build, PDF inspection, grep, bibliography check, or manual read.

Prefer a table for user-facing plans. Keep comments marked "already fixed" only after checking the current source/PDF.

## Minimal Edit Policy

- Fix clear grammar, typo, spacing, capitalization, cross-reference, and bibliography defects directly after approval.
- For structural additions requested by examiners, add a compact paragraph in the most natural place; avoid broad rewrites.
- For ambiguous preferences, propose the smallest two or three options and recommend one.
- Preserve theorem statements, proofs, algorithms, experiments, claims, and numeric results unless the user explicitly asks for content-level revision.

## Verification Report

After edits, report:

- Files changed.
- Build command and result.
- Reference/citation warnings found or absent.
- PDF-visible checks performed.
- Remaining issues that are stylistic, optional, or require user judgment.
