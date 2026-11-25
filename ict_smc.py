import pandas as pd


def analyze_market(df):
    """
    Educational ICT + SMC market analysis.
    Required columns: open, high, low, close
    """

    required = ["open", "high", "low", "close"]

    if not all(col in df.columns for col in required):
        return {"Error": "OHLC candle data missing"}

    if len(df) < 20:
        return {"Status": "Not enough candle data"}

    df = df.copy().reset_index(drop=True)

    # Swing highs and lows
    df["swing_high"] = (
        (df["high"] > df["high"].shift(1)) &
        (df["high"] > df["high"].shift(-1))
    )

    df["swing_low"] = (
        (df["low"] < df["low"].shift(1)) &
        (df["low"] < df["low"].shift(-1))
    )

    latest = df.iloc[-1]

    previous_highs = df.loc[df["swing_high"], "high"]
    previous_lows = df.loc[df["swing_low"], "low"]

    bos = "Not detected"
    choch = "Not detected"

    # Market structure
    if len(previous_highs) > 0:
        if latest["close"] > previous_highs.iloc[-1]:
            bos = "Bullish BOS"

    if len(previous_lows) > 0:
        if latest["close"] < previous_lows.iloc[-1]:
            bos = "Bearish BOS"

    # Fair Value Gap
    fvg = "Not detected"

    if latest["low"] > df.iloc[-3]["high"]:
        fvg = "Bullish FVG"

    elif latest["high"] < df.iloc[-3]["low"]:
        fvg = "Bearish FVG"

    # Liquidity sweep
    liquidity = "Not detected"

    recent = df.iloc[-10:-1]

    if (
        latest["high"] > recent["high"].max()
        and latest["close"] < recent["high"].max()
    ):
        liquidity = "Buy-side liquidity sweep"

    elif (
        latest["low"] < recent["low"].min()
        and latest["close"] > recent["low"].min()
    ):
        liquidity = "Sell-side liquidity sweep"

    # Simple order block approximation
    order_block = "Not detected"

    if latest["close"] > latest["open"]:
        previous = df.iloc[-2]

        if previous["close"] < previous["open"]:
            order_block = "Potential Bullish Order Block"

    elif latest["close"] < latest["open"]:
        previous = df.iloc[-2]

        if previous["close"] > previous["open"]:
            order_block = "Potential Bearish Order Block"

    return {
        "Market Structure": bos,
        "CHoCH": choch,
        "Fair Value Gap": fvg,
        "Liquidity Sweep": liquidity,
        "Order Block": order_block,
        "Analysis": "Educational analysis only"
    }
