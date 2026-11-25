import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timezone

st.set_page_config(
    page_title="ICT SMART AI BOT",
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

API = "https://api.coinbase.com"

TIMEFRAMES = {
    "1m": "1m",
    "3m": "3m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1H": "1h",
    "2H": "2h",
    "4H": "4h",
    "Daily": "1d",
    "Weekly": "1w"
}

@st.cache_data(ttl=30)
@st.cache_data(ttl=30)
def get_price():
    response = requests.get(
        "https://api.coinbase.com/v2/prices/BTC-USD/spot",
        timeout=10
    )
    response.raise_for_status()
    return float(response.json()["data"]["amount"])

@st.cache_data(ttl=30)
@st.cache_data(ttl=30)
def get_candles(interval):

    granularity = {
        "1m": 60,
        "5m": 300,
        "15m": 900,
        "1h": 3600,
        "1d": 86400
    }

    if interval not in granularity:
        raise ValueError(
            f"Coinbase par {interval} timeframe abhi supported nahi."
        )

    response = requests.get(
        "https://api.exchange.coinbase.com/products/BTC-USD/candles",
        params={"granularity": granularity[interval]},
        timeout=15
    )

    response.raise_for_status()
    data = response.json()

    df = pd.DataFrame(
        data,
        columns=["time", "low", "high", "open", "close", "volume"]
    )

    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = pd.to_numeric(df[col])

    df["time"] = pd.to_datetime(
        df["time"], unit="s", utc=True
    )

    df = df.sort_values("time").reset_index(drop=True)

    return df


st.title("⚡ ICT SMART AI TRADING BOT")

st.caption(
    "ICT + SMC | QUALITY OVER QUANTITY | "
    "MANUAL EXECUTION ONLY"
)

st.divider()

page = st.sidebar.selectbox(
    "NAVIGATION",
    [
        "Home",
        "BTC Signals",
        "Gold Signals",
        "Live Chart",
        "Backtesting",
        "Historical Probabilities",
        "Trade History",
        "Risk Calculator",
        "Settings"
    ]
)

st.sidebar.markdown("### ACCOUNT SETTINGS")
st.sidebar.write("Balance: $1,000")
st.sidebar.write("Preferred Risk: 1%")
st.sidebar.write("Maximum Risk: 2%")
st.sidebar.write("Daily Limit: 5")

def bitcoin_dashboard():

    st.subheader("₿ BITCOIN MARKET DATA")

    try:

        price = get_price()

        st.success("BINANCE CONNECTION: SUCCESS")

        st.metric(
            "BTC/USDT CURRENT PRICE",
            f"${price:,.2f}"
        )

        st.caption(
            "Source: Binance Public API | "
            "Fetched: " +
            datetime.now(timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S UTC"
            )
        )

    except Exception as e:

        st.error("BINANCE DATA UNAVAILABLE")
        st.write(str(e))
        st.warning("NO DATA — No verified price available.")
        return

    st.divider()

    timeframe = st.selectbox(
        "Select Timeframe",
        list(TIMEFRAMES.keys())
    )

    try:

        df = get_candles(TIMEFRAMES[timeframe])

        st.success("HISTORICAL CANDLES: CONNECTED")

        st.write(
            "Latest candle timestamp (UTC):",
            df.iloc[-1]["time"].strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        fig = go.Figure(data=[
            go.Candlestick(
                x=df["time"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="BTC/USDT"
            )
        ])

        fig.update_layout(
            template="plotly_dark",
            height=500,
            title=f"BTC/USDT — {timeframe}",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("LATEST MARKET CANDLES")

        st.dataframe(
            df[["time", "open", "high", "low",
                "close", "volume"]].tail(10),
            use_container_width=True
        )

        st.info(
            "Candles include historical data and may "
            "include the currently forming candle."
        )

    except Exception as e:

        st.error("CANDLE DATA UNAVAILABLE")
        st.write(str(e))


if page == "Home":

    st.subheader("📊 MARKET OVERVIEW")

    a, b = st.columns(2)

    with a:
        st.metric("Account Balance", "$1,000")
        st.metric("Preferred Risk", "1%")

    with b:
        st.metric("Maximum Risk", "2%")
        st.metric("Daily Signal Limit", "5")

    st.divider()

    bitcoin_dashboard()

    st.divider()

    st.warning(
        "NO TRADE — ICT/SMC confirmation engine "
        "is not implemented yet."
    )


elif page == "BTC Signals":

    st.title("₿ BTC MARKET ANALYSIS")

    bitcoin_dashboard()

    st.warning(
        "Market data only. No confirmed trading signal."
    )


elif page == "Gold Signals":

    st.title("🥇 GOLD ANALYSIS")

    st.warning(
        "NO TRADE — Authorized COMEX data not connected."
    )


elif page == "Live Chart":

    st.title("📈 LIVE MARKET CHART")

    bitcoin_dashboard()


elif page == "Backtesting":

    st.title("BACKTESTING ENGINE")

    st.warning("INSUFFICIENT DATA")

    st.write("Win Rate: Not calculated")
    st.write("Profit Factor: Not calculated")
    st.write("Maximum Drawdown: Not calculated")


elif page == "Historical Probabilities":

    st.title("TP PROBABILITY ENGINE")

    st.warning("INSUFFICIENT DATA")

    st.write("TP1: Not calculated")
    st.write("TP2: Not calculated")
    st.write("TP3: Not calculated")


elif page == "Trade History":

    st.title("TRADE HISTORY")

    st.info("No paper trades recorded yet.")


elif page == "Risk Calculator":

    st.title("RISK CALCULATOR")

    balance = st.number_input(
        "Account Balance ($)",
        min_value=1.0,
        value=1000.0
    )

    risk = st.slider(
        "Risk Percentage",
        0.1,
        2.0,
        1.0,
        0.1
    )

    st.metric(
        "Illustrative Risk Amount",
        f"${balance * risk / 100:.2f}"
    )

    st.info(
        "Structural SL and position sizing "
        "engine are not implemented yet."
    )


elif page == "Settings":

    st.title("⚙️ SETTINGS")

    st.write("Starting Balance: $1,000")
    st.write("Preferred Risk: 1%")
    st.write("Maximum Risk: 2%")
    st.write("Trading Mode: SIGNAL ONLY")
    st.write("Automatic Execution: DISABLED")


st.divider()

st.markdown(
    "QUALITY OVER QUANTITY | "
    "NO FORCED TRADES | "
    "MANUAL EXECUTION ONLY"
)

st.caption(
    "Educational market-data dashboard. "
    "Public Binance API. No trading orders."
)
