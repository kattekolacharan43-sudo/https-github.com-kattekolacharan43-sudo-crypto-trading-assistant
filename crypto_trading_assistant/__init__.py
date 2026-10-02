from __future__ import annotations

from typing import Dict, List, Tuple
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
    """Normalize a user-entered ticker to a canonical uppercase symbol."""
    if symbol is None:
        raise ValueError("Ticker cannot be empty.")
    cleaned = re.sub(r"[^A-Za-z0-9]", "", str(symbol)).upper()
    if not cleaned:
        raise ValueError("Ticker could not be normalized.")
    if cleaned.endswith("USD"):
        return cleaned
    if cleaned.endswith("USDT"):
        return cleaned[:-4] + "USD"
    if cleaned.endswith("/USD"):
        return cleaned[:-4] + "USD"
    return cleaned if cleaned in SUPPORTED_SYMBOLS else cleaned + "USD"


def search_ticker(query: str, limit: int = 5) -> List[str]:
    """Return likely matches for a user query from the known symbol set."""
    if query is None or not str(query).strip():
        return []
    normalized = normalize_symbol(query)
    matches = []
    if normalized in SUPPORTED_SYMBOLS:
        matches.append(normalized)

    for symbol in SUPPORTED_SYMBOLS:
        if symbol.startswith(normalized[: min(3, len(normalized))]) or normalized in symbol:
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


def _market_snapshot_for_symbol(symbol: str) -> Dict[str, float]:
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
    """Return a synthetic but deterministic market snapshot across multiple exchanges."""
    normalized = normalize_symbol(symbol)
    price_info = _market_snapshot_for_symbol(normalized)
    exchange_prices = {}
    for name in EXCHANGES:
        multiplier = 1.0 + ((abs(_stable_seed(f"{normalized}:{name}") % 250) - 125) / 10000.0)
        exchange_prices[name] = round(price_info["price"] * multiplier, 6 if price_info["price"] < 1 else 2)

    return {
        "symbol": normalized,
        "market_summary": {
            "price": price_info["price"],
            "change_24h": price_info["change_24h"],
            "volume": price_info["volume"],
            "support": price_info["support"],
            "resistance": price_info["resistance"],
        },
        "exchange_prices": exchange_prices,
        "exchanges": EXCHANGES,
    }
