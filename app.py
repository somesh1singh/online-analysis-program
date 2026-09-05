"""
Portfolio Analyser – Detailed Research Dashboard
Run free online via Streamlit Community Cloud or locally.
Data as of 4-Sep-2026 holdings + synthesised public research (Sep 2026).
Not investment advice.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

st.set_page_config(
    page_title="Portfolio Analyser | Sep 2026",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ───────────────────────────── DATA ─────────────────────────────
HOLDINGS = [
    {"symbol":"AGI","sector":"PACKAGING","qty":575,"lt":150,"st":425,"avg":685.25,"invested":394020,"ltp":736,"current":423200,"pnl":29180,"pnl_pct":7,"frame":"Satellite","action":"HOLD","signal":"Domestic demand-driven","tech":"Uptrend/relative strength","note":"Solid packaging play."},
    {"symbol":"BAJAJHFL","sector":"FINANCIAL SERVICES","qty":3700,"lt":1100,"st":2600,"avg":104.49,"invested":386626,"ltp":83,"current":307396,"pnl":-79230,"pnl_pct":-20,"frame":"Satellite","action":"HOLD","signal":"Sector de-rating (PSU/NBFC)","tech":"Downtrend/stabilizing","note":"Clean ~20% markdown."},
    {"symbol":"BBOX","sector":"TELECOM","qty":450,"lt":320,"st":130,"avg":623.71,"invested":280668,"ltp":712,"current":320513,"pnl":39845,"pnl_pct":14,"frame":"CORE","action":"HOLD","signal":"Strong (high ROE ~27-28%)","tech":"Uptrend/relative strength","note":"Best fundamental profile. AI/data-centre backlog surge. High ROE, expanding order book."},
    {"symbol":"BDL","sector":"DEFENCE","qty":315,"lt":150,"st":165,"avg":1521.68,"invested":479330,"ltp":1258,"current":396270,"pnl":-83060,"pnl_pct":-17,"frame":"CORE","action":"OVERRIDE","signal":"Strong orders / rich valuation","tech":"Downtrend (valuation correction)","note":"Order book ~₹26,000 Cr. Recent ₹1,348 Cr HAL order. PAT recovery. Overrule stop-loss."},
    {"symbol":"BECTORFOOD","sector":"FMCG","qty":1900,"lt":450,"st":1450,"avg":227.97,"invested":433143,"ltp":226,"current":429324,"pnl":-3819,"pnl_pct":-1,"frame":"Satellite","action":"HOLD","signal":"Domestic consumption-driven","tech":"Range-bound","note":"Profit +25.5%, biscuit/bakery growth."},
    {"symbol":"DATAPATTNS","sector":"DEFENCE","qty":15,"lt":0,"st":15,"avg":4441.44,"invested":66622,"ltp":4585,"current":68775,"pnl":2153,"pnl_pct":3,"frame":"Satellite","action":"HOLD","signal":"High gross margins 78.9%","tech":"Uptrend","note":"₹1,300 Cr HAL contract."},
    {"symbol":"DCXINDIA","sector":"ENGINEERING & CAPITAL GOODS","qty":575,"lt":450,"st":125,"avg":322.27,"invested":185305,"ltp":169,"current":97118,"pnl":-88187,"pnl_pct":-48,"frame":"Satellite","action":"OVERRIDE","signal":"Infra/Make-in-India mixed","tech":"Downtrend (confirmed)","note":"Deep loss but listed for turnaround monitoring."},
    {"symbol":"DENISCHEM-X","sector":"HEALTHCARE","qty":1000,"lt":800,"st":200,"avg":122.89,"invested":122887,"ltp":71,"current":70700,"pnl":-52187,"pnl_pct":-42,"frame":"Satellite","action":"WATCH","signal":"Company-specific","tech":"Downtrend","note":"Steep loss, small weight."},
    {"symbol":"DIXON","sector":"ENGINEERING & CAPITAL GOODS","qty":15,"lt":0,"st":15,"avg":11891.33,"invested":178370,"ltp":14250,"current":213750,"pnl":35380,"pnl_pct":20,"frame":"Satellite","action":"HOLD","signal":"EMS / Make-in-India","tech":"Uptrend","note":"Best performer in Engg sector."},
    {"symbol":"DLINKINDIA","sector":"SOFTWARE SERVICES","qty":225,"lt":0,"st":225,"avg":476.99,"invested":107324,"ltp":451,"current":101509,"pnl":-5815,"pnl_pct":-5,"frame":"Satellite","action":"HOLD","signal":"IT sector headwind","tech":"Range-bound","note":"Mild loss."},
    {"symbol":"DMART","sector":"RETAIL","qty":60,"lt":0,"st":60,"avg":4322.80,"invested":259368,"ltp":3770,"current":226200,"pnl":-33168,"pnl_pct":-13,"frame":"Satellite","action":"HOLD","signal":"Domestic consumption","tech":"Range-bound","note":"Revenue +14.9%, SSSG non-metro strong."},
    {"symbol":"EMIL","sector":"RETAIL","qty":2000,"lt":1400,"st":600,"avg":140.67,"invested":281337,"ltp":174,"current":348400,"pnl":67063,"pnl_pct":24,"frame":"CORE","action":"HOLD (reconsider)","signal":"Weak support (momentum only)","tech":"Uptrend","note":"PAT +458%, SSSG +34.2%. Thin-margin retail; strongest % gainer."},
    {"symbol":"FINOPB","sector":"FINANCIAL SERVICES","qty":950,"lt":550,"st":400,"avg":271.73,"invested":258147,"ltp":139,"current":132364,"pnl":-125783,"pnl_pct":-49,"frame":"Satellite","action":"OVERRIDE","signal":"Sector de-rating","tech":"Downtrend (confirmed)","note":"Near-halved. Temporary B2B UPI recalibration cited."},
    {"symbol":"GENUSPOWER","sector":"ENGINEERING & CAPITAL GOODS","qty":509,"lt":175,"st":334,"avg":283.51,"invested":144306,"ltp":338,"current":171940,"pnl":27635,"pnl_pct":19,"frame":"Satellite","action":"HOLD","signal":"Infra/Make-in-India","tech":"Uptrend","note":"Second-best in Engg."},
    {"symbol":"GPPL","sector":"LOGISTICS","qty":1250,"lt":0,"st":1250,"avg":167.85,"invested":209816,"ltp":162,"current":202025,"pnl":-7791,"pnl_pct":-4,"frame":"Satellite","action":"HOLD","signal":"Trade/domestic demand","tech":"Range-bound","note":"Standalone PAT +46.7%."},
    {"symbol":"GREENPLY","sector":"BUILDING MATERIALS","qty":1250,"lt":500,"st":750,"avg":277.41,"invested":346756,"ltp":305,"current":381563,"pnl":34806,"pnl_pct":10,"frame":"CORE","action":"HOLD","signal":"Growth, leveraged & rich","tech":"Uptrend","note":"Capacity expansion, rising debt & rich P/E."},
    {"symbol":"GREENPOWER","sector":"ENERGY","qty":10100,"lt":9100,"st":1000,"avg":16.56,"invested":167214,"ltp":9,"current":93728,"pnl":-73486,"pnl_pct":-44,"frame":"Satellite","action":"EXIT","signal":"Weak wind, 100% promoter pledge","tech":"Downtrend","note":"EXIT: governance + cyclical drag. Liquidate 10,100 shares."},
    {"symbol":"GRSE","sector":"DEFENCE","qty":110,"lt":82,"st":28,"avg":2685.00,"invested":295350,"ltp":2533,"current":278652,"pnl":-16698,"pnl_pct":-6,"frame":"Satellite","action":"HOLD","signal":"Structural defence capex","tech":"Range-bound","note":"Navratna, PAT +43.8%."},
    {"symbol":"GSFC","sector":"FERTILIZERS","qty":1300,"lt":400,"st":900,"avg":187.60,"invested":243879,"ltp":163,"current":211744,"pnl":-32135,"pnl_pct":-13,"frame":"Satellite","action":"HOLD","signal":"Policy/subsidy-linked","tech":"Range-bound","note":""},
    {"symbol":"HAL","sector":"DEFENCE","qty":61,"lt":34,"st":27,"avg":4430.88,"invested":270284,"ltp":4856,"current":296216,"pnl":25932,"pnl_pct":10,"frame":"CORE","action":"HOLD","signal":"Strong (huge order book)","tech":"Uptrend","note":"₹2.54 Lakh Cr order book, monopoly position."},
    {"symbol":"HDFCBANK","sector":"FINANCIAL SERVICES","qty":230,"lt":0,"st":230,"avg":748.67,"invested":172194,"ltp":713,"current":164025,"pnl":-8170,"pnl_pct":-5,"frame":"CORE","action":"HOLD","signal":"Stabilizer, not growth engine","tech":"Range-bound","note":"Low-volatility core anchor."},
    {"symbol":"HINDZINC","sector":"METALS","qty":450,"lt":0,"st":450,"avg":606.43,"invested":272894,"ltp":601,"current":270450,"pnl":-2444,"pnl_pct":-1,"frame":"Satellite","action":"HOLD","signal":"Commodity-cycle, peak profitability","tech":"Range-bound","note":"Record profit, silver contribution high, lowest mining costs."},
    {"symbol":"HITECH","sector":"BUILDING MATERIALS","qty":2650,"lt":1600,"st":1050,"avg":102.13,"invested":270638,"ltp":76,"current":200817,"pnl":-69821,"pnl_pct":-26,"frame":"Satellite","action":"WATCH","signal":"Domestic demand mixed","tech":"Downtrend/stabilizing","note":"Outlier dragging Building Materials."},
    {"symbol":"INA","sector":"ENGINEERING & CAPITAL GOODS","qty":1923,"lt":0,"st":1923,"avg":126.46,"invested":243190,"ltp":90,"current":173608,"pnl":-69582,"pnl_pct":-29,"frame":"Satellite","action":"WATCH","signal":"Infra mixed quality","tech":"Downtrend/stabilizing","note":"Fully short-term."},
    {"symbol":"INOXWIND","sector":"ENGINEERING & CAPITAL GOODS","qty":600,"lt":0,"st":600,"avg":81.13,"invested":48675,"ltp":75,"current":44814,"pnl":-3861,"pnl_pct":-8,"frame":"Satellite","action":"HOLD","signal":"Renewable equipment","tech":"Range-bound","note":"Small position."},
    {"symbol":"IREDA","sector":"FINANCIAL SERVICES","qty":9000,"lt":3125,"st":5875,"avg":147.86,"invested":1330710,"ltp":114,"current":1022760,"pnl":-307950,"pnl_pct":-23,"frame":"CORE","action":"OVERRIDE","signal":"Improving (profit +37%, NPA better)","tech":"Stabilizing (mixed)","note":"Largest position. Business executing well; stock hit by PSU NBFC de-rating & FII flows. Near 52W low."},
    {"symbol":"IRFC","sector":"FINANCIAL SERVICES","qty":2000,"lt":850,"st":1150,"avg":117.70,"invested":235408,"ltp":84,"current":167200,"pnl":-68208,"pnl_pct":-29,"frame":"Satellite","action":"HOLD","signal":"Sector de-rating","tech":"Downtrend/stabilizing","note":""},
    {"symbol":"JAYSREETEA","sector":"FMCG","qty":550,"lt":400,"st":150,"avg":118.84,"invested":65363,"ltp":99,"current":54500,"pnl":-10863,"pnl_pct":-17,"frame":"Satellite","action":"EXIT","signal":"Stagnant agri commodity","tech":"Downtrend","note":"EXIT: low capital velocity. Liquidate 550 shares."},
    {"symbol":"JIOFIN","sector":"FINANCIAL SERVICES","qty":1275,"lt":850,"st":425,"avg":286.79,"invested":365652,"ltp":240,"current":305809,"pnl":-59843,"pnl_pct":-16,"frame":"CORE","action":"HOLD","signal":"Strong & accelerating (+156% profit)","tech":"Downtrend/stabilizing","note":"Q1 FY27 PAT +156% to ₹830 Cr. One of the better fundamental stories."},
    {"symbol":"JSWENERGY","sector":"ENERGY","qty":350,"lt":250,"st":100,"avg":513.02,"invested":179557,"ltp":540,"current":188948,"pnl":9390,"pnl_pct":5,"frame":"Satellite","action":"HOLD","signal":"Capacity surge +1,081 MW","tech":"Uptrend","note":"Overrule stop-loss per Batch 1."},
    {"symbol":"KAYNES","sector":"ENGINEERING & CAPITAL GOODS","qty":15,"lt":0,"st":15,"avg":3173.33,"invested":47600,"ltp":3598,"current":53970,"pnl":6370,"pnl_pct":13,"frame":"Satellite","action":"HOLD","signal":"EMS / Make-in-India","tech":"Uptrend","note":"Tiny weight."},
    {"symbol":"KIRIINDUS","sector":"CHEMICALS","qty":450,"lt":0,"st":450,"avg":603.39,"invested":271526,"ltp":559,"current":251618,"pnl":-19908,"pnl_pct":-7,"frame":"Satellite","action":"HOLD","signal":"Turnaround profit but other-income heavy","tech":"Range-bound","note":"Quality-of-earnings flag: almost all profit from treasury/interest."},
    {"symbol":"KNRCON","sector":"ENGINEERING & CAPITAL GOODS","qty":1300,"lt":750,"st":550,"avg":202.18,"invested":262833,"ltp":125,"current":162240,"pnl":-100593,"pnl_pct":-38,"frame":"Satellite","action":"WATCH","signal":"Infra mixed quality","tech":"Downtrend (confirmed)","note":""},
    {"symbol":"KPIGREEN","sector":"ENGINEERING & CAPITAL GOODS","qty":600,"lt":250,"st":350,"avg":438.89,"invested":263332,"ltp":307,"current":184200,"pnl":-79132,"pnl_pct":-30,"frame":"Satellite","action":"OVERRIDE","signal":"Renewable / infra mixed","tech":"Downtrend (confirmed)","note":"Turnaround list."},
    {"symbol":"KPITTECH","sector":"SOFTWARE SERVICES","qty":570,"lt":80,"st":490,"avg":832.29,"invested":474404,"ltp":576,"current":328320,"pnl":-146084,"pnl_pct":-31,"frame":"Satellite","action":"OVERRIDE","signal":"Sector headwind (IT)","tech":"Downtrend (confirmed)","note":"Relative outperformer vs large IT; auto-tech/ER&D better positioned."},
    {"symbol":"MAHSEAMLES","sector":"BUILDING MATERIALS","qty":510,"lt":210,"st":300,"avg":619.34,"invested":315864,"ltp":688,"current":350957,"pnl":35092,"pnl_pct":11,"frame":"CORE","action":"HOLD (watch next Q)","signal":"Strong history, recent wobble","tech":"Uptrend","note":"Almost debt-free historically; recent quarter profit fell sharply."},
    {"symbol":"MCX","sector":"FINANCIAL SERVICES","qty":31,"lt":0,"st":31,"avg":2773.82,"invested":85988,"ltp":3275,"current":101537,"pnl":15549,"pnl_pct":18,"frame":"Satellite","action":"HOLD","signal":"Exchange play","tech":"Uptrend","note":"Lone winner in Financial Services."},
    {"symbol":"MOSCHIP","sector":"ENGINEERING & CAPITAL GOODS","qty":1150,"lt":900,"st":250,"avg":228.13,"invested":262347,"ltp":212,"current":244203,"pnl":-18145,"pnl_pct":-7,"frame":"Satellite","action":"HOLD","signal":"Infra mixed","tech":"Range-bound","note":""},
    {"symbol":"NPST","sector":"SOFTWARE SERVICES","qty":201,"lt":5,"st":196,"avg":1499.90,"invested":301480,"ltp":1721,"current":345981,"pnl":44501,"pnl_pct":15,"frame":"CORE","action":"HOLD","signal":"Domestic fintech infra","tech":"Uptrend","note":"Less exposed to US IT headwinds."},
    {"symbol":"NTPCGREEN","sector":"ENERGY","qty":3500,"lt":750,"st":2750,"avg":101.55,"invested":355440,"ltp":89,"current":312865,"pnl":-42575,"pnl_pct":-12,"frame":"Satellite","action":"OVERRIDE","signal":"Renewable policy, execution risk","tech":"Range-bound","note":"Net profit +38%, high EBITDA margin. Capacity additions."},
    {"symbol":"PCBL","sector":"CHEMICALS","qty":1400,"lt":225,"st":1175,"avg":321.38,"invested":449935,"ltp":317,"current":444010,"pnl":-5925,"pnl_pct":-1,"frame":"Satellite","action":"HOLD","signal":"Specialty black growth","tech":"Range-bound","note":"PAT +65%, specialty volumes +23%."},
    {"symbol":"PFC","sector":"FINANCIAL SERVICES","qty":350,"lt":0,"st":350,"avg":380.92,"invested":133321,"ltp":356,"current":124548,"pnl":-8774,"pnl_pct":-7,"frame":"Satellite","action":"HOLD","signal":"Sector de-rating","tech":"Range-bound","note":""},
    {"symbol":"PROTEAN","sector":"SOFTWARE SERVICES","qty":200,"lt":20,"st":180,"avg":720.45,"invested":144090,"ltp":497,"current":99470,"pnl":-44620,"pnl_pct":-31,"frame":"Satellite","action":"WATCH","signal":"IT headwind","tech":"Downtrend","note":""},
    {"symbol":"RAILTEL","sector":"ENGINEERING & CAPITAL GOODS","qty":550,"lt":375,"st":175,"avg":395.58,"invested":217568,"ltp":271,"current":149133,"pnl":-68436,"pnl_pct":-31,"frame":"Satellite","action":"WATCH","signal":"Infra mixed","tech":"Downtrend (confirmed)","note":""},
    {"symbol":"RELIANCE","sector":"ENERGY","qty":125,"lt":0,"st":125,"avg":1327.34,"invested":165917,"ltp":1322,"current":165250,"pnl":-667,"pnl_pct":0,"frame":"Satellite","action":"HOLD","signal":"O2C strength","tech":"Range-bound","note":"MOFSL Buy cited earlier."},
    {"symbol":"ROUTE","sector":"SOFTWARE SERVICES","qty":600,"lt":300,"st":300,"avg":864.14,"invested":518484,"ltp":502,"current":300930,"pnl":-217554,"pnl_pct":-42,"frame":"Satellite","action":"OVERRIDE","signal":"Recovering (CPaaS)","tech":"Stabilizing","note":"Q1 FY27 revenue +9.6% YoY. Margins expected to recover H2. Security incident resolved."},
    {"symbol":"SIYARAM-M","sector":"METALS","qty":7500,"lt":1500,"st":6000,"avg":79.91,"invested":599325,"ltp":35,"current":264900,"pnl":-334425,"pnl_pct":-56,"frame":"Satellite","action":"EXIT","signal":"High caution (micro-cap recycling)","tech":"Downtrend (extreme, thin liquidity)","note":"NOT Siyaram Silk. Micro-cap, thin volumes, profit −74%. Highest-risk holding. EXIT."},
    {"symbol":"TATASTEEL","sector":"METALS","qty":1000,"lt":0,"st":1000,"avg":196.55,"invested":196549,"ltp":189,"current":189000,"pnl":-7549,"pnl_pct":-4,"frame":"Satellite","action":"HOLD","signal":"India ROCE 27%","tech":"Range-bound","note":"Approved large expansion."},
    {"symbol":"TEXRAIL","sector":"ENGINEERING & CAPITAL GOODS","qty":1350,"lt":800,"st":550,"avg":151.47,"invested":204480,"ltp":116,"current":156587,"pnl":-47894,"pnl_pct":-23,"frame":"Satellite","action":"WATCH","signal":"Infra mixed","tech":"Downtrend/stabilizing","note":""},
    {"symbol":"VISAKAIND","sector":"BUILDING MATERIALS","qty":2100,"lt":1675,"st":425,"avg":100.51,"invested":211079,"ltp":93,"current":196077,"pnl":-15002,"pnl_pct":-7,"frame":"Satellite","action":"HOLD","signal":"Domestic demand mixed","tech":"Range-bound","note":""},
    {"symbol":"WAAREEENER","sector":"ENGINEERING & CAPITAL GOODS","qty":50,"lt":0,"st":50,"avg":2937.56,"invested":146878,"ltp":2636,"current":131800,"pnl":-15078,"pnl_pct":-10,"frame":"Satellite","action":"HOLD","signal":"Renewable equipment","tech":"Range-bound","note":""},
    {"symbol":"ZAGGLE","sector":"FINANCIAL SERVICES","qty":1200,"lt":300,"st":900,"avg":306.51,"invested":367811,"ltp":181,"current":217080,"pnl":-150731,"pnl_pct":-41,"frame":"Satellite","action":"OVERRIDE","signal":"Weakening (DICE integration costs)","tech":"Downtrend (confirmed)","note":"Revenue +27.5%, PAT dip from one-time M&A. FY27 guidance 40% growth."},
]


df = pd.DataFrame(HOLDINGS)
df["weight"] = (df["invested"] / df["invested"].sum() * 100).round(2)

# ───────────────────────────── LIVE DATA HELPERS ─────────────────────────────
# Yahoo Finance tickers for NSE stocks (most use .NS)
TICKER_MAP = {
    "AGI": "AGI.NS", "BAJAJHFL": "BAJAJHFL.NS", "BBOX": "BBOX.NS", "BDL": "BDL.NS",
    "BECTORFOOD": "BECTORFOOD.NS", "DATAPATTNS": "DATAPATTNS.NS", "DCXINDIA": "DCXINDIA.NS",
    "DENISCHEM-X": "DENISCHEM.NS", "DIXON": "DIXON.NS", "DLINKINDIA": "DLINKINDIA.NS",
    "DMART": "DMART.NS", "EMIL": "EMIL.NS", "FINOPB": "FINOPB.NS", "GENUSPOWER": "GENUSPOWER.NS",
    "GPPL": "GPPL.NS", "GREENPLY": "GREENPLY.NS", "GREENPOWER": "GREENPOWER.NS", "GRSE": "GRSE.NS",
    "GSFC": "GSFC.NS", "HAL": "HAL.NS", "HDFCBANK": "HDFCBANK.NS", "HINDZINC": "HINDZINC.NS",
    "HITECH": "HITECH.NS", "INA": "INA.NS", "INOXWIND": "INOXWIND.NS", "IREDA": "IREDA.NS",
    "IRFC": "IRFC.NS", "JAYSREETEA": "JAYSREETEA.NS", "JIOFIN": "JIOFIN.NS", "JSWENERGY": "JSWENERGY.NS",
    "KAYNES": "KAYNES.NS", "KIRIINDUS": "KIRIINDUS.NS", "KNRCON": "KNRCON.NS", "KPIGREEN": "KPIGREEN.NS",
    "KPITTECH": "KPITTECH.NS", "MAHSEAMLES": "MAHSEAMLES.NS", "MCX": "MCX.NS", "MOSCHIP": "MOSCHIP.NS",
    "NPST": "NPST.NS", "NTPCGREEN": "NTPCGREEN.NS", "PCBL": "PCBL.NS", "PFC": "PFC.NS",
    "PROTEAN": "PROTEAN.NS", "RAILTEL": "RAILTEL.NS", "RELIANCE": "RELIANCE.NS", "ROUTE": "ROUTE.NS",
    "SIYARAM-M": "SIYARAM.NS", "TATASTEEL": "TATASTEEL.NS", "TEXRAIL": "TEXRAIL.NS",
    "VISAKAIND": "VISAKAIND.NS", "WAAREEENER": "WAAREEENER.NS", "ZAGGLE": "ZAGGLE.NS",
}

@st.cache_data(ttl=300, show_spinner=False)
def get_live_price(symbol: str):
    """Fetch latest price from Yahoo Finance. Returns dict or None."""
    ticker = TICKER_MAP.get(symbol)
    if not ticker:
        return None
    try:
        t = yf.Ticker(ticker)
        info = t.fast_info
        price = getattr(info, "last_price", None) or getattr(info, "lastPrice", None)
        if price is None:
            hist = t.history(period="5d")
            if hist is not None and not hist.empty:
                price = float(hist["Close"].iloc[-1])
        if price is None:
            return None
        prev = getattr(info, "previous_close", None) or getattr(info, "previousClose", None)
        return {
            "price": float(price),
            "prev_close": float(prev) if prev else None,
            "ticker": ticker,
        }
    except Exception:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def get_history(symbol: str, period: str = "1y"):
    """Historical OHLCV for charting."""
    ticker = TICKER_MAP.get(symbol)
    if not ticker:
        return None
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period)
        if hist is None or hist.empty:
            return None
        hist = hist.reset_index()
        hist["Date"] = pd.to_datetime(hist["Date"]).dt.tz_localize(None)
        return hist
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def get_batch_live_prices(symbols: tuple):
    """Fetch multiple live prices. symbols must be tuple for cache hash."""
    results = {}
    for sym in symbols:
        results[sym] = get_live_price(sym)
    return results


# ───────────────────────────── SIDEBAR ─────────────────────────────
st.sidebar.title("📊 Portfolio Analyser")
st.sidebar.caption("Data: 4-Sep-2026 holdings + public research")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "📋 All Holdings",
        "📈 Technical Analysis",
        "📄 Stock Report",
        "⚡ Actions & Recs",
        "🏭 Sectors",
        "🔄 Rebalance Framework",
        "ℹ️ About & Disclaimer",
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("Free to run online via Streamlit Community Cloud. Not investment advice.")

# ───────────────────────────── HELPERS ─────────────────────────────
def fmt_inr(n):
    n = float(n)
    if abs(n) >= 1e7:
        return f"₹{n/1e7:.2f} Cr"
    if abs(n) >= 1e5:
        return f"₹{n/1e5:.2f} L"
    return f"₹{n:,.0f}"

def color_pnl(val):
    color = "green" if val >= 0 else "red"
    return f"color: {color}"

# ───────────────────────────── PAGES ─────────────────────────────
if page == "🏠 Dashboard":
    st.title("Portfolio Snapshot")
    st.caption(f"As of 4-Sep-2026 · Generated {datetime.now().strftime('%d %b %Y %H:%M')}")

    total_inv = df["invested"].sum()
    total_cur = df["current"].sum()
    total_pnl = total_cur - total_inv
    total_pnl_pct = total_pnl / total_inv * 100

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Invested", fmt_inr(total_inv))
    c2.metric("Current Value", fmt_inr(total_cur))
    c3.metric("Unrealized P&L", fmt_inr(total_pnl), f"{total_pnl_pct:.1f}%")
    c4.metric("Holdings", f"{len(df)}", f"{(df.pnl > 0).sum()} in profit")

    st.markdown("---")
    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.subheader("Sector Allocation (Current Value)")
        sec = df.groupby("sector")["current"].sum().reset_index().sort_values("current", ascending=False)
        fig = px.pie(sec, values="current", names="sector", hole=0.45,
                     color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=380, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Top 5 Gainers (₹)")
        top_g = df.nlargest(5, "pnl")[["symbol", "pnl", "pnl_pct", "current"]]
        st.dataframe(
            top_g.style.format({"pnl": "₹{:,.0f}", "pnl_pct": "{:+.0f}%", "current": "₹{:,.0f}"}),
            use_container_width=True, hide_index=True
        )
        st.subheader("Top 5 Losers (₹)")
        top_l = df.nsmallest(5, "pnl")[["symbol", "pnl", "pnl_pct", "current"]]
        st.dataframe(
            top_l.style.format({"pnl": "₹{:,.0f}", "pnl_pct": "{:+.0f}%", "current": "₹{:,.0f}"}),
            use_container_width=True, hide_index=True
        )

    st.markdown("---")
    st.subheader("Quick Research Summary")
    st.markdown("""
    **Macro**: Nifty ~9% off highs. Prolonged FII selling (especially mid/small-caps). Domestic growth healthy.  
    **Largest drag**: IREDA (business improving, stock de-rated), SIYARAM-M (micro-cap risk), ROUTE & ZAGGLE (recovering/integration).  
    **Strongest fundamentals**: JIOFIN, BBOX, HAL, BDL (order books), HINDZINC.  
    **Clear exits**: GREENPOWER, JAYSREETEA, SIYARAM-M → free ≈ ₹4.08 Lakh for redeployment.
    """)

    st.markdown("---")
    st.subheader("Live Prices – Top Holdings (Yahoo Finance)")
    st.caption("Click the button to fetch current market prices (cached 5 min). Delayed quotes.")
    if st.button("🔄 Fetch live prices for top 10 holdings", type="primary"):
        top10 = df.nlargest(10, "invested")["symbol"].tolist()
        with st.spinner("Fetching from Yahoo Finance..."):
            prices = get_batch_live_prices(tuple(top10))
        rows = []
        for sym in top10:
            r = df[df.symbol == sym].iloc[0]
            live = prices.get(sym)
            if live and live.get("price"):
                live_px = live["price"]
                live_val = live_px * r.qty
                live_pnl = live_val - r.invested
                live_pct = live_pnl / r.invested * 100
                rows.append({
                    "Symbol": sym,
                    "Book LTP": r.ltp,
                    "Live Price": round(live_px, 2),
                    "Change vs Book": round(live_px - r.ltp, 2),
                    "Live Value": round(live_val),
                    "Live P&L %": round(live_pct, 1),
                })
            else:
                rows.append({
                    "Symbol": sym,
                    "Book LTP": r.ltp,
                    "Live Price": "N/A",
                    "Change vs Book": "—",
                    "Live Value": "—",
                    "Live P&L %": "—",
                })
        live_df = pd.DataFrame(rows)
        st.dataframe(live_df, use_container_width=True, hide_index=True)
        st.caption("Data from Yahoo Finance. Some micro-caps or recently listed names may return N/A.")

elif page == "📋 All Holdings":
    st.title("All 52 Holdings")
    st.caption("Invested · Average · Book LTP · Optional Live Price. Search / filter / sort.")

    colf1, colf2, colf3, colf4 = st.columns(4)
    with colf1:
        search = st.text_input("Search symbol / sector", "")
    with colf2:
        sec_filter = st.multiselect("Sector", sorted(df.sector.unique()))
    with colf3:
        frame_filter = st.multiselect("Framework", ["CORE", "Satellite"])
    with colf4:
        action_filter = st.multiselect("Action", sorted(df.action.unique()))

    fetch_live = st.checkbox("Fetch live prices (Yahoo, slower)", value=False)

    view = df.copy()
    if search:
        q = search.lower()
        view = view[view.symbol.str.lower().str.contains(q) | view.sector.str.lower().str.contains(q)]
    if sec_filter:
        view = view[view.sector.isin(sec_filter)]
    if frame_filter:
        view = view[view.frame.isin(frame_filter)]
    if action_filter:
        view = view[view.action.isin(action_filter)]

    view = view.sort_values("invested", ascending=False)

    if fetch_live and len(view) > 0:
        with st.spinner(f"Fetching live prices for {len(view)} stocks..."):
            live_map = get_batch_live_prices(tuple(view.symbol.tolist()))
        live_prices, live_vals, live_pnls, live_pcts = [], [], [], []
        for _, row in view.iterrows():
            lp = live_map.get(row.symbol)
            if lp and lp.get("price"):
                px = lp["price"]
                val = px * row.qty
                pnl = val - row.invested
                pct = pnl / row.invested * 100
                live_prices.append(round(px, 2))
                live_vals.append(round(val))
                live_pnls.append(round(pnl))
                live_pcts.append(round(pct, 1))
            else:
                live_prices.append(None)
                live_vals.append(None)
                live_pnls.append(None)
                live_pcts.append(None)
        view = view.copy()
        view["live_price"] = live_prices
        view["live_value"] = live_vals
        view["live_pnl"] = live_pnls
        view["live_pnl_pct"] = live_pcts
        display_cols = ["symbol", "sector", "invested", "avg", "ltp", "live_price", "current", "live_value", "pnl", "live_pnl", "pnl_pct", "live_pnl_pct", "frame", "action"]
        format_dict = {
            "invested": "₹{:,.0f}", "avg": "₹{:.2f}", "ltp": "₹{:.2f}",
            "live_price": "₹{:.2f}", "current": "₹{:,.0f}", "live_value": "₹{:,.0f}",
            "pnl": "₹{:,.0f}", "live_pnl": "₹{:,.0f}",
            "pnl_pct": "{:+.0f}%", "live_pnl_pct": "{:+.1f}%",
        }
    else:
        display_cols = ["symbol", "sector", "weight", "invested", "avg", "ltp", "current", "pnl", "pnl_pct", "frame", "action", "signal"]
        format_dict = {
            "weight": "{:.2f}%", "invested": "₹{:,.0f}", "avg": "₹{:.2f}", "ltp": "₹{:.2f}",
            "current": "₹{:,.0f}", "pnl": "₹{:,.0f}", "pnl_pct": "{:+.0f}%",
        }

    def color_pnl_style(v):
        if isinstance(v, (int, float)):
            if v > 0: return "color: green"
            if v < 0: return "color: red"
        return ""

    subset_cols = [c for c in ["pnl", "pnl_pct", "live_pnl", "live_pnl_pct"] if c in view.columns]
    styled = view[display_cols].style.format(format_dict, na_rep="—")
    if subset_cols:
        styled = styled.map(color_pnl_style, subset=subset_cols)

    st.dataframe(styled, use_container_width=True, height=620, hide_index=True)
    st.caption(f"Showing {len(view)} of {len(df)} holdings · Book data as of 4-Sep-2026 · Live via Yahoo Finance when enabled")


elif page == "📈 Technical Analysis":
    st.title("Technical Analysis")
    st.caption("Simple indicators from Yahoo Finance history. Educational only.")

    scope = st.radio("Analyse", ["Selected stock", "Top 10 by invested"], horizontal=True)
    period = st.selectbox("History period", ["3mo", "6mo", "1y", "2y"], index=2)

    def compute_ta(hist):
        if hist is None or len(hist) < 30:
            return None
        close = hist["Close"]
        sma20 = close.rolling(20).mean().iloc[-1]
        sma50 = close.rolling(50).mean().iloc[-1] if len(close) >= 50 else None
        last = float(close.iloc[-1])
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss.replace(0, 1e-9)
        rsi = 100 - (100 / (1 + rs))
        rsi_last = float(rsi.iloc[-1]) if not rsi.empty else None
        if sma50 is not None and last > float(sma50):
            trend = "Uptrend bias"
        elif sma50 is not None and last < float(sma50):
            trend = "Downtrend bias"
        else:
            trend = "Range / mixed"
        return {
            "last": last,
            "sma20": float(sma20) if sma20 == sma20 else None,
            "sma50": float(sma50) if sma50 is not None and sma50 == sma50 else None,
            "rsi": rsi_last,
            "trend": trend,
            "ret_period": float(close.iloc[-1] / close.iloc[0] - 1) * 100,
        }

    if scope == "Selected stock":
        sym = st.selectbox("Stock", sorted(df.symbol.unique()), key="ta_sym")
        hist = get_history(sym, period)
        ta = compute_ta(hist)
        r = df[df.symbol == sym].iloc[0]
        if ta:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Last Close", f"₹{ta['last']:,.2f}")
            c2.metric("RSI (14)", f"{ta['rsi']:.1f}" if ta['rsi'] else "—")
            c3.metric("Period Return", f"{ta['ret_period']:+.1f}%")
            c4.metric("Trend proxy", ta["trend"])
            sma20s = f"{ta['sma20']:.1f}" if ta.get('sma20') else "—"
            sma50s = f"{ta['sma50']:.1f}" if ta.get('sma50') else "—"
            st.write(f"SMA20: {sma20s} | SMA50: {sma50s} | Your Avg: ₹{r.avg}")
            if hist is not None:
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist["Date"], y=hist["Close"], name="Close", line=dict(color="#38bdf8")))
                if len(hist) >= 20:
                    fig.add_trace(go.Scatter(x=hist["Date"], y=hist["Close"].rolling(20).mean(), name="SMA20", line=dict(color="#f59e0b", width=1)))
                if len(hist) >= 50:
                    fig.add_trace(go.Scatter(x=hist["Date"], y=hist["Close"].rolling(50).mean(), name="SMA50", line=dict(color="#a78bfa", width=1)))
                fig.add_hline(y=r.avg, line_dash="dash", line_color="#22c55e", annotation_text="Your Avg")
                fig.update_layout(height=400, hovermode="x unified", template="plotly_white", margin=dict(t=20, b=20))
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Not enough history for indicators.")
    else:
        top = df.nlargest(10, "invested")
        rows = []
        progress = st.progress(0)
        for i, (_, row) in enumerate(top.iterrows()):
            hist = get_history(row.symbol, period)
            ta = compute_ta(hist)
            if ta:
                rows.append({"Symbol": row.symbol, "Last": round(ta["last"], 2), "RSI": round(ta["rsi"], 1) if ta["rsi"] else None,
                             "Trend": ta["trend"], "Period %": round(ta["ret_period"], 1), "Your Avg": row.avg})
            else:
                rows.append({"Symbol": row.symbol, "Last": None, "RSI": None, "Trend": "N/A", "Period %": None, "Your Avg": row.avg})
            progress.progress((i + 1) / len(top))
        progress.empty()
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

elif page == "📄 Stock Report":
    st.title("Detailed Stock Report")
    st.caption("Book data + live price + technicals + research notes + limited Yahoo fundamentals.")

    sym = st.selectbox("Select stock for full report", sorted(df.symbol.unique()), key="report_sym")
    r = df[df.symbol == sym].iloc[0]

    st.header(f"{sym} — Full Report")
    st.write(f"**Sector**: {r.sector} · **Framework**: {r.frame} · **Action**: {r.action}")

    st.subheader("1. Position & Prices")
    live = get_live_price(sym)
    cols = st.columns(5)
    cols[0].metric("Invested", fmt_inr(r.invested))
    cols[1].metric("Avg Cost", f"₹{r.avg}")
    cols[2].metric("Book LTP", f"₹{r.ltp}")
    if live and live.get("price"):
        lp = live["price"]
        cols[3].metric("Live Price", f"₹{lp:,.2f}", f"{lp - r.ltp:+.2f}")
        live_pnl = lp * r.qty - r.invested
        cols[4].metric("Live P&L", fmt_inr(live_pnl), f"{(live_pnl/r.invested)*100:+.1f}%")
    else:
        cols[3].metric("Live Price", "N/A")
        cols[4].metric("Live P&L", "—")
    st.write(f"Qty: **{r.qty}** (LT {r.lt} / ST {r.st}) · Book value: {fmt_inr(r.current)}")

    st.subheader("2. Historical Trend & Technicals")
    period = st.selectbox("Chart period", ["3mo", "6mo", "1y", "2y"], index=2, key="rep_period")
    hist = get_history(sym, period)
    if hist is not None and not hist.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist["Date"], y=hist["Close"], name="Close", line=dict(color="#38bdf8", width=2)))
        if len(hist) >= 20:
            fig.add_trace(go.Scatter(x=hist["Date"], y=hist["Close"].rolling(20).mean(), name="SMA20", line=dict(width=1, color="#f59e0b")))
        if len(hist) >= 50:
            fig.add_trace(go.Scatter(x=hist["Date"], y=hist["Close"].rolling(50).mean(), name="SMA50", line=dict(width=1, color="#a78bfa")))
        fig.add_hline(y=r.avg, line_dash="dash", line_color="#22c55e", annotation_text=f"Avg ₹{r.avg}")
        fig.update_layout(height=360, template="plotly_white", hovermode="x unified", margin=dict(t=10, b=20))
        st.plotly_chart(fig, use_container_width=True)
        close = hist["Close"]
        ret = (close.iloc[-1] / close.iloc[0] - 1) * 100
        st.write(f"Period return: **{ret:+.1f}%** · High ₹{hist['High'].max():,.1f} · Low ₹{hist['Low'].min():,.1f}")
    else:
        st.info("Historical data unavailable.")

    st.subheader("3. Business Signal & Research")
    st.markdown(f"""
