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
from fpdf import FPDF
import io

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
        "📊 Sector RS & Rotation",
        "🧮 Factor Scores",
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
    st.caption("Volume · RSI · MACD · SMA — computed from Yahoo Finance history. Educational only, not trading signals.")

    scope = st.radio("Scope", ["Selected stock", "Top 10 by invested", "All 52 stocks"], horizontal=True)
    period = st.selectbox("History period", ["3mo", "6mo", "1y", "2y"], index=2)

    def compute_ta_full(hist):
        if hist is None or len(hist) < 35:
            return None
        close = hist["Close"].astype(float)
        vol = hist["Volume"].astype(float) if "Volume" in hist.columns else None
        last = float(close.iloc[-1])

        # SMAs
        sma20 = float(close.rolling(20).mean().iloc[-1]) if len(close) >= 20 else None
        sma50 = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else None
        sma200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else None

        # RSI 14
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rs = gain / loss.replace(0, 1e-9)
        rsi_series = 100 - (100 / (1 + rs))
        rsi = float(rsi_series.iloc[-1]) if not rsi_series.empty else None

        # MACD (12, 26, 9)
        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        hist_macd = macd_line - signal_line
        macd_v = float(macd_line.iloc[-1])
        signal_v = float(signal_line.iloc[-1])
        hist_v = float(hist_macd.iloc[-1])
        prev_hist = float(hist_macd.iloc[-2]) if len(hist_macd) > 1 else 0
        if hist_v > 0 and prev_hist <= 0:
            macd_signal = "Bullish crossover"
        elif hist_v < 0 and prev_hist >= 0:
            macd_signal = "Bearish crossover"
        elif hist_v > 0:
            macd_signal = "Bullish (above signal)"
        else:
            macd_signal = "Bearish (below signal)"

        # Volume analysis
        vol_signal = "N/A"
        vol_ratio = None
        if vol is not None and vol.sum() > 0:
            recent = float(vol.tail(10).mean())
            longer = float(vol.tail(50).mean()) if len(vol) >= 50 else float(vol.mean())
            if longer > 0:
                vol_ratio = recent / longer
                if vol_ratio < 0.7:
                    vol_signal = "Drying up (low participation)"
                elif vol_ratio > 1.3:
                    vol_signal = "Rising liquidity / interest"
                else:
                    vol_signal = "Stable volume"

        # Trend
        if sma50 and last > sma50 and (sma20 is None or sma20 > sma50):
            trend = "Uptrend bias"
        elif sma50 and last < sma50:
            trend = "Downtrend bias"
        else:
            trend = "Range / mixed"

        # RSI indication
        if rsi is None:
            rsi_ind = "—"
        elif rsi < 30:
            rsi_ind = "Oversold zone"
        elif rsi > 70:
            rsi_ind = "Overbought zone"
        else:
            rsi_ind = "Neutral"

        return {
            "last": last, "sma20": sma20, "sma50": sma50, "sma200": sma200,
            "rsi": rsi, "rsi_ind": rsi_ind,
            "macd": macd_v, "macd_signal": signal_v, "macd_hist": hist_v, "macd_ind": macd_signal,
            "vol_ratio": vol_ratio, "vol_signal": vol_signal,
            "trend": trend,
            "ret_period": float(close.iloc[-1] / close.iloc[0] - 1) * 100,
            "hist": hist,
        }

    def render_ta_card(sym, ta, avg_cost):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Last Close", f"₹{ta['last']:,.2f}")
        c2.metric("RSI (14)", f"{ta['rsi']:.1f}" if ta['rsi'] else "—", ta.get("rsi_ind"))
        c3.metric("Period Return", f"{ta['ret_period']:+.1f}%")
        c4.metric("Trend", ta["trend"])
        c5, c6, c7 = st.columns(3)
        c5.metric("MACD", f"{ta['macd']:.2f}", ta["macd_ind"])
        vol_txt = f"{ta['vol_ratio']:.2f}x" if ta.get("vol_ratio") else "—"
        c6.metric("Vol (10d/50d)", vol_txt, ta.get("vol_signal"))
        c7.metric("Your Avg", f"₹{avg_cost}")
        s20 = f"{ta['sma20']:.1f}" if ta.get("sma20") else "—"
        s50 = f"{ta['sma50']:.1f}" if ta.get("sma50") else "—"
        s200 = f"{ta['sma200']:.1f}" if ta.get("sma200") else "—"
        st.caption(f"SMA20: {s20} · SMA50: {s50} · SMA200: {s200}")

    if scope == "Selected stock":
        sym = st.selectbox("Stock", sorted(df.symbol.unique()), key="ta_sym")
        with st.spinner("Loading history & computing indicators..."):
            hist = get_history(sym, period)
            ta = compute_ta_full(hist)
        r = df[df.symbol == sym].iloc[0]
        if ta:
            render_ta_card(sym, ta, r.avg)
            # Price + volume chart
            h = ta["hist"]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=h["Date"], y=h["Close"], name="Close", line=dict(color="#38bdf8"), yaxis="y1"))
            if len(h) >= 20:
                fig.add_trace(go.Scatter(x=h["Date"], y=h["Close"].rolling(20).mean(), name="SMA20", line=dict(color="#f59e0b", width=1), yaxis="y1"))
            if len(h) >= 50:
                fig.add_trace(go.Scatter(x=h["Date"], y=h["Close"].rolling(50).mean(), name="SMA50", line=dict(color="#a78bfa", width=1), yaxis="y1"))
            fig.add_hline(y=r.avg, line_dash="dash", line_color="#22c55e", annotation_text="Your Avg")
            if "Volume" in h.columns:
                fig.add_trace(go.Bar(x=h["Date"], y=h["Volume"], name="Volume", marker_color="rgba(148,163,184,0.4)", yaxis="y2"))
            fig.update_layout(
                height=420, hovermode="x unified", template="plotly_white",
                yaxis=dict(title="Price"), yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False),
                margin=dict(t=20, b=20), legend=dict(orientation="h")
            )
            st.plotly_chart(fig, use_container_width=True)
            # MACD panel
            close = h["Close"].astype(float)
            ema12 = close.ewm(span=12, adjust=False).mean()
            ema26 = close.ewm(span=26, adjust=False).mean()
            macd_line = ema12 - ema26
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            hist_m = macd_line - signal_line
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=h["Date"], y=macd_line, name="MACD", line=dict(color="#38bdf8")))
            fig2.add_trace(go.Scatter(x=h["Date"], y=signal_line, name="Signal", line=dict(color="#f59e0b")))
            colors = ["#22c55e" if v >= 0 else "#ef4444" for v in hist_m]
            fig2.add_trace(go.Bar(x=h["Date"], y=hist_m, name="Histogram", marker_color=colors))
            fig2.update_layout(height=220, template="plotly_white", margin=dict(t=10, b=10), legend=dict(orientation="h"))
            st.plotly_chart(fig2, use_container_width=True)
            st.markdown(f"""
**Interpretation (educational)**  
- **RSI**: {ta['rsi_ind']} (RSI can stay extreme in strong trends).  
- **MACD**: {ta['macd_ind']}.  
- **Volume**: {ta['vol_signal']} — ratio of recent 10-day avg volume vs ~50-day avg.  
- **Trend**: Price vs SMA50 / SMA20 relationship → {ta['trend']}.
""")
        else:
            st.warning("Not enough history for full indicators.")

    else:
        # Top 10 or All
        if scope == "Top 10 by invested":
            universe = df.nlargest(10, "invested")
        else:
            universe = df.sort_values("invested", ascending=False)
            st.warning("Analysing all 52 stocks may take 1–3 minutes depending on Yahoo rate limits. Data is cached.")

        rows = []
        progress = st.progress(0)
        status = st.empty()
        n = len(universe)
        for i, (_, row) in enumerate(universe.iterrows()):
            status.text(f"Processing {row.symbol} ({i+1}/{n})...")
            hist = get_history(row.symbol, period)
            ta = compute_ta_full(hist)
            if ta:
                rows.append({
                    "Symbol": row.symbol,
                    "Last": round(ta["last"], 2),
                    "RSI": round(ta["rsi"], 1) if ta["rsi"] else None,
                    "RSI zone": ta["rsi_ind"],
                    "MACD signal": ta["macd_ind"],
                    "Vol signal": ta["vol_signal"],
                    "Vol ratio": round(ta["vol_ratio"], 2) if ta.get("vol_ratio") else None,
                    "Trend": ta["trend"],
                    "Period %": round(ta["ret_period"], 1),
                    "Your Avg": row.avg,
                })
            else:
                rows.append({
                    "Symbol": row.symbol, "Last": None, "RSI": None, "RSI zone": "N/A",
                    "MACD signal": "N/A", "Vol signal": "N/A", "Vol ratio": None,
                    "Trend": "N/A", "Period %": None, "Your Avg": row.avg,
                })
            progress.progress((i + 1) / n)
        progress.empty()
        status.empty()
        out = pd.DataFrame(rows)
        st.dataframe(out, use_container_width=True, height=500, hide_index=True)
        st.caption("Vol ratio = recent 10-day average volume ÷ longer (~50-day) average. <0.7 drying up · >1.3 rising liquidity.")

