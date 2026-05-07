# Bibliography Checklist

Use this guide when editing `.bib` files, reference lists, publication lists, or examiner comments about references.

## Duplicate and Version Checks

- Group likely duplicates by DOI, arXiv identifier, normalized title, and close title similarity.
- When the same work appears as preprint, conference, and journal versions, prefer the formally published version unless:
  - only the preprint is cited for content absent from the published version,
  - the field convention cites the preprint,
  - the user explicitly wants the preprint.
- Preserve existing citation keys when possible. If keys are merged, update all citations and verify no undefined citations remain.

## Capitalization Protection

BibTeX styles may downcase title words. Protect words that must retain capitalization with braces:

- Acronyms and initialisms: `{SDP}`, `{ADMM}`, `{PDE}`, `{QRAM}`, `{AI}`.
- Proper nouns, software names, datasets, theorem/method names, and named algorithms.
- Mixed-case technical terms whose capitalization is meaningful.

Do not blindly brace entire titles unless the project already follows that style. Prefer bracing the smallest necessary word or phrase.

## Field Normalization

Check:

- Author names are in a BibTeX-safe form and not reversed incorrectly.
- Journal, booktitle, publisher, and conference names use consistent official capitalization.
- Edition fields use conventional forms such as `2nd edition`.
- URL fields have no inserted spaces and use `url = {...}` or `howpublished` consistently.
- DOI/arXiv/eprint fields are present when useful and not duplicated in the title.
- Version, year, volume, number, pages, and punctuation do not produce malformed output.

## Verification

- Run BibTeX through the project build.
- Inspect `.blg` for warnings.
- Inspect generated references in the PDF or `.bbl`, because some formatting problems appear only after style processing.
- Re-run scans for undefined citations after deleting or merging entries.
