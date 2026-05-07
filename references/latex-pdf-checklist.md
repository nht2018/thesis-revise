# LaTeX and PDF Checklist

Use this guide when the user reports compilation failures, wrong PDF output, or cross-reference/reference problems.

## Build Diagnosis

- Prefer the project build script if present (`compile.sh`, `latexmkrc`, `Makefile`, or documented command).
- Check logs for fatal errors, undefined control sequences, missing files, undefined citations/references, duplicate labels, BibTeX warnings, and rerun messages.
- Distinguish warnings that affect correctness from layout-only warnings such as minor overfull boxes.

## Cross-References

Check for:

- Hard-coded numbers such as `Theorem 6`, `Algorithm 1`, or `Proposition 1` when labels exist.
- Repeated automatic names such as `Lemma Lemma 3.1`.
- Algorithm line labels used where the algorithm float label was intended.
- Equation ranges rendered as `Equation (1)-Equation (2)` when prose should use `Equations (1)-(2)` or `(1)-(2)`.
- Missing spaces before citations such as `in\cite{...}` or `in[12]`.
- Labels placed before captions in floats when the number should refer to the float.

## PDF Presentation

Inspect the generated PDF when layout matters:

- Cover title line breaks, especially in long titles.
- Table of contents page numbers for references, publications, appendices, and acknowledgments.
- Blank pages with unwanted headers/footers if template rules allow changing them.
- Algorithm environments for doubled punctuation such as `.;`.
- Bibliography entries for capitalization, duplicate entries, URL spacing, and malformed punctuation.

## Text Extraction Caveat

`pdftotext` is useful but imperfect. Page numbers, math, hyphenation, and line breaks can create false positives. Confirm suspicious text against the source or rendered PDF before editing.