elif page == "📄 Stock Report":
    st.title("Detailed Stock Report")
    st.caption("Position · Live price · Highs/Lows · Fundamentals · Promoter/Institutional notes · Sector context. Educational only.")

    sym = st.selectbox("Select stock for full report", sorted(df.symbol.unique()), key="report_sym")
    r = df[df.symbol == sym].iloc[0]

    st.header(f"{sym} — Full Report")
    st.write(f"**Sector**: {r.sector} · **Framework**: {r.frame} · **Action**: {r.action}")

    # ── 1. Position & prices ──
    st.subheader("1. Position & Prices")
    live = get_live_price(sym)
    cols = st.columns(5)
    cols[0].metric("Invested", fmt_inr(r.invested))
    cols[1].metric("Your Avg Cost", f"₹{r.avg}")
    cols[2].metric("Book LTP (4-Sep)", f"₹{r.ltp}")
    if live and live.get("price"):
        lp = live["price"]
        cols[3].metric("Live Price", f"₹{lp:,.2f}", f"{lp - r.ltp:+.2f}")
        live_pnl = lp * r.qty - r.invested
        cols[4].metric("Live P&L", fmt_inr(live_pnl), f"{(live_pnl/r.invested)*100:+.1f}%")
    else:
        cols[3].metric("Live Price", "N/A")
        cols[4].metric("Live P&L", "—")
    st.write(f"Qty: **{r.qty}** (LT {r.lt} / ST {r.st}) · Book value: {fmt_inr(r.current)}")

    # ── 2. High / Low / Average prices (1Y, 5Y, max available) ──
    st.subheader("2. High · Low · Average prices")
    with st.spinner("Loading multi-year history..."):
        hist_1y = get_history(sym, "1y")
        hist_5y = get_history(sym, "5y")
        hist_max = get_history(sym, "max")

    def hl_stats(hist, label):
        if hist is None or hist.empty:
            return {"period": label, "high": None, "low": None, "avg": None, "last": None, "from_high_pct": None}
        high = float(hist["High"].max())
        low = float(hist["Low"].min())
        avg = float(hist["Close"].mean())
        last = float(hist["Close"].iloc[-1])
        from_high = (last / high - 1) * 100 if high else None
        return {"period": label, "high": high, "low": low, "avg": avg, "last": last, "from_high_pct": from_high}

    rows_hl = [hl_stats(hist_1y, "1 Year"), hl_stats(hist_5y, "5 Year"), hl_stats(hist_max, "Max available")]
    hl_df = pd.DataFrame(rows_hl)
    # Format for display
    disp = []
    for row in rows_hl:
        disp.append({
            "Period": row["period"],
            "High": f"₹{row['high']:,.1f}" if row["high"] else "—",
            "Low": f"₹{row['low']:,.1f}" if row["low"] else "—",
            "Avg Close": f"₹{row['avg']:,.1f}" if row["avg"] else "—",
            "Last": f"₹{row['last']:,.1f}" if row["last"] else "—",
            "% from High": f"{row['from_high_pct']:+.1f}%" if row["from_high_pct"] is not None else "—",
        })
    st.dataframe(pd.DataFrame(disp), use_container_width=True, hide_index=True)
    st.caption("10-year exact window depends on listing date. 'Max available' uses full Yahoo history (may be <10y for newer listings). Your avg cost: ₹" + str(r.avg))

    # Chart 1Y with high/low markers
    if hist_1y is not None and not hist_1y.empty:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hist_1y["Date"], y=hist_1y["Close"], name="Close", line=dict(color="#38bdf8", width=2)))
        if len(hist_1y) >= 20:
            fig.add_trace(go.Scatter(x=hist_1y["Date"], y=hist_1y["Close"].rolling(20).mean(), name="SMA20", line=dict(width=1, color="#f59e0b")))
        if len(hist_1y) >= 50:
            fig.add_trace(go.Scatter(x=hist_1y["Date"], y=hist_1y["Close"].rolling(50).mean(), name="SMA50", line=dict(width=1, color="#a78bfa")))
        fig.add_hline(y=r.avg, line_dash="dash", line_color="#22c55e", annotation_text=f"Your Avg ₹{r.avg}")
        h1 = rows_hl[0]
        if h1["high"]:
            fig.add_hline(y=h1["high"], line_dash="dot", line_color="#ef4444", annotation_text="1Y High")
        if h1["low"]:
            fig.add_hline(y=h1["low"], line_dash="dot", line_color="#94a3b8", annotation_text="1Y Low")
        fig.update_layout(height=360, template="plotly_white", hovermode="x unified", margin=dict(t=10, b=20), title="1-Year price")
        st.plotly_chart(fig, use_container_width=True)

    # ── 3. Fundamentals (Yahoo + embedded) ──
    st.subheader("3. Company fundamentals (Yahoo Finance — limited for India)")
    fund = {}
    try:
        ticker = TICKER_MAP.get(sym)
        if ticker:
            info = yf.Ticker(ticker).info or {}
            keys = [
                "longName", "sector", "industry", "marketCap", "enterpriseValue",
                "trailingPE", "forwardPE", "pegRatio", "priceToBook", "priceToSalesTrailing12Months",
                "profitMargins", "operatingMargins", "grossMargins",
                "returnOnEquity", "returnOnAssets", "revenueGrowth", "earningsGrowth",
                "debtToEquity", "currentRatio", "quickRatio",
                "dividendYield", "payoutRatio",
                "recommendationKey", "targetMeanPrice", "targetHighPrice", "targetLowPrice",
                "numberOfAnalystOpinions", "fiftyTwoWeekHigh", "fiftyTwoWeekLow",
            ]
            fund = {k: info.get(k) for k in keys if info.get(k) is not None}
            if fund:
                # Pretty display
                mc = fund.get("marketCap")
                st.write(f"**{fund.get('longName', sym)}** · {fund.get('industry', fund.get('sector', ''))}")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Market Cap", fmt_inr(mc) if isinstance(mc, (int, float)) else "—")
                c2.metric("Trailing P/E", f"{fund['trailingPE']:.1f}" if fund.get("trailingPE") else "—")
                c3.metric("P/B", f"{fund['priceToBook']:.2f}" if fund.get("priceToBook") else "—")
                c4.metric("ROE", f"{fund['returnOnEquity']*100:.1f}%" if fund.get("returnOnEquity") else "—")
                c5, c6, c7, c8 = st.columns(4)
                c5.metric("Profit margin", f"{fund['profitMargins']*100:.1f}%" if fund.get("profitMargins") else "—")
                c6.metric("Rev growth", f"{fund['revenueGrowth']*100:.1f}%" if fund.get("revenueGrowth") else "—")
                c7.metric("Debt/Equity", f"{fund['debtToEquity']:.1f}" if fund.get("debtToEquity") else "—")
                c8.metric("Analyst target", f"₹{fund['targetMeanPrice']:.0f}" if fund.get("targetMeanPrice") else "—")
                with st.expander("All Yahoo fields returned"):
                    st.json(fund)
            else:
                st.info("Limited fundamental fields returned for this ticker.")
        else:
            st.info("No Yahoo ticker mapped.")
    except Exception as e:
        st.warning(f"Yahoo fundamentals error: {e}")

    # ── 4. Business signal & research ──
    st.subheader("4. Business signal & research notes")
    st.markdown(f"""
| Field | Detail |
|-------|--------|
| Business signal | {r.signal} |
| Technical signal (book) | {r.tech} |
| Action tag | **{r.action}** |
""")
    st.write(r.note or "No additional note.")

    research = {
        "IREDA": "Business executing: record FY26 profit, loan book growth, sequential NPA improvement. Near 52W low mainly on PSU NBFC de-rating + FII flows. Structural renewable financing theme. Promoter = Government of India (majority).",
        "SIYARAM-M": "Micro-cap recycling (not textile). FY26 revenue -29%, profit -74%. Thin liquidity, stretched WC. Highest risk. Promoter-dominated; limited institutional ownership.",
        "ROUTE": "Q1 FY27 revenue +9.6% YoY after soft FY26. Gross margins recovered. Competitive CPaaS. Stabilising. Institutional ownership present.",
        "BDL": "Order book ~₹26,000 Cr + ₹1,348 Cr HAL order. Q1 FY27 revenue recovery. Valuation was very rich. Structural defence tailwind. Promoter = GoI.",
        "JIOFIN": "Q1 FY27 PAT +156% YoY. Strong AUM growth across lending/payments/AMC. Reliance ecosystem promoter. Institutional interest rising with scale.",
        "ZAGGLE": "Revenue growing; PAT hit by DICE integration costs. FY27 40% revenue guidance reiterated. Watch institutional holding post acquisition.",
        "BBOX": "High ROE, expanding AI/data-centre backlog. Quality growth profile. Institutional interest supportive of turnaround.",
        "HAL": "Massive order book, monopoly platforms. Clean structural defence play. Promoter = GoI.",
        "KPITTECH": "IT/ER&D headwind. Relative resilience via auto-tech. Brokerages relatively constructive vs large-cap IT.",
        "GREENPOWER": "Weak wind seasonality + 100% promoter pledge. Clear exit on governance + cyclical grounds.",
        "HDFCBANK": "Stabilizer. Modest growth by design. Large FII+DII ownership. Core long-term hold for many brokerages.",
        "HINDZINC": "Peak profitability, silver contribution high, low mining costs. Vedanta group promoter. Commodity-cycle sensitive.",
        "EMIL": "Strong SSSG and profit growth; thin-margin consumer electronics retail. Momentum excellent; margin durability to watch.",
        "PCBL": "Specialty black growth, PAT +65% cited in earlier research. Chemicals cycle / oil-linked input costs.",
        "NTPCGREEN": "Renewable policy tailwind; execution risk varies. Part of NTPC group ecosystem.",
        "JSWENERGY": "Capacity additions; energy transition theme.",
        "GRSE": "Defence shipbuilding, Navratna, structural capex tailwind. Promoter = GoI.",
        "DIXON": "EMS / Make-in-India beneficiary. Strong price performance in book.",
        "GREENPLY": "Growth with leverage and rich valuation; capacity expansion underway.",
        "MAHSEAMLES": "Historically strong ROCE/ROE; recent quarter wobble — confirm next results.",
    }
    st.write("**Research snapshot:**", research.get(sym, "No extended note in embedded set. Use business signal + Yahoo fields above."))

    # ── 5. Promoter & institutional ──
    st.subheader("5. Promoter & institutional holdings")
    st.markdown("""
**Important:** Free APIs do **not** provide reliable, up-to-date Indian **promoter %**, **quarter-on-quarter changes**, or **full MF/FII break-up**.  
Authoritative sources (check these for live data):

| Source | What you get |
|--------|----------------|
| [NSE](https://www.nseindia.com) → company → Shareholding pattern | Promoter, FII, DII, public % by quarter |
| [Screener.in](https://www.screener.in) | Promoter trend chart, MF holdings, quarterly results |
| [Trendlyne](https://trendlyne.com) | Shareholding changes, bulk/block deals, analyst ratings |

**Embedded notes for this portfolio:**
""")
    promoter_notes = {
        "IREDA": "Promoter: Government of India (majority PSU). Holding changes are policy-driven and infrequent.",
        "BDL": "Promoter: Government of India (defence PSU).",
        "HAL": "Promoter: Government of India.",
        "GRSE": "Promoter: Government of India (Navratna shipyard).",
        "IRFC": "Promoter: Government of India.",
        "PFC": "Promoter: Government of India.",
        "JIOFIN": "Promoter group: Reliance. Strong promoter commitment; institutional (FII/DII) interest has grown with scale-up.",
        "HDFCBANK": "Widely held by FIIs and DIIs; among the highest institutional ownership names in the book.",
        "SIYARAM-M": "Promoter-dominated micro-cap; limited public float and institutional ownership → higher governance & liquidity risk.",
        "HINDZINC": "Promoter: Vedanta group. Commodity major with significant institutional following.",
        "RELIANCE": "Promoter: Reliance group. Flagship; heavy institutional ownership.",
        "GREENPOWER": "Research flagged 100% promoter stake pledged — governance red flag.",
    }
    note = promoter_notes.get(sym)
    if note:
        st.info(note)
    else:
        st.write("No specific promoter note stored for this symbol. Check NSE shareholding pattern for latest promoter / FII / DII % and QoQ changes.")

    st.markdown("""
**Market-level context (2025–26):** Prolonged FII selling hit mid/small-caps hardest; DIIs were partial absorbers. Many names in this book saw multiple compression even when business metrics held up.
""")

    # ── 6. Sector context ──
    st.subheader("6. Sector context")
    sector_ctx = {
        "FINANCIAL SERVICES": "Largest sector in the book and largest rupee drag. Mix of PSU NBFCs (IREDA, IRFC, PFC), private banks (HDFC), and newer platforms (JIOFIN, ZAGGLE, FINOPB). Sector hit by FII outflows and NBFC multiple compression. Quality varies sharply — JIOFIN/HDFC stronger than pure PSU beta.",
        "ENGINEERING & CAPITAL GOODS": "Most fragmented (12 names). Make-in-India / infra / EMS themes. Execution quality uneven. Better names (DIXON, KAYNES, GENUSPOWER) vs weaker order-book/quality stories. Over-diversified — consolidation would help.",
        "DEFENCE": "Structural multi-year tailwind from rising budgets and indigenisation. HAL cleanest monopoly; BDL strong order book but rich valuations corrected; GRSE shipbuilding. Govt promoters. Visibility high; near-term risk is execution and multiple.",
        "SOFTWARE SERVICES": "Genuine multi-year headwind (visa costs, outsourcing tax risk, soft global tech spend). KPIT relatively better positioned (auto ER&D); ROUTE stabilising after soft year; pure IT services names face sector current.",
        "ENERGY": "Renewable policy tailwind (500 GW non-fossil) vs execution risk in crowded cohort. NTPCGREEN / JSWENERGY higher quality than GREENPOWER (pledge + weak seasonality).",
        "METALS": "Dominated by SIYARAM-M micro-cap loss. HINDZINC is high-quality cash generator; TATASTEEL India ROCE supportive.",
        "CHEMICALS": "PCBL specialty growth; KIRIINDUS turnaround but other-income heavy. Oil-linked input costs matter.",
        "BUILDING MATERIALS": "Mixed. GREENPLY growth + leverage; MAHSEAMLES strong history with recent wobble; HITECH lagging.",
        "RETAIL": "Only sector in meaningful net profit in the book (EMIL). DMART softer. Consumer electronics retail is structurally thin-margin.",
        "TELECOM": "BBOX stands out with high ROE and AI/data-centre backlog growth.",
        "FMCG": "BECTORFOOD stable; JAYSREETEA stagnant agri — exit candidate.",
        "LOGISTICS": "GPPL: port/concession linked; Ro-Ro volumes and PAT growth cited earlier.",
        "PACKAGING": "AGI: domestic demand-driven, in profit in the book.",
        "FERTILIZERS": "GSFC: policy/subsidy linked.",
        "HEALTHCARE": "DENISCHEM-X: small weight, steep loss — company-specific.",
    }
    st.write(sector_ctx.get(r.sector, "No extended sector note for this classification."))

    # ── 7. PDF export ──
    st.markdown("---")
    st.subheader("Export PDF")
    if st.button("Generate PDF report", type="primary"):
        def pdf_safe(s):
            """Strip/replace characters Helvetica cannot render."""
            if s is None:
                return "-"
            s = str(s)
            repl = {
                "₹": "Rs ", "—": "-", "–": "-", "−": "-", "×": "x",
                "‘": "'", "’": "'", "“": '"', "”": '"', "…": "...",
                "≥": ">=", "≤": "<=", "→": "->", "≈": "~",
                "\n": " ", "\r": " ",
            }
            for a, b in repl.items():
                s = s.replace(a, b)
            # drop any remaining non-latin1
            return s.encode("latin-1", "replace").decode("latin-1")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, pdf_safe(f"Stock Report: {sym}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, pdf_safe(f"Generated: {datetime.now().strftime('%d %b %Y %H:%M')} IST"), new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 8, pdf_safe(f"Sector: {r.sector} | Framework: {r.frame} | Action: {r.action}"), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Position", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, pdf_safe(f"Invested: Rs {r.invested:,.0f} | Avg: Rs {r.avg} | Book LTP: Rs {r.ltp}"), new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 7, pdf_safe(f"Qty: {r.qty} (LT {r.lt} / ST {r.st}) | Book value: Rs {r.current:,.0f}"), new_x="LMARGIN", new_y="NEXT")
        if live and live.get("price"):
            lp = live["price"]
            live_pnl = lp * r.qty - r.invested
            pdf.cell(0, 7, pdf_safe(f"Live: Rs {lp:,.2f} | Live P&L: Rs {live_pnl:,.0f} ({(live_pnl/r.invested)*100:+.1f}%)"), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "High / Low / Avg", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        for row in rows_hl:
            if row["high"]:
                line = f"{row['period']}: High Rs {row['high']:,.1f} | Low Rs {row['low']:,.1f} | Avg Rs {row['avg']:,.1f} | From high {row['from_high_pct']:+.1f}%"
                pdf.cell(0, 6, pdf_safe(line), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Business & Research", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        usable = pdf.epw  # effective page width
        pdf.multi_cell(usable, 5, pdf_safe(f"Signal: {r.signal}"))
        pdf.multi_cell(usable, 5, pdf_safe(f"Note: {r.note or '-'}"))
        pdf.multi_cell(usable, 5, pdf_safe(f"Research: {research.get(sym, 'No extended note.')}"))
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Promoter / Institutional", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(usable, 5, pdf_safe(promoter_notes.get(sym, "Check NSE shareholding pattern for live promoter/FII/DII %.")))
        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Sector", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(usable, 5, pdf_safe(sector_ctx.get(r.sector, "-")[:500]))
        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 8, "Disclaimer", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(usable, 5, "Educational only. Not investment advice. Live data from Yahoo Finance may be delayed. Verify on NSE/BSE. Consult SEBI-registered advisor.")
        buf = io.BytesIO()
        pdf.output(buf)
        st.download_button(
            "Download PDF",
            data=buf.getvalue(),
            file_name=f"{sym}_report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
        )

    st.caption("Educational report only. Not investment advice. High/low from Yahoo history; promoter % must be verified on NSE.")


elif page == "📊 Sector RS & Rotation":
    st.title("Sector Relative Strength & Rotation")
    st.caption("Portfolio sector returns vs Nifty · Momentum · Simple rotation framework. Educational only.")

    st.markdown("""
### Concepts
| Term | Meaning |
|------|---------|
| **Relative Strength (RS)** | Sector return − benchmark return (here: Nifty 50 via Yahoo `^NSEI`) |
| **Momentum** | Absolute price trend over a lookback (e.g. 3M / 6M return, or % above SMA) |
| **Sector rotation** | Capital shifting from lagging sectors into leading ones as the cycle moves |

**RS ≠ Momentum:** A sector can have *positive momentum* (prices rising) but *negative RS* (rising slower than Nifty), or the reverse after a sharp market drop.
""")

    period = st.selectbox("Lookback for RS & momentum", ["1mo", "3mo", "6mo", "1y"], index=2, key="rs_period")

    # Map period to yfinance period string
    yf_period = {"1mo": "1mo", "3mo": "3mo", "6mo": "6mo", "1y": "1y"}[period]

    @st.cache_data(ttl=600, show_spinner=False)
    def nifty_return(period_str):
        try:
            h = yf.Ticker("^NSEI").history(period=period_str)
            if h is None or len(h) < 2:
                return None
            return float(h["Close"].iloc[-1] / h["Close"].iloc[0] - 1) * 100
        except Exception:
            return None

    @st.cache_data(ttl=600, show_spinner=False)
    def symbol_return(symbol, period_str):
        hist = get_history(symbol, period_str)
        if hist is None or len(hist) < 2:
            return None
        return float(hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100

    with st.spinner("Fetching Nifty & sector stock returns..."):
        nifty_ret = nifty_return(yf_period)

    if nifty_ret is None:
        st.warning("Could not fetch Nifty (^NSEI) return. RS will be shown as portfolio sector absolute returns only.")
        nifty_ret = 0.0
        st.metric("Nifty 50 return (lookback)", "N/A")
    else:
        st.metric("Nifty 50 return (lookback)", f"{nifty_ret:+.2f}%")

    # Build sector-level value-weighted returns from holdings
    # For each sector: weight by invested, average stock returns where available
    sector_rows = []
    sectors = sorted(df.sector.unique())
    progress = st.progress(0)
    status = st.empty()

    for i, sec in enumerate(sectors):
        status.text(f"Sector: {sec}")
        sub = df[df.sector == sec]
        total_inv = sub["invested"].sum()
        wret = 0.0
        wsum = 0.0
        n_ok = 0
        mom_list = []
        for _, row in sub.iterrows():
            ret = symbol_return(row.symbol, yf_period)
            if ret is not None:
                w = row.invested / total_inv if total_inv else 0
                wret += w * ret
                wsum += w
                mom_list.append(ret)
                n_ok += 1
        if wsum > 0:
            sec_ret = wret  # already weighted
        else:
            sec_ret = None
        rs = (sec_ret - nifty_ret) if sec_ret is not None else None
        # Book P&L as secondary view
        book_pnl_pct = (sub["pnl"].sum() / sub["invested"].sum() * 100) if sub["invested"].sum() else 0
        sector_rows.append({
            "Sector": sec,
            "Holdings": len(sub),
            "Invested weight %": round(total_inv / df["invested"].sum() * 100, 1),
            "Lookback return %": round(sec_ret, 2) if sec_ret is not None else None,
            "Nifty return %": round(nifty_ret, 2),
            "RS (ret − Nifty)": round(rs, 2) if rs is not None else None,
            "Book P&L %": round(book_pnl_pct, 1),
            "Stocks with data": n_ok,
            "Momentum avg %": round(sum(mom_list)/len(mom_list), 2) if mom_list else None,
        })
        progress.progress((i + 1) / len(sectors))
    progress.empty()
    status.empty()

    rs_df = pd.DataFrame(sector_rows).sort_values("RS (ret − Nifty)", ascending=False, na_position="last")

    st.subheader("Sector RS ranking (your portfolio sleeves)")
    st.dataframe(rs_df, use_container_width=True, hide_index=True, height=420)

    # Scatter: Momentum vs RS
    plot_df = rs_df.dropna(subset=["RS (ret − Nifty)", "Momentum avg %"])
    if len(plot_df) > 0:
        st.subheader("Momentum vs Relative Strength")
        fig = px.scatter(
            plot_df, x="Momentum avg %", y="RS (ret − Nifty)",
            size="Invested weight %", hover_name="Sector",
            text="Sector",
            title="Bubble size = portfolio weight",
            color="RS (ret − Nifty)",
            color_continuous_scale=["#ef4444", "#f59e0b", "#22c55e"],
        )
        fig.add_hline(y=0, line_dash="dash", line_color="#94a3b8")
        fig.add_vline(x=0, line_dash="dash", line_color="#94a3b8")
        fig.update_traces(textposition="top center")
        fig.update_layout(height=480, template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
**Quadrant read**
| Quadrant | Meaning | Typical action bias |
|----------|---------|---------------------|
| **+Mom +RS** (top-right) | Rising and beating Nifty | Leadership — candidates for Core weight |
| **+Mom −RS** (bottom-right) | Rising but lagging Nifty | Market beta, not true leadership |
| **−Mom +RS** (top-left) | Falling less than Nifty | Relative defensive strength |
| **−Mom −RS** (bottom-left) | Falling and lagging | Weak — need stock-specific thesis or trim |
""")

    # Rotation narrative
    st.subheader("Sector rotation framework (how to use this)")
    st.markdown("""
Classic rotation cycle (simplified):

1. **Early recovery** — Financials, Discretionary often lead  
2. **Mid-cycle expansion** — Industrials, Materials, Capex themes  
3. **Late cycle** — Energy, Commodities  
4. **Slowdown / risk-off** — Staples, Pharma/Healthcare, quality defensives  
5. **Deep risk-off** — Cash / bonds; high-beta midcaps suffer  

**2026 India colour (from public sector performance):**  
Metals & Pharma/Healthcare showed **leadership**; IT & FMCG were **laggards**; Financials mixed under FII pressure.  
Your book is heavy in **Financials + Software/IT + fragmented Engg** — sleeves that map more to mixed/weak RS than to 2026 leadership sectors.

**Rotation vs your decisions**
- Don’t add pure beta to **−Mom −RS** sectors without a strong stock story  
- Prefer **+RS** names when increasing risk  
- Use **book P&L %** column as a reality check: sector RS can look fine while your specific holdings lag (e.g. metals RS strong, Siyaram-M still a large loss)
""")

    # Simple signals table
    st.subheader("Quick signals for your sleeves")
    signals = []
    for _, row in rs_df.iterrows():
        rs = row["RS (ret − Nifty)"]
        mom = row["Momentum avg %"]
        if rs is None or mom is None:
            sig = "Insufficient data"
        elif rs > 0 and mom > 0:
            sig = "Leadership (Mom+ RS+)"
        elif rs > 0 and mom <= 0:
            sig = "Relative defensive"
        elif rs <= 0 and mom > 0:
            sig = "Beta only (Mom+ RS−)"
        else:
            sig = "Weak (Mom− RS−)"
        signals.append({"Sector": row["Sector"], "Signal": sig, "Weight %": row["Invested weight %"]})
    st.dataframe(pd.DataFrame(signals), use_container_width=True, hide_index=True)

    st.caption("Returns from Yahoo Finance history (delayed). Value-weighted by your invested amount. Not investment advice.")


elif page == "🧮 Factor Scores":
    st.title("Factor Scores")
    st.caption("Simple Quality · Momentum · Value proxies + composite. Educational scoring only — not a buy/sell signal.")

    st.markdown("""
| Factor | Proxy used here |
|--------|-----------------|
| **Quality** | Book signal strength + frame (CORE boost) + action tag penalty for EXIT |
| **Momentum** | Lookback price return from Yahoo history (optional live) |
| **Value** | Rough: deeper drawdown from your avg / book LTP treated as cheaper (heuristic only) |
| **Composite** | 0.4×Quality + 0.35×Momentum + 0.25×Value (then adjusted by action tag) |
""")

    lookback = st.selectbox("Momentum lookback", ["3mo", "6mo", "1y"], index=1, key="factor_lb")
    use_live_mom = st.checkbox("Compute live momentum from Yahoo (slower)", value=True)

    def quality_score(row):
        # 0–100 heuristic from embedded research fields
        s = 50.0
        sig = str(row.signal).lower()
        if "strong" in sig or "high roe" in sig or "improving" in sig:
            s += 20
        if "weak" in sig or "stagnant" in sig or "pledge" in sig:
            s -= 25
        if "mixed" in sig or "de-rating" in sig:
            s -= 5
        if row.frame == "CORE":
            s += 15
        if row.action == "EXIT":
            s -= 30
        elif row.action == "OVERRIDE":
            s += 5  # business thesis still active
        elif "WATCH" in str(row.action):
            s -= 10
        # pnl as soft quality of entry timing (not pure quality)
        if row.pnl_pct <= -40:
            s -= 10
        elif row.pnl_pct >= 15:
            s += 5
        return max(0, min(100, s))

    def value_score(row):
        # Heuristic: more negative pnl_pct → "cheaper" vs cost (NOT fundamental value)
        # Clamp so extreme losers aren't auto-attractive
        pct = row.pnl_pct
        if pct >= 20:
            return 25  # expensive vs your cost
        if pct >= 0:
            return 45
        if pct >= -15:
            return 60
        if pct >= -30:
            return 70
        if pct >= -45:
            return 55  # deep but may be value trap
        return 35  # very deep — trap risk high

    @st.cache_data(ttl=600, show_spinner=False)
    def mom_return(symbol, period):
        hist = get_history(symbol, period)
        if hist is None or len(hist) < 2:
            return None
        return float(hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100

    rows = []
    if use_live_mom:
        progress = st.progress(0)
        status = st.empty()
        n = len(df)
        for i, (_, row) in enumerate(df.iterrows()):
            status.text(f"Momentum: {row.symbol}")
            m = mom_return(row.symbol, lookback)
            # Map return to 0–100 score
            if m is None:
                mom_s = 50
                m_disp = None
            else:
                # -30% → 0, 0% → 50, +30% → 100
                mom_s = max(0, min(100, 50 + m * (50 / 30)))
                m_disp = round(m, 1)
            q = quality_score(row)
            v = value_score(row)
            comp = 0.40 * q + 0.35 * mom_s + 0.25 * v
            # Action tag overlay
            if row.action == "EXIT":
                comp *= 0.55
            elif "WATCH" in str(row.action):
                comp *= 0.85
            rows.append({
                "Symbol": row.symbol,
                "Sector": row.sector,
                "Frame": row.frame,
                "Action": row.action,
                "Quality": round(q, 0),
                "Momentum": round(mom_s, 0),
                "Mom %": m_disp,
                "Value (heur)": round(v, 0),
                "Composite": round(comp, 0),
                "Book P&L %": row.pnl_pct,
                "Weight %": row.weight,
            })
            progress.progress((i + 1) / n)
        progress.empty()
        status.empty()
    else:
        for _, row in df.iterrows():
            q = quality_score(row)
            v = value_score(row)
            mom_s = 50
            comp = 0.40 * q + 0.35 * mom_s + 0.25 * v
            if row.action == "EXIT":
                comp *= 0.55
            elif "WATCH" in str(row.action):
                comp *= 0.85
            rows.append({
                "Symbol": row.symbol,
                "Sector": row.sector,
                "Frame": row.frame,
                "Action": row.action,
                "Quality": round(q, 0),
                "Momentum": mom_s,
                "Mom %": None,
                "Value (heur)": round(v, 0),
                "Composite": round(comp, 0),
                "Book P&L %": row.pnl_pct,
                "Weight %": row.weight,
            })

    fdf = pd.DataFrame(rows).sort_values("Composite", ascending=False)

    st.subheader("Ranked by composite factor score")
    st.dataframe(fdf, use_container_width=True, height=520, hide_index=True)

    c1, c2, c3 = st.columns(3)
    top = fdf.head(8)
    bottom = fdf.tail(8)
    with c1:
        st.markdown("**Top composite**")
        st.write(", ".join(top["Symbol"].tolist()))
    with c2:
        st.markdown("**EXIT tagged (should score low)**")
        exits = fdf[fdf.Action == "EXIT"]["Symbol"].tolist()
        st.write(", ".join(exits) if exits else "—")
    with c3:
        st.markdown("**CORE with high score**")
        core_hi = fdf[(fdf.Frame == "CORE") & (fdf.Composite >= 55)]["Symbol"].tolist()
        st.write(", ".join(core_hi) if core_hi else "—")

    st.subheader("How to read scores")
    st.markdown("""
- **Quality ≥ 70 + CORE** → hold / add-on-dips candidates  
- **Composite ≤ 35 or Action = EXIT** → trim / exit priority  
- **High Value score + low Quality** → classic value-trap risk (deep loss without business quality)  
- **High Momentum + low Quality** → speculative; size small or skip  
- Scores are **portfolio-relative heuristics**, not academic factor portfolios
""")

    st.markdown("---")
    st.subheader("Quarterly rebalance checklist")
    st.markdown("""
### Quarterly process (repeat every ~90 days)

**A. Data refresh (day 1)**
1. Update prices / P&L (broker export or live fetch in All Holdings)
2. Run **Factor Scores** (6M momentum)
3. Run **Sector RS & Rotation** (6M)
4. Skim **Actions & Recs** EXIT / OVERRIDE lists

**B. Hard rules (do these first)**
| Rule | Action |
|------|--------|
| Action tag = **EXIT** | Sell remaining quantity (or finish staged exit) |
| Promoter pledge / governance red flag still true | Keep in EXIT |
| Composite ≤ 30 **and** Quality ≤ 40 | Strong trim candidate even if not tagged EXIT |
| Single name > 12% of portfolio | Trim toward 8–10% unless CORE + Quality ≥ 70 |

**C. Core sleeve (target ~60–65%)**
1. List Frame = CORE
2. Keep if Quality ≥ 55 **or** OVERRIDE with improving business note
3. Add only to CORE names with Quality ≥ 65 and Composite ≥ 55
4. Prefer funding adds from EXIT proceeds and weak Satellite trims

**D. Satellite sleeve (target ~35–40%)**
1. Keep Satellite if Composite ≥ 50 **or** clear catalyst within 2 quarters
2. Trim Satellite if Composite < 45 **and** Sector RS is negative
3. No new Satellite micro-caps without Quality ≥ 60

**E. Factor balance check**
1. Count names with Quality ≥ 65 → want a meaningful Core share
2. Avoid adding pure Momentum names with Quality < 45
3. Treat deep-loss “Value” scores as traps unless research shows earnings repair

**F. After trades**
1. Recompute weights vs 65/35 Core–Satellite target
2. Log: date, symbols sold/bought, reason (EXIT / factor / RS / size)
3. Next review date = +90 days (or sooner if macro shock)

**G. Do-not-do list**
- Don’t average down EXIT names  
- Don’t add to −RS sectors without Quality ≥ 65  
- Don’t let one OVERRIDE become >10–12% without fresh thesis review  
""")

    st.caption("Factor proxies are simplified for this portfolio tool. Not investment advice. Verify with NSE data and a SEBI-registered advisor.")

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
