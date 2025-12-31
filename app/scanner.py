import time
import os
import json
from datetime import datetime
from web3 import Web3
from requests.exceptions import HTTPError

from app.config import SCAN_INTERVAL, MIN_PROFIT_PCT, ETH_RPC_URL
from app.dex.uniswap_v2 import UniswapV2
from app.dex.sushiswap import SushiSwap
from app.models.arbitrage import ArbitrageOpportunity


OUTPUT_FILE = "scan_results.json"


def init_web3():
    if not ETH_RPC_URL:
        raise RuntimeError("ETH_RPC_URL is not set")

    w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))

    if not w3.is_connected():
        raise RuntimeError("Failed to connect to Ethereum RPC")

    return w3


def safe_rpc_call(fn, retries=5, delay=15):
    """
    Prevents scanner crash due to RPC rate limits.
    """
    for attempt in range(retries):
        try:
            return fn()
        except HTTPError as e:
            if e.response is not None and e.response.status_code == 429:
                print(f"[RPC] Rate limited (429). Sleeping {delay}s...")
                time.sleep(delay)
            else:
                raise
        except Exception as e:
            print(f"[RPC] Error: {e}. Sleeping {delay}s...")
            time.sleep(delay)

    print("[RPC] Max retries exceeded. Backing off.")
    time.sleep(delay * 2)
    return None


def save_results(results):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "count": len(results),
        "results": [r.to_dict() for r in results],
    }
    with open(OUTPUT_FILE, "w") as f:
        json.dump(payload, f, indent=2)


def run_scan():
    print("[INIT] Initializing Web3...")
    w3 = init_web3()

    chain_id = safe_rpc_call(lambda: w3.eth.chain_id)
    if not chain_id:
        return

    print(f"[INIT] Connected to chain_id={chain_id}")

    uniswap = UniswapV2(w3)
    sushi = SushiSwap(w3)

    print("[SCAN] Fetching prices...")
    prices_uni = safe_rpc_call(uniswap.get_prices)
    prices_sushi = safe_rpc_call(sushi.get_prices)

    if not prices_uni or not prices_sushi:
        print("[SCAN] Price fetch failed, skipping round")
        return

    opportunities = ArbitrageOpportunity.find(
        prices_uni,
        prices_sushi,
        min_profit_pct=MIN_PROFIT_PCT,
    )

    if opportunities:
        for op in opportunities:
            print(
                f"[ARBITRAGE] {op.token.symbol} | "
                f"Buy {op.buy_exchange} @ {op.buy_price} → "
                f"Sell {op.sell_exchange} @ {op.sell_price} | "
                f"Profit {op.profit_pct:.2f}%"
            )
        save_results(opportunities)
    else:
        print("[SCAN] No arbitrage found")


def main():
    print("[START] Arbitrage scanner started")

    while True:
        try:
            run_scan()
        except Exception as e:
            print("[FATAL] Unexpected error:", e)

        print(f"[SLEEP] Sleeping {SCAN_INTERVAL}s\n")
        time.sleep(SCAN_INTERVAL)


if __name__ == "__main__":
    main()
