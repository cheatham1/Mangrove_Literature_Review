# Mangrove Plastics — Scoping Review Dashboard

Interactive dashboard for exploring findings from a scoping review of **plastic pollution in mangrove ecosystems**, covering 152 peer-reviewed and grey literature sources (2002–2026).

## Quick Start

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set **Main file path** to `app.py`
5. Deploy

## Files

| File | Description |
|------|-------------|
| `app.py` | Streamlit dashboard application |
| `mangrove_literature_review_data.tsv` | Cleaned dataset (152 sources, 17 columns) |
| `requirements.txt` | Python dependencies |

## Dashboard Tabs

- **Summary of Evidence** — headline metrics, research area volumes, publication timeline, geographic distribution
- **Thematic Findings** — expandable profiles for each of the 7 research areas with key metrics and keywords
- **Evidence Landscape** — literature type composition, quality score distribution, research area × region heatmap, keyword frequencies
- **Knowledge Gaps** — geographic and thematic gaps, evidence recency, 8 numbered research priority recommendations

## Dataset Columns

| Column | Description |
|--------|-------------|
| Research Area | One of 7 thematic categories |
| Focus area | Relevance specificity |
| Score on focus area | Numeric score (3–10) |
| Type of Literature | Peer Reviewed Academic / Grey Literature / Intergovernmental |
| Score from type | Numeric score (4–5) |
| Title | Publication title |
| Year | Publication year |
| Keywords of note | Subject keywords |
| Keywords | Whether keywords present (Yes/No) |
| Keywords score | 0 or 3 |
| Geographic area | Region classification |
| Region Score | Numeric score |
| Score total Calculation | Composite quality score |
| Percentage | Quality percentage (0–100) |
| Quality Score Colour | Quality band colour |
| Included | Inclusion status |
| Excluded | Exclusion status |

## Data Notes

The original spreadsheet contained 224 rows. During analysis, 70 empty placeholder rows (containing only `#N/A` scores) and 2 malformed records were identified and removed, yielding 152 valid sources with complete scoring.

## Licence

Dataset and dashboard code provided for research purposes.
