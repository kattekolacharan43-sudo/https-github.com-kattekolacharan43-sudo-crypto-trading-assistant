from __future__ import annotations

import argparse
import json

from crypto_trading_assistant import analyze_pair


def main() -> None:
    parser = argparse.ArgumentParser(description="Advanced AI Crypto Trading Assistant")
    parser.add_argument("symbol", nargs="?", default="BTCUSD", help="Trading pair to analyze")
    parser.add_argument("--timeframe", default="4h", help="Timeframe for analysis (default: 4h)")
    args = parser.parse_args()
    payload = analyze_pair(args.symbol, timeframe=args.timeframe)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