| Field | Detail |
|-------|--------|
| Business signal | {r.signal} |
| Technical signal | {r.tech} |
| Action tag | **{r.action}** |
""")
    st.write(r.note or "No additional note.")

    research = {
        "IREDA": "Business executing well; near 52W low mainly on PSU NBFC de-rating + FII flows. Govt promoter.",
        "SIYARAM-M": "Micro-cap recycling (not textile). FY26 profit -74%. Highest risk. Promoter-dominated.",
        "ROUTE": "Q1 FY27 revenue +9.6% YoY. Stabilising after soft FY26. Competitive CPaaS.",
        "BDL": "Order book ~₹26,000 Cr + HAL order. Valuation correction. Govt PSU.",
        "JIOFIN": "Q1 FY27 PAT +156%. Strong AUM growth. Reliance ecosystem promoter.",
        "ZAGGLE": "Revenue growing; PAT hit by DICE costs. 40% FY27 guidance reiterated.",
        "BBOX": "High ROE, AI/data-centre backlog expansion. Quality growth.",
        "HAL": "Huge order book, monopoly platforms. Govt promoter.",
        "KPITTECH": "IT headwind; relative resilience via auto-tech.",
        "GREENPOWER": "Weak seasonality + 100% promoter pledge. Exit candidate.",
        "HDFCBANK": "Stabilizer. Large institutional ownership. Core long-term hold for many brokerages.",
        "HINDZINC": "Peak profitability, silver contribution high. Vedanta promoter. Commodity cycle.",
        "EMIL": "Strong SSSG; thin-margin retail. Momentum strong, margin durability to watch.",
    }
    st.write("**Research snapshot:**", research.get(sym, "No extended note in embedded set."))

    st.subheader("4. Yahoo Finance quick fundamentals (limited for India)")
    try:
        ticker = TICKER_MAP.get(sym)
        if ticker:
            info = yf.Ticker(ticker).info
            keys = ["longName", "marketCap", "trailingPE", "forwardPE", "priceToBook",
                    "profitMargins", "revenueGrowth", "earningsGrowth", "returnOnEquity",
                    "debtToEquity", "recommendationKey", "targetMeanPrice", "numberOfAnalystOpinions"]
            fund = {k: info.get(k) for k in keys if info.get(k) is not None}
            if fund:
                st.json(fund)
            else:
                st.info("Limited fields returned.")
        else:
            st.info("No ticker mapped.")
    except Exception as e:
        st.warning(f"Yahoo info error: {e}")

    st.subheader("5. Promoter / MF / Analyst notes")
    st.markdown("""
