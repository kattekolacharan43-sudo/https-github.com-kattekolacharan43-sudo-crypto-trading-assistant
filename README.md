# Crypto Trading Assistant

This repository contains a lightweight Python-based crypto trading assistant that can normalize trading symbols, simulate market snapshots across major exchanges, and generate a technical-analysis style trade setup for any supported pair.

## Included capabilities

- Automatic ticker normalization for formats like `BTCUSD`, `BTC/USD`, `btc-usd`
- Recognized major and emerging crypto pairs including BTC, ETH, SOL, XRP, BNB, DOGE, ADA, AVAX, LINK, SUI, APT, HYPE, PEPE, SHIB, TRX, TON, ZEC, and more
- Multi-exchange price snapshot generation for Binance, Kraken, Coinbase, and DEX references
- Trend, support/resistance, Smart Money Concepts, ICT-style setup estimation, and risk management outputs
- CLI usage for quick market analysis from the terminal

## Quick start

```bash
python app.py BTCUSD
python app.py ETHUSD --timeframe 1h
python -m crypto_trading_assistant BTCUSD
```

## Python API

```python
from crypto_trading_assistant import analyze_pair, generate_trade_setup, normalize_symbol

print(normalize_symbol("btc/usd"))
print(analyze_pair("SOLUSD", timeframe="4h"))
print(generate_trade_setup("PEPEUSD"))
```

## Notes

The current implementation is intentionally self-contained and works without external API keys or internet access. It is designed to provide a deterministic, testable market-analysis interface suitable for local development and benchmarking.
