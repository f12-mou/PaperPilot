# PaperPilot Repository Instructions

PaperPilot is a configurable literature-review pipeline.

The core codebase should remain domain-independent. Domain-specific behavior should come primarily from:

- `configs/`
- `schemas/`
- `prompts/`

Do not hard-code GRN-specific logic into the Python source unless absolutely necessary.

## Stage 0: Paper Discovery

When asked to perform paper discovery:

1. Read the active config file.
2. Read the configured `paper_finder` prompt.
3. For every method listed under `algorithms`:
   - identify the primary paper introducing the method
   - verify the title, authors, year, venue, DOI, and source
   - prefer the peer-reviewed publication when available
   - download the paper PDF
   - save it inside the configured papers directory
   - rename it using the canonical algorithm name
4. Update the configured paper manifest JSON.
5. Do not silently guess when multiple papers are plausible.
6. Mark ambiguous or unavailable papers using the statuses defined by the workflow.
7. Do not analyze a paper unless its manifest status is `verified`.

## Extraction

When performing initial extraction:

1. Read the active schema file.
2. Read `prompts/extractor.md`.
3. Analyze only verified papers.
4. Produce one row per method.
5. Preserve supporting evidence and page numbers.
6. Do not guess missing information.
7. Save the initial table as `table_v0.csv`.
8. Save supporting evidence in a structured JSON file.

## Critique

The independent critic is handled by the configured external model.

Do not replace the critic with Claude unless explicitly requested.

## Revision

When revising:

1. Read the critic report.
2. Re-check the original paper.
3. Do not blindly accept critic suggestions.
4. Modify only justified fields.
5. Update evidence and confidence when needed.
6. Maintain a changelog.

## General Rules

- Preserve reproducibility.
- Do not overwrite previous run outputs unnecessarily.
- Do not fabricate citations, metadata, or paper content.
- Prefer explicit uncertainty over unsupported certainty.
- Keep the codebase reusable across research domains.