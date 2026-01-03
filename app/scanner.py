import json
from.tokens import TOKENS
from.config import MIN_GROSS_PROFIT_PCT, ESTIMATED_GAS_PCT, OUTPUT_FILE
from.uniswap_v3 import get_uniswap_price
from.paraswap_v5 import get_paraswap_price

def scan(network):
    results = []

    token_list = TOKENS.get(network, [])
    base = "WETH"

    for token in token_list:
        if token == base:
            continue

        uni_price = get_uniswap_price(network, token, base)
        para_price = get_paraswap_price(network, token, base)

        if not uni_price or not para_price:
            continue

        buy_dex, sell_dex = None, None
        buy_price, sell_price = None, None

        if uni_price < para_price:
            buy_dex, sell_dex = "UniswapV3", "ParaswapV5"
            buy_price, sell_price = uni_price, para_price
        elif para_price < uni_price:
            buy_dex, sell_dex = "ParaswapV5", "UniswapV3"
            buy_price, sell_price = para_price, uni_price
        else:
            continue

        gross_pct = ((sell_price - buy_price) / buy_price) * 100
        net_pct = gross_pct - ESTIMATED_GAS_PCT

        if gross_pct >= MIN_GROSS_PROFIT_PCT:
            results.append({
                "network": network,
                "pair": f"{token}/{base}",
                "buy": {
                    "token": token,
                    "dex": buy_dex,
                    "price": buy_price
                },
                "sell": {
                    "token": token,
                    "dex": sell_dex,
                    "price": sell_price
                },
                "gross_profit_pct": round(gross_pct, 2),
                "net_profit_pct": round(net_pct, 2)
            })

    return results


def run_scan(network):
    data = scan(network)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Scan complete — {len(data)} opportunities found.")
