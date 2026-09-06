# Portfolio Analyser – Live Prices + Research Dashboard

Interactive Streamlit app with:

- Full portfolio analysis (as of 4-Sep-2026 holdings)
- **Live market prices** via Yahoo Finance (free)
- **Historical price charts** (3mo / 6mo / 1y / 2y)
- EXIT / OVERRIDE / HOLD recommendations
- Sector deep-dive & Core+Satellite framework

## Deploy free on Streamlit Cloud

1. Push this folder to a **public** GitHub repo  
2. Go to https://share.streamlit.io → New app → select repo → `app.py`  
3. Deploy

After any code change, reboot the app from “Manage app”.

## Local run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Live data notes

- Prices and history come from Yahoo Finance (`.NS` tickers).
- Quotes are often delayed 15–20 minutes.
- Some micro-caps or newly listed names may return “N/A”.
- Data is cached 5–10 minutes to stay within free limits.

**Not investment advice.** Always cross-check live prices on NSE/BSE or your broker.
