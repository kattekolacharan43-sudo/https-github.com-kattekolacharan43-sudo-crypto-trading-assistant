from __future__ import annotations

from typing import Dict, List, Tuple

from .market import get_market_data, normalize_symbol


def _trend_from_change(change_24h: float) -> str:
    if change_24h > 0.03:
        return "uptrend"
    if change_24h < -0.03:
        return "downtrend"
    return "ranging"


def _probability_for_bias(bias: str) -> int:
    if bias == "bullish":
        return 68
    if bias == "bearish":
        return 66
    return 52


def _entry_levels(price: float) -> Tuple[float, float, float]:
    return (round(price * 0.99, 6 if price < 1 else 2), round(price, 6 if price < 1 else 2), round(price * 1.01, 6 if price < 1 else 2))


def _stop_loss(price: float, trend: str) -> float:
    factor = 0.03 if trend == "uptrend" else 0.04
    return round(price * (1 - factor) if trend != "downtrend" else price * (1 + factor), 6 if price < 1 else 2)


def _take_profit_levels(price: float, trend: str) -> Tuple[float, float, float]:
    if trend == "downtrend":
        return (
            round(price * (1 + 0.01), 6 if price < 1 else 2),
            round(price * (1 + 0.025), 6 if price < 1 else 2),
            round(price * (1 + 0.05), 6 if price < 1 else 2),
        )
    return (
        round(price * (1 - 0.01), 6 if price < 1 else 2),
        round(price * (1 - 0.025), 6 if price < 1 else 2),
        round(price * (1 - 0.05), 6 if price < 1 else 2),
    )


def _bias_from_market(price: float, support: float, resistance: float, change_24h: float) -> str:
    if price > resistance * 0.995:
        return "bullish"
    if price < support * 1.005:
        return "bearish"
    if change_24h > 0.01:
        return "bullish"
    if change_24h < -0.01:
        return "bearish"
    return "neutral"


def _market_structure(price: float, support: float, resistance: float) -> Dict[str, object]:
    return {
        "trend": _trend_from_change((price - support) / support * 100 if support else 0),
        "higher_high": round(resistance, 6 if resistance < 1 else 2),
        "lower_low": round(support, 6 if support < 1 else 2),
        "break_of_structure": price > resistance * 0.995 or price < support * 1.005,
    }


def analyze_pair(symbol: str, timeframe: str = "4h") -> Dict[str, object]:
    """Generate a complete trade analysis object for a symbol."""
    normalized = normalize_symbol(symbol)
    snapshot = get_market_data(normalized)
    base = snapshot["market_summary"]
    price = float(base["price"])
    support = float(base["support"])
    resistance = float(base["resistance"])
    change_24h = float(base["change_24h"])
    trend = _trend_from_change(change_24h)
    bias = _bias_from_market(price, support, resistance, change_24h)
    entry_points = _entry_levels(price)
    stop_loss = _stop_loss(price, trend)
    take_profit = _take_profit_levels(price, trend)
    market_structure = _market_structure(price, support, resistance)
    order_block = (round(price * 0.985, 6 if price < 1 else 2), round(price * 0.995, 6 if price < 1 else 2))
    fair_value_gap = (round(price * 0.99, 6 if price < 1 else 2), round(price * 1.01, 6 if price < 1 else 2))
    ote = (round(price * (1 - 0.382), 6 if price < 1 else 2), round(price * (1 - 0.618), 6 if price < 1 else 2))

    return {
        "symbol": normalized,
        "timeframe": timeframe,
        "market_data": snapshot,
        "analysis": {
            "trend": trend,
            "market_structure": market_structure,
            "smc": {
                "order_block": order_block,
                "fair_value_gap": fair_value_gap,
                "liquidity_sweep_detected": change_24h > 0.02 or change_24h < -0.02,
            },
            "ict": {
                "premium_discount_zone": "premium" if bias == "bullish" else "discount" if bias == "bearish" else "balanced",
                "ote": ote,
                "optimal_trade_entry": "buy zone" if bias == "bullish" else "sell zone" if bias == "bearish" else "wait for confirmation",
            },
            "risk_management": {
                "stop_loss": stop_loss,
                "take_profit": list(take_profit),
                "risk_reward_ratio": "1:2.5",
            },
            "probability": {
                "bullish": _probability_for_bias("bullish") if bias == "bullish" else 42,
                "bearish": _probability_for_bias("bearish") if bias == "bearish" else 38,
                "neutral": 20,
            },
            "confluence": [
                "trend alignment",
                "support and resistance reaction",
                "supply/demand zone",
                "volume confirmation",
            ],
        },
        "trade_setup": {
            "bias": bias,
            "entry_points": list(entry_points),
            "stop_loss": stop_loss,
            "take_profit": list(take_profit),
            "risk_reward": 2.5,
            "position_sizing": "2% portfolio risk",
        },
    }


def generate_trade_setup(symbol: str, timeframe: str = "4h") -> Dict[str, object]:
    """Return the concise trade setup output for a pair."""
    payload = analyze_pair(symbol, timeframe=timeframe)
    return payload["trade_setup"]


def analyze_market(symbol: str, timeframe: str = "4h") -> Dict[str, object]:
    """Compatibility alias for analyze_pair."""
    return analyze_pair(symbol, timeframe=timeframe)
