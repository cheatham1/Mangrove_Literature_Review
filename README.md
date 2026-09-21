# Mangrove Plastics — Scoping Review Dashboard

Interactive dashboard for exploring findings from a scoping review of **plastic pollution in mangrove ecosystems**. It covers **260 sources** published between **1993 and 2026**, spanning peer-reviewed articles, grey literature, policy and legal documents, and intergovernmental reports.

## Dashboard tabs

- **Summary of evidence** — headline metrics; breakdowns by literature type, geographic region, quality band, and focus specificity (each pie annotated with a short insight); research-area volumes; the publication timeline by theme; and focus specificity over time.
- **Thematic findings** — a profile for each of the 7 research areas, with source counts, share peer-reviewed, recency, leading region, and characteristic keywords.
- **Evidence landscape** — literature-type composition, quality-score distribution and bands, mean quality by theme, quality by source type, a quantity-vs-quality bubble view, the research-area × region heatmap, and keyword frequencies.
- **Knowledge gaps** — geographic and thematic gaps, evidence recency by theme, and numbered research-priority recommendations.
- **Source table** — a searchable, sortable table of all 260 sources. Filter by theme, source type, region, focus specificity, or quality band, and follow the link to each source.

## Dataset columns

The `List refs` sheet contains one row per source across the following columns:

| Column | Description |
|--------|-------------|
| Research Area | One of 7 thematic categories |
| Focus area | Relevance specificity (in mangroves / mangrove-general / adjacent ecosystems) |
| Score on focus area | Numeric score (5 or 10) |
| Type of Literature | One of 7 source types (see below) |
| Score from type | Numeric score (3–5) |
| Title | Publication title |
| Abstract | Abstract or summary text |
| Author(s) | Author list |
| Year | Publication year (1993–2026) |
| DOI or Link | DOI or source URL |
| Keywords of note | Subject keywords (comma-separated) |
| Keywords | Whether keywords are present (Yes/No) |
| Keywords score (0 or 3) | Numeric score (0 or 3) |
| Geographic area | Region classification |
| Region Score | Numeric score (0 or 3) |
| Score total Calculation | Composite quality score (sum of the four scores above, max 21) |
| Percentage | Quality percentage, `Score total / 21 × 100` |
| Quality Score Colour | Quality band colour |
| citation | Formatted citation |

**Research areas (7):** State of Plastic Pollution in Mangroves · Impact Assessment · Policy and Governance Analysis · Microplastics, Chemical Additives & POPs · Ecosystem Services and Linkages · Transboundary Riverine Plastic & Chemical Pollution · Mitigation and Clean-up Practices

**Literature types (7):** Peer Reviewed Academic · Grey Literature · Intergovernmental sources · Policy and legal sources · Newsletters, Conferences, other sources · Online databases and repositories · Geographic/Map data

**Geographic regions:** Global · Asia / Middle East · Africa · Europe · Americas · Pacific / Oceania · Not noted

**Quality bands** (from `Percentage`): High (>70%) · Medium (40–70%) · Low (≤40%)

## Data notes

- **260 sources**, all with complete scoring.
- **173 (67%)** are peer-reviewed; the remainder is grey literature, policy/legal, and intergovernmental material.
- **95%** of sources fall in the high quality band (>70%).
- The dataset is de-duplicated: two sources sharing the generic title "Mapping data source" are distinct records (a river-hydrography dataset and an administrative-boundaries dataset) and are intentionally retained.

## Licence

Dataset and dashboard code provided for research purposes.
