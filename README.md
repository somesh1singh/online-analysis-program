# Portfolio Analyser – Free Online Research Dashboard

Detailed interactive analysis of the 52-stock portfolio (as of 4-Sep-2026) with:

- Dashboard (value, P&L, sector pie, top gainers/losers)
- Full holdings table with search / filter / sort
- Explicit EXIT / OVERRIDE / HOLD recommendations
- Sector deep-dive
- Individual stock research cards
- Core + Satellite rebalancing framework
- Independent research notes synthesised from public results & news

**Not investment advice.**

---

## Run for FREE online (easiest)

### Option 1 – Streamlit Community Cloud (recommended)

1. Create a free GitHub account (if you don’t have one).
2. Create a new **public** repository.
3. Upload the three files: `app.py`, `requirements.txt`, `README.md`.
4. Go to [https://share.streamlit.io](https://share.streamlit.io) → Sign in with GitHub.
5. Click **“New app”** → select your repo → main file `app.py` → Deploy.
6. You get a permanent public URL (e.g. `https://yourname-portfolio-analyser.streamlit.app`).

Anyone can open the link on phone or laptop. No credit card required.

### Option 2 – Run on your computer

```bash
pip install streamlit pandas plotly
streamlit run app.py
```

Opens at http://localhost:8501

### Option 3 – Google Colab

Upload `app.py` to Colab and use a Streamlit tunnel (or simply run the analysis cells if you convert it).

---

## What the app contains

| Page | Content |
|------|---------|
| Dashboard | Snapshot metrics, sector pie, top 5 gainers & losers, research summary |
| All Holdings | Searchable / filterable table of all 52 stocks |
| Actions & Recs | EXIT list, OVERRIDE list, Core HOLD candidates, cash reclaim |
| Sectors | Bar chart + table of sector P&L and weights |
| Stock Deep Dive | Full card for any stock + independent research note |
| Rebalance Framework | Core+Satellite, sector consolidation, barbell approaches |
| About | How to run + full disclaimer |

Data is embedded (no external API calls). Works offline after first load once deployed.
