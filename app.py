from __future__ import annotations

from typing import Dict, List
import re

SUPPORTED_SYMBOLS = {
    "BTCUSD": "BTCUSD",
    "ETHUSD": "ETHUSD",
    "SOLUSD": "SOLUSD",
    "XRPUSD": "XRPUSD",
    "BNBUSD": "BNBUSD",
    "DOGEUSD": "DOGEUSD",
    "ADAUSD": "ADAUSD",
    "AVAXUSD": "AVAXUSD",
    "LINKUSD": "LINKUSD",
    "SUIUSD": "SUIUSD",
    "APTUSD": "APTUSD",
    "HYPEUSD": "HYPEUSD",
    "PEPEUSD": "PEPEUSD",
    "SHIBUSD": "SHIBUSD",
    "TRXUSD": "TRXUSD",
    "TONUSD": "TONUSD",
    "ZECUSD": "ZECUSD",
    "BUSD": "BUSD",
    "MUSD": "MUSD",
    "DEEPUSD": "DEEPUSD",
    "LITUSD": "LITUSD",
    "AINUSD": "AINUSD",
    "EVAAUSD": "EVAAUSD",
    "BEATUSD": "BEATUSD",
    "AIGENSYNUSD": "AIGENSYNUSD",
    "VVVUSD": "VVVUSD",
    "SIRENUSD": "SIRENUSD",
    "SKYIAUSD": "SKYIAUSD",
    "BLESSUSD": "BLESSUSD",
}

EXCHANGES = ["Binance", "Kraken", "Coinbase", "DEX"]


def normalize_symbol(symbol: str) -> str:
    """Normalize user-provided pair strings into uppercase canonical symbol names."""
    if symbol is None:
        raise ValueError("Ticker cannot be empty.")
    cleaned = re.sub(r"[^A-Za-z0-9]", "", str(symbol)).upper()
    if not cleaned:
        raise ValueError("Ticker could not be normalized.")
    if cleaned.endswith("USD"):
        return cleaned
    if cleaned.endswith("USDT"):
        return cleaned[:-4] + "USD"
    if cleaned in SUPPORTED_SYMBOLS:
        return SUPPORTED_SYMBOLS[cleaned]
    return cleaned + "USD"


def search_ticker(query: str, limit: int = 5) -> List[str]:
    """Return suggested tickers based on a query."""
    if not query or not str(query).strip():
        return []
    q = normalize_symbol(query)
    matches = []
    if q in SUPPORTED_SYMBOLS:
        matches.append(q)
    for symbol in sorted(SUPPORTED_SYMBOLS):
        if q[: min(3, len(q))] and (symbol.startswith(q[:3]) or q in symbol):
            matches.append(symbol)
        if len(matches) >= limit:
            break
    seen = set()
    ordered = []
    for symbol in matches:
        if symbol not in seen:
            ordered.append(symbol)
            seen.add(symbol)
    return ordered


def _stable_seed(value: str) -> int:
    total = 0
    for idx, char in enumerate(value.upper()):
        total += (idx + 1) * ord(char)
    return total


def _price_profile(symbol: str) -> Dict[str, float]:
    seed = _stable_seed(symbol)
    base = 100.0
    if symbol.startswith("BTC"):
        base = 60000.0
    elif symbol.startswith("ETH"):
        base = 3500.0
    elif symbol.startswith("SOL"):
        base = 150.0
    elif symbol.startswith("XRP"):
        base = 0.75
    elif symbol.startswith("BNB"):
        base = 600.0
    elif symbol.startswith("DOGE"):
        base = 0.18
    elif symbol.startswith("PEPE"):
        base = 0.00002
    elif symbol.startswith("SHIB"):
        base = 0.00003
    elif symbol.startswith("APT"):
        base = 7.5
    elif symbol.startswith("HYPE"):
        base = 17.0
    elif symbol.startswith("TRX"):
        base = 0.12
    elif symbol.startswith("TON"):
        base = 6.5
    else:
        base = max(0.05, (seed % 1000) / 10.0)

    price = base * (1 + ((seed % 1000) / 5000.0))
    change_24h = ((seed % 180) - 90) / 100.0
    volume = base * 1000000 * (1 + ((seed % 400) / 1000.0))
    support = price * (1 - (((seed % 20) + 10) / 1000.0))
    resistance = price * (1 + (((seed % 20) + 10) / 1000.0))
    return {
        "price": round(price, 6 if price < 1 else 2),
        "change_24h": round(change_24h, 4),
        "volume": round(volume, 2),
        "support": round(support, 6 if support < 1 else 2),
        "resistance": round(resistance, 6 if resistance < 1 else 2),
    }


def get_market_data(symbol: str) -> Dict[str, object]:
    """Return a synthetic multi-exchange market snapshot for a symbol."""
    normalized = normalize_symbol(symbol)
    profile = _price_profile(normalized)
    exchange_prices = {}
    for exchange in EXCHANGES:
        multiplier = 1.0 + ((abs(_stable_seed(f"{normalized}:{exchange}") % 250) - 125) / 10000.0)
        exchange_prices[exchange] = round(profile["price"] * multiplier, 6 if profile["price"] < 1 else 2)
    return {
        "symbol": normalized,
        "market_summary": {
            "price": profile["price"],
            "change_24h": profile["change_24h"],
            "volume": profile["volume"],
            "support": profile["support"],
            "resistance": profile["resistance"],
        },
        "exchange_prices": exchange_prices,
        "exchanges": EXCHANGES,
    }