Free automated feeds do **not** reliably give live Indian promoter %, HNI changes or full brokerage report text.
Use these authoritative sources for live data:
- **NSE** shareholding pattern pages
- **Screener.in** or **Trendlyne** (promoter, MF, FII % and quarterly changes)
- Broker terminals / Bloomberg for full analyst notes

Embedded research notes:
- PSU names (IREDA, BDL, HAL…): Promoter = Government of India
- JIOFIN: Reliance group promoter, institutional interest rising with scale
- SIYARAM-M: Promoter-dominated micro-cap, limited institutional ownership
- Brokerage colour from earlier research: BDL mixed (valuation/execution); KPIT relatively preferred in mid-cap IT; IREDA/JIOFIN viewed as growth + de-rating stories; HINDZINC as cash-flow quality
- Market-level: FII selling pressure on midcaps 2025-26; DIIs partial absorbers
""")
    st.caption("Educational report only. Not investment advice.")

elif page == "⚡ Actions & Recs":
    st.title("Actions & Recommendations")
    st.caption("Synthesised from Board presentation, Core-Satellite report and independent research")

    st.subheader("🔴 Recommended EXITS")
    exits = df[df.action == "EXIT"]
    for _, r in exits.iterrows():
        with st.expander(f"{r.symbol}  ·  {r.pnl_pct}%  ·  {fmt_inr(r.current)}"):
            st.write(f"**Sector**: {r.sector}")
            st.write(f"**Signal**: {r.signal}")
            st.write(f"**Note**: {r.note}")
            st.write(f"Qty: {r.qty} | Avg: ₹{r.avg} | LTP: ₹{r.ltp}")

    st.subheader("🟠 OVERRIDES (hold despite deep drawdown)")
    overs = df[df.action.str.contains("OVERRIDE", na=False)]
    for _, r in overs.iterrows():
        with st.expander(f"{r.symbol}  ·  {r.pnl_pct}%  ·  {fmt_inr(r.current)}"):
            st.write(f"**Sector**: {r.sector} | **Frame**: {r.frame}")
            st.write(f"**Signal**: {r.signal}")
            st.write(f"**Technical**: {r.tech}")
            st.write(f"**Note**: {r.note}")

    st.subheader("🟢 Core HOLD candidates")
    cores = df[df.frame == "CORE"]
    st.dataframe(
        cores[["symbol", "sector", "pnl_pct", "current", "signal", "action"]].style.format({
            "pnl_pct": "{:+.0f}%", "current": "₹{:,.0f}"
        }),
        use_container_width=True, hide_index=True
    )

    st.markdown("---")
    st.subheader("Cash from recommended exits")
    cash = exits["current"].sum()
    st.metric("Approx. capital freed", fmt_inr(cash), "GREENPOWER + JAYSREETEA + SIYARAM-M")
    st.info("Redeploy into high-conviction Core names (IREDA, JIOFIN, BBOX, HAL, BDL) or follow 65/35 Core+Satellite structure.")

elif page == "🏭 Sectors":
    st.title("Sector Deep Dive")
    sec_agg = df.groupby("sector").agg(
        holdings=("symbol", "count"),
        invested=("invested", "sum"),
        current=("current", "sum"),
        pnl=("pnl", "sum")
    ).reset_index()
    sec_agg["pnl_pct"] = (sec_agg.pnl / sec_agg.invested * 100).round(1)
    sec_agg["weight"] = (sec_agg.current / sec_agg.current.sum() * 100).round(1)
    sec_agg = sec_agg.sort_values("current", ascending=False)

    fig = px.bar(sec_agg, x="sector", y="pnl", color="pnl",
                 color_continuous_scale=["#ef4444", "#22c55e"],
                 title="Sector P&L (₹)")
    fig.update_layout(xaxis_tickangle=-45, height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        sec_agg.style.format({
            "invested": "₹{:,.0f}", "current": "₹{:,.0f}",
            "pnl": "₹{:,.0f}", "pnl_pct": "{:+.1f}%", "weight": "{:.1f}%"
        }),
        use_container_width=True, hide_index=True
    )

    st.markdown("""
    **Key observations**  
    - **Financial Services** is the largest and biggest rupee loser (IREDA + several NBFCs).  
    - **Engineering & Capital Goods** is over-diversified (12 names).  
    - **Defence** has strong order-book visibility despite valuation correction.  
    - **Metals** is skewed almost entirely by the SIYARAM-M micro-cap loss.  
    - **Retail** is the only meaningful sector in net profit (driven by EMIL).
    """)

elif page == "🔍 Stock Deep Dive":
    st.title("Stock Deep Dive + Live Data")
    sym = st.selectbox("Select stock", sorted(df.symbol.unique()))
    r = df[df.symbol == sym].iloc[0]

    st.header(f"{r.symbol}")
    st.caption(f"{r.sector} · Weight {r.weight}% · {r.frame} · Action: **{r.action}**")

    # Live price fetch
    with st.spinner("Fetching live price..."):
        live = get_live_price(sym)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Invested (book)", fmt_inr(r.invested))
    c2.metric("Book Value (4-Sep)", fmt_inr(r.current), f"LTP then ₹{r.ltp}")

    if live and live.get("price"):
        live_px = live["price"]
        live_val = live_px * r.qty
        live_pnl = live_val - r.invested
        live_pnl_pct = (live_pnl / r.invested) * 100
        delta_vs_book = live_px - r.ltp
        c3.metric("Live Price (Yahoo)", f"₹{live_px:,.2f}", f"{delta_vs_book:+.2f} vs book LTP")
        c4.metric("Live P&L", fmt_inr(live_pnl), f"{live_pnl_pct:+.1f}%")
    else:
        c3.metric("Live Price", "Unavailable")
        c4.metric("Live P&L", "—")
        st.warning("Live price not available from Yahoo Finance for this symbol right now. Book values still shown.")

    st.markdown(f"""
    | Metric | Value |
    |--------|-------|
    | Average Cost | ₹{r.avg} |
    | Book LTP (4-Sep-2026) | ₹{r.ltp} |
    | Qty (LT / ST) | {r.qty} ({r.lt} / {r.st}) |
    | Business Signal | {r.signal} |
    | Technical Signal | {r.tech} |
    """)

    # Historical chart
    st.subheader("Historical Price Trend")
    period = st.radio("Period", ["3mo", "6mo", "1y", "2y"], horizontal=True, index=2)
    hist = get_history(sym, period)
    if hist is not None and not hist.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hist["Date"], y=hist["Close"],
            mode="lines", name="Close",
            line=dict(color="#38bdf8", width=2)
        ))
        # Average cost line
        fig.add_hline(y=r.avg, line_dash="dash", line_color="#f59e0b",
                      annotation_text=f"Your Avg ₹{r.avg}", annotation_position="top left")
        fig.update_layout(
            height=380, margin=dict(t=30, b=30, l=40, r=20),
            xaxis_title=None, yaxis_title="Price (₹)",
            hovermode="x unified",
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
        # Simple stats
        ret = (hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100
        st.caption(f"Period return: **{ret:+.1f}%** · High: ₹{hist['High'].max():,.1f} · Low: ₹{hist['Low'].min():,.1f}")
    else:
        st.info("Historical data not available for this symbol via Yahoo Finance.")

    st.subheader("Research Note")
    st.write(r.note if r.note else "No additional note.")

    st.markdown("---")
    st.subheader("Independent Research Snapshot (early Sep 2026)")
    research = {
        "IREDA": "Business executing: record FY26 profit, loan book growth, sequential NPA improvement. Stock near 52W low mainly on PSU NBFC de-rating + FII flows. Structural renewable financing theme intact.",
        "SIYARAM-M": "Micro-cap recycling company (not textile). FY26 revenue −29%, profit −74%. Thin liquidity, stretched working capital. Recent small orders do not change the risk profile. Highest risk name in book.",
        "ROUTE": "Q1 FY27 revenue +9.6% YoY after soft FY26. Gross margins recovered earlier. Management guiding mid/high single-digit growth. Competitive CPaaS industry; stabilising after rough patch.",
        "BDL": "Order book ~₹26,000 Cr + fresh ₹1,348 Cr HAL order. Q1 FY27 revenue recovery after earlier supply delays. Valuation was extremely rich; correction largely multiple compression. Structural defence tailwind intact.",
        "JIOFIN": "Q1 FY27 PAT +156% YoY to ₹830 Cr. Strong AUM growth across lending, payments, AMC. One of the cleanest fundamental growth stories; underperformance mostly flow-driven.",
        "ZAGGLE": "Revenue still growing strongly; Q1 PAT hit by DICE acquisition integration costs. Management reaffirmed 40% revenue guidance for FY27. Integration risk is real.",
        "BBOX": "High ROE, expanding order backlog (AI/data-centre hyperscaler wins), strong revenue & EBITDA trajectory. Quality growth profile.",
        "HAL": "Massive order book (₹2.54 Lakh Cr cited), monopoly position in many platforms. Clean structural defence play.",
        "KPITTECH": "Caught in broader IT/ER&D headwind. Relative resilience due to auto-tech exposure. Sector recovery expected to be gradual.",
        "GREENPOWER": "Weak wind seasonality + 100% promoter pledge. Clear exit on governance + cyclical grounds.",
    }
    st.write(research.get(r.symbol, "No specific independent deep-dive note for this name in the current research set. Refer to sector context and business signal above."))
    st.caption("Live prices via Yahoo Finance (free, may be delayed 15–20 min). Not all Indian symbols are perfectly mapped; data can be missing for micro-caps.")

elif page == "🔄 Rebalance Framework":
    st.title("Rebalance Framework")
    st.markdown("""
    ### Core + Satellite (65/35 target)
    - **Core (60-70%)**: 8–15 highest-conviction names with structural growth, strong order books or high ROE (IREDA, JIOFIN, BBOX, HAL, BDL, GREENPLY, MAHSEAMLES, NPST, HDFCBANK, EMIL…).
    - **Satellite (30-40%)**: Higher-risk / higher-upside or smaller positions, deliberately sized 1–2% each.

    ### Three practical approaches
    1. **Core + Satellite** – Concentrate growth engine, ring-fence risk.
    2. **Sector Consolidation** – Instead of 12 Engineering or 9 Financial names, keep the best 2–4 per sector → total 20–25 holdings.
    3. **Barbell** – Explicit 70/30 or 80/20 split between compounders and high-growth/high-risk sleeve.

    ### Immediate cash from recommended exits
    """)
    exits = df[df.action == "EXIT"]
    st.dataframe(
        exits[["symbol", "current", "pnl_pct", "note"]].style.format({
            "current": "₹{:,.0f}", "pnl_pct": "{:+.0f}%"
        }),
        use_container_width=True, hide_index=True
    )
    st.success(f"Total capital that can be freed: **{fmt_inr(exits.current.sum())}**")

    st.markdown("""
    ### Suggested next steps (educational)
    1. Decide risk appetite explicitly (20% CAGR target implies tolerance for 30-40% drawdowns).
    2. Formally approve the three exits.
    3. Formally override stop-loss on the high-conviction turnaround names you wish to keep.
    4. Redeploy freed capital into Core sleeve while respecting a max single-stock concentration (e.g. 3.5–5%).
    5. Review quarterly results of override names within 180 days.
    """)

else:  # About
    st.title("About & Disclaimer")
    st.markdown("""
    ### What this tool is
    An interactive research dashboard built on your 4-Sep-2026 holdings statement and synthesised public information 
    (company results, exchange filings, news flow, order-book disclosures) as of early September 2026.

    It mirrors the depth of analysis performed in the accompanying research conversation:  
    macro context, business quality signals, technical proxy, Core/Satellite framework, explicit exit/override lists, 
    and rebalancing mathematics.

    ### How to run it for free
    1. **Streamlit Community Cloud** (recommended)  
       - Create a free account at [share.streamlit.io](https://share.streamlit.io)  
       - Push this folder to a public GitHub repo  
       - Deploy in one click – get a permanent public URL  
    2. **Locally**  
       ```bash
       pip install streamlit pandas plotly
       streamlit run app.py
       ```
    3. **Google Colab** – upload the file and run with a Streamlit tunnel if desired.

    ### Important disclaimer
    This is **not** investment advice.  
    It is **not** a SEBI-registered recommendation.  
    Live prices come from Yahoo Finance (free, often delayed 15–20 minutes) and may be missing for some Indian micro-caps.  
    Past performance and published research do not guarantee future results.  
    Always verify latest financials, order books and prices on NSE/BSE or your broker, and consult a SEBI-registered advisor before taking any action.

    Data sources: holdings-04.09.2026.pdf + public quarterly results, exchange announcements, news flow, and Yahoo Finance for live/historical prices.
    """)

st.sidebar.markdown("---")
st.sidebar.caption("Portfolio Analyser · Free educational tool")
