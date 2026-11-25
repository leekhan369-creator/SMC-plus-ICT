import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="ICT SMART AI TRADING BOT",
    page_icon="⚡",
    layout="wide"
)

# ================= BLACK GOLD THEME =================

st.markdown("""
<style>
.stApp {
    background-color: #080808;
    color: #F5F5F5;
}
[data-testid="stSidebar"] {
    background-color: #111111;
}
h1, h2, h3 {
    color: #D4AF37 !important;
}
.card {
    background: #171717;
    border: 1px solid #806820;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ================= CONFIGURATION =================

PRICE_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"

CANDLE_URL = (
    "https://api.exchange.coinbase.com/"
    "products/BTC-USD/candles"
)

TIMEFRAMES = {
    "1m": 60,
    "3m": 180,
    "5m": 300,
    "15m": 900,
    "30m": 1800,
    "1H": 3600,
    "2H": 7200,
    "4H": 21600,
    "Daily": 86400,
    "Weekly": 604800
}

# ================= BTC PRICE =================

@st.cache_data(ttl=30)
def get_price():

    response = requests.get(
        PRICE_URL,
        timeout=15
    )

    response.raise_for_status()

    return float(response.json()["data"]["amount"])


# ================= BTC CANDLES =================

@st.cache_data(ttl=60)
def get_candles(granularity):

    if granularity not in [60, 300, 900, 3600, 21600, 86400]:
        raise ValueError(
            "Coinbase does not support this candle timeframe."
        )

    response = requests.get(
        CANDLE_URL,
        params={"granularity": granularity},
        timeout=20,
        headers={"User-Agent": "ICT-SMART-AI"}
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError("No candle data received.")

    df = pd.DataFrame(
        data,
        columns=[
            "time", "low", "high",
            "open", "close", "volume"
        ]
    )

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col])

    df["time"] = pd.to_datetime(
        df["time"], unit="s", utc=True
    )

    return df.sort_values("time").reset_index(drop=True)


# ================= SIDEBAR =================

st.sidebar.title("⚡ ICT SMART AI")

page = st.sidebar.selectbox(
    "NAVIGATION",
    [
        "Home",
        "Gold Signals",
        "BTC Signals",
        "Live Chart",
        "Multi-Timeframe Dashboard",
        "Backtesting",
        "Historical Probabilities",
        "Trade History",
        "Risk Calculator",
        "Settings"
    ]
)

st.sidebar.divider()

st.sidebar.success("Dashboard: ONLINE")
st.sidebar.info("Trading: SIGNAL ONLY")
st.sidebar.warning("Automatic Orders: DISABLED")

# ================= HEADER =================

st.title("⚡ ICT SMART AI TRADING BOT")

st.caption(
    "ICT + SMC | QUALITY OVER QUANTITY | MANUAL EXECUTION ONLY"
)

st.divider()

# ================= BTC MARKET FUNCTION =================

def bitcoin_dashboard(show_chart=True):

    st.subheader("₿ BITCOIN MARKET DATA")

    try:
        price = get_price()

        st.success("COINBASE PRICE CONNECTION: SUCCESS")

        st.metric(
            "BTC/USD CURRENT PRICE",
            f"${price:,.2f}"
        )

        st.caption(
            "Source: Coinbase | " +
            datetime.now(timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        )

    except Exception as e:
        st.error("BTC PRICE DATA UNAVAILABLE")
        st.write(str(e))
        return

    if not show_chart:
        return

    timeframe = st.selectbox(
        "SELECT TIMEFRAME",
        list(TIMEFRAMES.keys()),
        key="btc_timeframe"
    )

    try:

        df = get_candles(TIMEFRAMES[timeframe])

        st.success("COINBASE CANDLE DATA: CONNECTED")

        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df["time"],
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"],
                    name="BTC/USD"
                )
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            height=500,
            title=f"BTC/USD — {timeframe}",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("LATEST MARKET CANDLES")

        st.dataframe(
            df.tail(10),
            use_container_width=True
        )

    except Exception as e:
        st.error("CANDLE DATA UNAVAILABLE")
        st.write(str(e))


# ================= HOME =================

if page == "Home":

    st.subheader("📊 MARKET OVERVIEW")

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="card">
        <h3>🟡 GOLD (XAUUSD)</h3>
        <h2>NO TRADE</h2>
        <p>Market Data: NOT CONNECTED</p>
        <p>Waiting for confirmation</p>
        </div>
        """, unsafe_allow_html=True)

    with b:
        st.markdown("""
        <div class="card">
        <h3>₿ BITCOIN (BTC/USD)</h3>
        <h2>LIVE DATA</h2>
        <p>Provider: Coinbase</p>
        <p>Trading: SIGNAL ONLY</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    bitcoin_dashboard(show_chart=False)

    st.warning(
        "ICT/SMC confirmation engine is not implemented yet."
    )


# ================= GOLD SIGNALS =================

elif page == "Gold Signals":

    st.header("🟡 GOLD SIGNALS")

    st.error("NO CONFIRMED SIGNAL")

    st.write("Market: XAUUSD")
    st.write("Data Source: Not connected")
    st.write("Entry: N/A")
    st.write("Stop Loss: N/A")
    st.write("TP1: N/A")
    st.write("TP2: N/A")
    st.write("TP3: N/A")

    st.info(
        "Authorized COMEX market data is required."
    )


# ================= BTC SIGNALS =================

elif page == "BTC Signals":

    st.header("₿ BTC SIGNALS")

    bitcoin_dashboard(show_chart=False)

    st.divider()

    st.warning("NO CONFIRMED ICT/SMC SIGNAL")

    st.info(
        "Live price does not automatically mean "
        "a confirmed trading setup."
    )


# ================= LIVE CHART =================

elif page == "Live Chart":

    st.header("📊 LIVE MARKET CHART")

    market = st.selectbox(
        "SELECT MARKET",
        ["BTC/USD", "XAUUSD"]
    )

    if market == "BTC/USD":
        bitcoin_dashboard()

    else:
        st.warning(
            "Gold chart requires an authorized data provider."
        )


# ================= MULTI TIMEFRAME =================

elif page == "Multi-Timeframe Dashboard":

    st.header("📊 MULTI-TIMEFRAME DASHBOARD")

    st.info(
        "BTC candle data is available only for supported "
        "Coinbase timeframes."
    )

    try:

        df = get_candles(3600)

        latest = df.iloc[-1]

        st.metric(
            "BTC/USD",
            f"${latest['close']:,.2f}"
        )

        rows = []

        for tf, seconds in TIMEFRAMES.items():

            if seconds not in [60, 300, 900, 3600, 21600, 86400]:
                rows.append({
                    "Timeframe": tf,
                    "BTC Status": "Not supported by Coinbase"
                })
                continue

            rows.append({
                "Timeframe": tf,
                "BTC Status": "Data available"
            })

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True
        )

    except Exception as e:

        st.error("MULTI-TIMEFRAME DATA UNAVAILABLE")
        st.write(str(e))


# ================= BACKTESTING =================

elif page == "Backtesting":

    st.header("📈 BACKTESTING ENGINE")

    st.warning("INSUFFICIENT VERIFIED DATA")

    st.write("Win Rate: Not calculated")
    st.write("Profit Factor: Not calculated")
    st.write("Maximum Drawdown: Not calculated")
    st.write("Expectancy: Not calculated")


# ================= HISTORICAL PROBABILITIES =================

elif page == "Historical Probabilities":

    st.header("🎯 TP PROBABILITY ENGINE")

    st.warning(
        "Historical testing engine is not implemented."
    )

    st.write("TP1 Probability: Not calculated")
    st.write("TP2 Probability: Not calculated")
    st.write("TP3 Probability: Not calculated")


# ================= TRADE HISTORY =================

elif page == "Trade History":

    st.header("📚 TRADE HISTORY")

    st.info("No recorded signals yet.")

    st.caption(
        "Historical results will appear after verified "
        "signal tracking is implemented."
    )


# ================= RISK CALCULATOR =================

elif page == "Risk Calculator":

    st.header("🛡️ RISK CALCULATOR")

    st.info(
        "Educational example only. "
        "No real-money trading recommendation."
    )

    balance = st.number_input(
        "Example Balance ($)",
        min_value=1.0,
        value=1000.0
    )

    risk = st.slider(
        "Example Percentage",
        0.1,
        2.0,
        1.0,
        0.1
    )

    amount = balance * risk / 100

    st.metric(
        "Illustrative Amount",
        f"${amount:.2f}"
    )


# ================= SETTINGS =================

elif page == "Settings":

    st.header("⚙️ BOT SETTINGS")

    st.write("BTC Market: BTC/USD")
    st.write("BTC Data Provider: Coinbase")
    st.write("Gold Data: Not connected")

    st.write("Trading Mode: SIGNAL ONLY")
    st.write("Automatic Execution: DISABLED")

    st.success("Dashboard configuration loaded.")


# ================= FOOTER =================

st.divider()

st.caption(
    "ICT SMART AI | EDUCATIONAL DASHBOARD | "
    "NO AUTOMATIC TRADING"
)

st.caption(
    "Dashboard Time (UTC): " +
    datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
)
