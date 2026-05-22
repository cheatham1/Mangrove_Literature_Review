"""
Scoping Review Findings — Plastic Pollution in Mangrove Ecosystems
Interactive Streamlit dashboard for exploring 152 peer-reviewed and grey literature sources.

Requirements:
    pip install streamlit pandas plotly

Run:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import os

# ──────────────────────────────────────────────
# Page configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Mangrove Plastics — Scoping Review",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600&family=Outfit:wght@300;400;500;600&display=swap');
    
    .main .block-container {
        max-width: 1100px;
        padding-top: 2rem;
    }
    h1, h2, h3 {
        font-family: 'Source Serif 4', Georgia, serif;
        color: #1A1A18;
    }
    .stMetric label {
        font-family: 'Outfit', sans-serif;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #908E88;
    }
    .stMetric [data-testid="stMetricValue"] {
        font-family: 'Source Serif 4', Georgia, serif;
        color: #1B7A5A;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 400;
    }
    div[data-testid="stExpander"] summary {
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Colour palette
# ──────────────────────────────────────────────
PALETTE = {
    "teal": "#1B7A5A",
    "amber": "#C8973A",
    "slate": "#5E5C56",
    "coral": "#D4654A",
    "blue": "#4A7FB5",
    "plum": "#8B5A8A",
    "sage": "#7A9E7E",
}
AREA_COLOURS = {
    "State of Plastic Pollution in Mangroves": PALETTE["teal"],
    "Impact Assessment": PALETTE["coral"],
    "Ecosystem Services and Linkages": PALETTE["sage"],
    "Policy and Governance Analysis": PALETTE["blue"],
    "Microplastics, Chemical Additives & POPs in ecosystems": PALETTE["plum"],
    "Transboundary Riverine Plastic & Chemical Pollution": PALETTE["amber"],
    "Mitigation and Clean-up Practices": PALETTE["slate"],
}
REGION_ORDER = ["Asia / Middle East", "Global", "Africa", "Americas", "Europe", "Pacific / Oceania"]


# ──────────────────────────────────────────────
# Load data
# ──────────────────────────────────────────────
@st.cache_data
def load_data():
    """Load the TSV dataset, looking in several locations."""
    candidates = [
        os.path.join(os.path.dirname(__file__), "mangrove_literature_review_data.tsv"),
        "mangrove_literature_review_data.tsv",
        os.path.join(os.path.dirname(__file__), "data", "mangrove_literature_review_data.tsv"),
    ]
    for path in candidates:
        if os.path.exists(path):
            df = pd.read_csv(path, sep="\t")
            df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
            df["Percentage"] = pd.to_numeric(df["Percentage"], errors="coerce")
            df["Score total Calculation"] = pd.to_numeric(df["Score total Calculation"], errors="coerce")
            return df
    st.error("Dataset file `mangrove_literature_review_data.tsv` not found. "
             "Place it in the same directory as this script.")
    st.stop()


df = load_data()
n_total = len(df)
n_peer = len(df[df["Type of Literature"] == "Peer Reviewed Academic"])
year_min = int(df["Year"].min())
year_max = int(df["Year"].max())
pct_recent = round(len(df[df["Year"] >= 2023]) / n_total * 100)

# ──────────────────────────────────────────────
# Header
# ──────────────────────────────────────────────
st.markdown(
    "<p style='font-size:11px;text-transform:uppercase;letter-spacing:2.5px;"
    "color:#1B7A5A;font-weight:600;margin-bottom:0'>Scoping Review</p>",
    unsafe_allow_html=True,
)
st.title("Plastic Pollution in Mangrove Ecosystems")
st.caption(
    f"{n_total} sources  ·  {year_min}–{year_max}  ·  "
    f"{pct_recent}% published since 2023  ·  "
    f"{round(n_peer / n_total * 100)}% peer-reviewed"
)
st.divider()

# ──────────────────────────────────────────────
# Tabs
# ──────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Summary of Evidence",
    "🔬 Thematic Findings",
    "🗺️ Evidence Landscape",
    "⚠️ Knowledge Gaps",
])

# ──────────────────────────────────────────────
# TAB 1 — Summary of Evidence
# ──────────────────────────────────────────────
with tab1:
    # Headline metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sources", n_total)
    c2.metric("Peer-Reviewed", n_peer)
    c3.metric("Research Areas", df["Research Area"].nunique())
    c4.metric("Regions Covered", df["Geographic area"].nunique())

    st.markdown("")

    col_l, col_r = st.columns([3, 2])

    # Bar: research area volumes
    with col_l:
        st.subheader("Evidence by Research Area")
        area_counts = df["Research Area"].value_counts().reset_index()
        area_counts.columns = ["Research Area", "Count"]
        fig = px.bar(
            area_counts.sort_values("Count"),
            y="Research Area", x="Count",
            orientation="h",
            color="Research Area",
            color_discrete_map=AREA_COLOURS,
            text="Count",
        )
        fig.update_layout(
            showlegend=False, height=340,
            margin=dict(l=0, r=20, t=10, b=10),
            xaxis_title="Number of sources",
            yaxis_title="",
            font=dict(family="Outfit, sans-serif"),
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    # Pie: literature types
    with col_r:
        st.subheader("Literature Types")
        type_counts = df["Type of Literature"].value_counts().reset_index()
        type_counts.columns = ["Type", "Count"]
        fig2 = px.pie(
            type_counts, names="Type", values="Count",
            color_discrete_sequence=[PALETTE["teal"], PALETTE["amber"],
                                     PALETTE["blue"], PALETTE["slate"]],
            hole=0.45,
        )
        fig2.update_layout(
            height=340,
            margin=dict(l=0, r=0, t=10, b=10),
            font=dict(family="Outfit, sans-serif"),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Timeline
    st.subheader("Publication Timeline")
    yr_counts = df.groupby("Year").size().reset_index(name="Count")
    fig3 = px.bar(
        yr_counts, x="Year", y="Count",
        text="Count",
        color_discrete_sequence=[PALETTE["teal"]],
    )
    fig3.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=10),
        xaxis_title="Year", yaxis_title="Sources published",
        font=dict(family="Outfit, sans-serif"),
    )
    fig3.update_traces(textposition="outside")
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(
        f"Research output has accelerated sharply: {pct_recent}% of the corpus "
        f"was published from 2023 onward, reflecting growing scientific and policy "
        f"attention to plastics in mangrove ecosystems."
    )

    # Geographic distribution
    st.subheader("Geographic Distribution")
    geo_counts = df["Geographic area"].value_counts().reindex(REGION_ORDER).reset_index()
    geo_counts.columns = ["Region", "Count"]
    geo_counts["Pct"] = (geo_counts["Count"] / n_total * 100).round(1)
    fig4 = px.bar(
        geo_counts, x="Region", y="Count",
        text=geo_counts.apply(lambda r: f"{r['Count']} ({r['Pct']}%)", axis=1),
        color_discrete_sequence=[PALETTE["teal"]],
    )
    fig4.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=10, b=10),
        xaxis_title="", yaxis_title="Sources",
        font=dict(family="Outfit, sans-serif"),
    )
    fig4.update_traces(textposition="outside")
    st.plotly_chart(fig4, use_container_width=True)
    st.caption(
        "Asia/Middle East dominates the evidence base — reflecting where most primary "
        "mangrove-plastics field research has been conducted. Africa, the Americas, and "
        "Pacific/Oceania are underrepresented relative to their mangrove extent."
    )


# ──────────────────────────────────────────────
# TAB 2 — Thematic Findings
# ──────────────────────────────────────────────
with tab2:
    st.subheader("Research Area Profiles")
    st.caption("Key metrics and dominant themes for each of the seven research areas.")

    for area in sorted(AREA_COLOURS.keys()):
        sub = df[df["Research Area"] == area]
        n = len(sub)
        pr_pct = round(len(sub[sub["Type of Literature"] == "Peer Reviewed Academic"]) / n * 100) if n else 0
        recent = round(len(sub[sub["Year"] >= 2023]) / n * 100) if n else 0
        top_region = sub["Geographic area"].mode().iloc[0] if n else "—"

        # Collect keywords
        kws = []
        for v in sub["Keywords of note"].dropna():
            kws.extend([k.strip() for k in v.split(",") if k.strip()])
        top_kw = ", ".join([w for w, _ in Counter(kws).most_common(5)]) if kws else "—"

        colour = AREA_COLOURS.get(area, "#888")
        with st.expander(f"**{area}** — {n} sources", expanded=False):
            mc1, mc2, mc3, mc4 = st.columns(4)
            mc1.metric("Sources", n)
            mc2.metric("Peer-Reviewed", f"{pr_pct}%")
            mc3.metric("Since 2023", f"{recent}%")
            mc4.metric("Top Region", top_region)
            st.markdown(f"**Dominant keywords:** {top_kw}")

            # Mini bar by year
            ysub = sub.groupby("Year").size().reset_index(name="Count")
            figm = px.bar(ysub, x="Year", y="Count",
                          color_discrete_sequence=[colour], height=180)
            figm.update_layout(margin=dict(l=0, r=0, t=5, b=5),
                               xaxis_title="", yaxis_title="",
                               font=dict(family="Outfit"))
            st.plotly_chart(figm, use_container_width=True)


# ──────────────────────────────────────────────
# TAB 3 — Evidence Landscape
# ──────────────────────────────────────────────
with tab3:
    # Literature type by research area — stacked bar
    st.subheader("Literature Type by Research Area")
    cross = pd.crosstab(df["Research Area"], df["Type of Literature"])
    cross_pct = cross.div(cross.sum(axis=1), axis=0) * 100

    fig5 = go.Figure()
    lit_colours = {
        "Peer Reviewed Academic": PALETTE["teal"],
        "Grey Literature": PALETTE["amber"],
        "Intergovernmental sources (Ramsar, BRS)": PALETTE["blue"],
    }
    for lit_type in cross.columns:
        fig5.add_trace(go.Bar(
            y=cross.index, x=cross_pct[lit_type],
            name=lit_type, orientation="h",
            marker_color=lit_colours.get(lit_type, PALETTE["slate"]),
            text=cross_pct[lit_type].round(0).astype(int).astype(str) + "%",
            textposition="inside",
        ))
    fig5.update_layout(
        barmode="stack", height=380,
        margin=dict(l=0, r=20, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2),
        xaxis_title="Percentage of sources",
        yaxis_title="",
        font=dict(family="Outfit, sans-serif"),
    )
    st.plotly_chart(fig5, use_container_width=True)
    st.caption(
        "Transboundary riverine research has the strongest peer-reviewed backing. "
        "Policy and governance analysis relies more heavily on grey literature and "
        "intergovernmental sources."
    )

    st.divider()

    # Quality score distribution
    st.subheader("Quality Score Distribution")
    scores = df["Percentage"].dropna()
    fig6 = px.histogram(
        scores, nbins=15,
        color_discrete_sequence=[PALETTE["teal"]],
        labels={"value": "Quality score (%)", "count": "Frequency"},
    )
    fig6.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=10),
        showlegend=False,
        font=dict(family="Outfit, sans-serif"),
    )
    # Quality band annotations
    fig6.add_vrect(x0=90, x1=100, fillcolor=PALETTE["teal"], opacity=0.08,
                   annotation_text="High", annotation_position="top")
    fig6.add_vrect(x0=70, x1=90, fillcolor=PALETTE["amber"], opacity=0.08,
                   annotation_text="Medium", annotation_position="top")
    fig6.add_vrect(x0=0, x1=70, fillcolor=PALETTE["coral"], opacity=0.08,
                   annotation_text="Low", annotation_position="top")
    st.plotly_chart(fig6, use_container_width=True)

    st.divider()

    # Heatmap: Research Area × Region
    st.subheader("Research Area × Geographic Region")
    heatmap_data = pd.crosstab(df["Research Area"], df["Geographic area"])
    # Reorder columns
    heatmap_data = heatmap_data.reindex(columns=REGION_ORDER, fill_value=0)

    fig7 = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns.tolist(),
        y=heatmap_data.index.tolist(),
        color_continuous_scale=["#F6F4F0", PALETTE["teal"]],
        text_auto=True,
        aspect="auto",
    )
    fig7.update_layout(
        height=380,
        margin=dict(l=0, r=0, t=10, b=10),
        font=dict(family="Outfit, sans-serif"),
        xaxis_title="", yaxis_title="",
    )
    st.plotly_chart(fig7, use_container_width=True)
    st.caption(
        "Darker cells indicate higher concentration. The strongest cluster is "
        "plastic pollution research in Asia/Middle East. Policy and governance "
        "research is predominantly global-level. Notable gaps: transboundary "
        "research outside the global level, and mitigation studies in Africa, "
        "Americas, and Pacific."
    )

    st.divider()

    # Keyword frequencies
    st.subheader("Keyword Frequencies")
    all_kws = []
    for v in df["Keywords of note"].dropna():
        all_kws.extend([k.strip().lower() for k in v.split(",") if k.strip()])
    kw_counts = Counter(all_kws).most_common(20)
    kw_df = pd.DataFrame(kw_counts, columns=["Keyword", "Count"])
    fig8 = px.bar(
        kw_df.sort_values("Count"), y="Keyword", x="Count",
        orientation="h", color_discrete_sequence=[PALETTE["teal"]],
        text="Count",
    )
    fig8.update_layout(
        height=500,
        margin=dict(l=0, r=20, t=10, b=10),
        xaxis_title="Frequency", yaxis_title="",
        font=dict(family="Outfit, sans-serif"),
    )
    fig8.update_traces(textposition="outside")
    st.plotly_chart(fig8, use_container_width=True)


# ──────────────────────────────────────────────
# TAB 4 — Knowledge Gaps
# ──────────────────────────────────────────────
with tab4:
    st.subheader("Geographic Coverage Gaps")
    gaps = [
        ("Pacific / Oceania", df["Geographic area"].value_counts().get("Pacific / Oceania", 0),
         "Papua New Guinea, Fiji, Solomon Islands have extensive mangroves but almost "
         "no plastic pollution research in the dataset."),
        ("Americas", df["Geographic area"].value_counts().get("Americas", 0),
         "Brazil, Mexico, Caribbean — significant mangrove coverage but underrepresented "
         "relative to Asia."),
        ("Africa", df["Geographic area"].value_counts().get("Africa", 0),
         "West African mangroves (Nigeria, Cameroon, Senegal) particularly underrepresented; "
         "most Africa references focus on East Africa."),
        ("Europe", df["Geographic area"].value_counts().get("Europe", 0),
         "Research mostly on microplastic methodology; limited field studies in "
         "Mediterranean or Atlantic mangrove-adjacent environments."),
    ]
    for region, count, note in gaps:
        with st.container():
            g1, g2 = st.columns([1, 5])
            g1.metric(region, f"{count} refs")
            g2.caption(note)

    st.divider()

    # Thematic gaps
    st.subheader("Thematic Gaps")
    thematic_gaps = [
        "**Mitigation effectiveness** — only 16 sources address clean-up and mitigation; "
        "almost none evaluate what actually works.",
        "**Nanoplastics** — a single study on nanoplastic contamination in the entire corpus. "
        "This is an emerging pollutant class with almost no mangrove-specific evidence.",
        "**Economic valuation** — no dedicated cost-benefit analyses of plastic pollution "
        "impacts on mangrove ecosystem services.",
        "**Community and indigenous knowledge** — socio-economic research exists but is "
        "overwhelmingly quantitative; qualitative community perspectives are missing.",
        "**Middle East disaggregation** — currently merged with Asia, obscuring "
        "petrochemical-specific pollution dynamics in Gulf mangroves.",
    ]
    for gap in thematic_gaps:
        st.markdown(f"- {gap}")

    st.divider()

    # Evidence recency by theme
    st.subheader("Evidence Recency by Research Area")
    recency = df.groupby("Research Area")["Year"].agg(["mean", "median", "max"]).round(1)
    recency.columns = ["Mean Year", "Median Year", "Latest"]
    recency = recency.sort_values("Mean Year")
    st.dataframe(recency, use_container_width=True)

    st.divider()

    # Recommendations
    st.subheader("Research Priorities")
    recs = [
        "Expand field research in Pacific/Oceania and the Americas to match the "
        "geographic range of mangrove ecosystems.",
        "Commission transboundary case studies on specific river-to-mangrove corridors "
        "(Mekong, Niger, Ganges) to complement existing global-level analyses.",
        "Fund longitudinal studies evaluating the effectiveness of mangrove clean-up "
        "and mitigation interventions, including cost-benefit analyses.",
        "Investigate nanoplastic contamination in mangrove sediments and biota as an "
        "emerging pollutant class.",
        "Integrate community and indigenous knowledge into impact assessments, moving "
        "beyond quantitative socioeconomic indicators.",
        "Support research on plastics as vectors for POPs transport in mangrove food webs, "
        "bridging the current siloed treatment of these two pollutant classes.",
        "Disaggregate Middle East mangrove research from the broader Asia category to "
        "capture petrochemical-specific pollution dynamics.",
        "Establish standardised assessment methodologies for plastic pollution in mangroves "
        "to enable cross-site and cross-regional comparisons.",
    ]
    for i, rec in enumerate(recs, 1):
        st.markdown(f"**{i}.** {rec}")


# ──────────────────────────────────────────────
# Sidebar — download dataset
# ──────────────────────────────────────────────
with st.sidebar:
    st.header("📥 Download Data")
    tsv_data = df.to_csv(sep="\t", index=False)
    st.download_button(
        label="Download dataset (TSV)",
        data=tsv_data,
        file_name="mangrove_literature_review_data.tsv",
        mime="text/tab-separated-values",
    )
    st.caption(
        f"{n_total} sources · {year_min}–{year_max} · "
        f"Cleaned from original 224-row spreadsheet (70 empty placeholders removed, "
        f"2 malformed records merged)."
    )
    st.divider()
    st.caption("Built with Streamlit · Data from scoping review of plastic pollution "
               "in mangrove ecosystems.")
