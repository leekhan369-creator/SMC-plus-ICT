import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone

# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="ICT SMART AI TRADING BOT",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #080808;
    color: white;
}
[data-testid="stSidebar"] {
    background-color: #151515;
}
h1, h2, h3 {
    color: #D4AF37 !important;
}
</style>
""", unsafe_allow_html=True)


# ---------------- CONFIGURATION ----------------

PRICE_URL = (
    "https://api.coinbase.com/v2/prices/BTC-USD/spot"
)

CANDLE_URL = (
    "https://api.exchange.coinbase.com/"
    "products/BTC-USD/candles"
)

TIMEFRAMES = {
    "1 Minute": 60,
    "5 Minutes": 300,
    "15 Minutes": 900,
    "1 Hour": 3600,
    "6 Hours": 21600,
    "Daily": 86400
}


# ---------------- BTC LIVE PRICE ----------------

@st.cache_data(ttl=30)
def get_price():

    response = requests.get(
        PRICE_URL,
        timeout=15
    )

    response.raise_for_status()

    data = response.json()

    return float(data["data"]["amount"])


# ---------------- BTC CANDLES ----------------

@st.cache_data(ttl=60)
def get_candles(granularity):

    response = requests.get(
        CANDLE_URL,
        params={
            "granularity": granularity
        },
        timeout=20,
        headers={
            "User-Agent": "ICT-SMART-AI-DASHBOARD"
        }
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError("Coinbase returned no candle data.")

    df = pd.DataFrame(
        data,
        columns=[
            "time",
            "low",
            "high",
            "open",
            "close",
            "volume"
        ]
    )

    for col in [
        "open",
        "high",
        "low",
        "close",
        "volume"
    ]:
        df[col] = pd.to_numeric(df[col])

    df["time"] = pd.to_datetime(
        df["time"],
        unit="s",
        utc=True
    )

    df = df.sort_values(
        "time"
    ).reset_index(drop=True)

    return df


# ---------------- SIDEBAR ----------------

st.sidebar.title("⚡ ICT SMART AI")

page = st.sidebar.selectbox(
    "NAVIGATION",
    [
        "Home",
        "BTC Market",
        "Gold Market",
        "ICT Signals",
        "Backtesting",
        "Historical Probabilities",
        "Risk Calculator",
        "Settings"
    ]
)

st.sidebar.divider()

st.sidebar.markdown("### SYSTEM STATUS")
st.sidebar.success("Dashboard: ONLINE")
st.sidebar.info("Trading: SIGNAL ONLY")
st.sidebar.warning("Automatic Orders: DISABLED")


# ---------------- HEADER ----------------

st.title("⚡ ICT SMART AI TRADING BOT")

st.caption(
    "ICT + SMC | QUALITY OVER QUANTITY | "
    "MANUAL EXECUTION ONLY"
)

st.divider()


# ---------------- BTC DASHBOARD ----------------

def bitcoin_dashboard():

    st.subheader("₿ BITCOIN MARKET DATA")

    try:

        price = get_price()

        st.success("COINBASE PRICE CONNECTION: SUCCESS")

        st.metric(
            "BTC/USD CURRENT PRICE",
            f"${price:,.2f}"
        )

        st.caption(
            "Source: Coinbase Public API | "
            + datetime.now(timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        )

    except Exception as e:

        st.error("BTC PRICE DATA UNAVAILABLE")
        st.write(str(e))

        return

    st.divider()

    timeframe = st.selectbox(
        "SELECT TIMEFRAME",
        list(TIMEFRAMES.keys())
    )

    try:

        df = get_candles(
            TIMEFRAMES[timeframe]
        )

        if df.empty:
            st.warning("No candle data available.")
            return

        st.success("COINBASE CANDLE DATA: CONNECTED")

        st.write(
            "Latest candle:",
            df.iloc[-1]["time"].strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        )

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
            df[
                [
                    "time",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume"
                ]
            ].tail(10),
            use_container_width=True
        )

    except Exception as e:

        st.error("CANDLE DATA UNAVAILABLE")
        st.write(str(e))


# ---------------- HOME ----------------

if page == "Home":

    st.subheader("📊 MARKET OVERVIEW")

    a, b = st.columns(2)

    with a:
        st.metric("MARKET", "BTC/USD")
        st.metric("DATA PROVIDER", "Coinbase")

    with b:
        st.metric("TRADING MODE", "SIGNAL ONLY")
        st.metric("AUTO EXECUTION", "DISABLED")

    st.divider()

    bitcoin_dashboard()

    st.warning(
        "ICT/SMC confirmation engine is not implemented yet."
    )


# ---------------- BTC MARKET ----------------

elif page == "BTC Market":

    st.title("₿ BTC MARKET ANALYSIS")

    bitcoin_dashboard()


# ---------------- GOLD MARKET ----------------

elif page == "Gold Market":

    st.title("🥇 GOLD MARKET")

    st.warning(
        "Gold market data is not connected."
    )

    st.info(
        "Authorized COMEX data is required."
    )


# ---------------- ICT SIGNALS ----------------

elif page == "ICT Signals":

    st.title("🎯 ICT + SMC SIGNALS")

    st.warning(
        "NO CONFIRMED SIGNAL"
    )

    st.write(
        "Market structure, liquidity and "
        "entry confirmation engine is not implemented."
    )

    st.info(
        "No artificial trading signals will be generated."
    )


# ---------------- BACKTESTING ----------------

elif page == "Backtesting":

    st.title("📈 BACKTESTING ENGINE")

    st.warning("INSUFFICIENT VERIFIED DATA")

    st.write("Win Rate: Not calculated")
    st.write("Profit Factor: Not calculated")
    st.write("Maximum Drawdown: Not calculated")


# ---------------- HISTORICAL PROBABILITIES ----------------

elif page == "Historical Probabilities":

    st.title("🎯 TP PROBABILITY ENGINE")

    st.warning(
        "Historical testing engine is not implemented."
    )

    st.write("TP1 Probability: Not calculated")
    st.write("TP2 Probability: Not calculated")
    st.write("TP3 Probability: Not calculated")


# ---------------- RISK CALCULATOR ----------------

elif page == "Risk Calculator":

    st.title("RISK CALCULATOR")

    st.info(
        "Educational calculator only. "
        "It does not recommend or execute trades."
    )

    balance = st.number_input(
        "Example Balance ($)",
        min_value=1.0,
        value=1000.0
    )

    percentage = st.slider(
        "Example Percentage",
        0.1,
        2.0,
        1.0,
        0.1
    )

    amount = balance * percentage / 100

    st.metric(
        "Illustrative Amount",
        f"${amount:.2f}"
    )


# ---------------- SETTINGS ----------------

elif page == "Settings":

    st.title("⚙️ SETTINGS")

    st.write("Market: BTC/USD")
    st.write("Data Provider: Coinbase")
    st.write("Trading Mode: SIGNAL ONLY")
    st.write("Automatic Execution: DISABLED")

    st.success("Dashboard configuration loaded.")


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "ICT SMART AI | EDUCATIONAL MARKET DASHBOARD | "
    "NO AUTOMATIC TRADING"
)
