"""
Furucombo calldata builder (human-readable version)

This does NOT execute trades.
It only explains and prepares the swap path clearly.
"""

from typing import Dict


def build_furucombo_plan(opportunity: Dict, flashloan_amount: float = 100_000):
    """
    Build a clear arbitrage execution plan for Furucombo

    :param opportunity: single scanner result
    :param flashloan_amount: amount of base token to borrow
    """

    network = opportunity["network"]
    pair = opportunity["pair"]          # e.g. USDC/WETH
    base_token, quote_token = pair.split("/")

    buy = opportunity["buy"]
    sell = opportunity["sell"]

    # We ALWAYS borrow the base token (USDC)
    flashloan_token = base_token

    plan = {
        "network": network,
        "flashloan": {
            "token": flashloan_token,
            "amount": flashloan_amount,
            "provider": "AaveV3"
        },
        "execution_path": [
            {
                "step": 1,
                "action": "BUY",
                "dex": buy["dex"],
                "from_token": base_token,
                "to_token": quote_token,
                "price": buy["price"]
            },
            {
                "step": 2,
                "action": "SELL",
                "dex": sell["dex"],
                "from_token": quote_token,
                "to_token": base_token,
                "price": sell["price"]
            }
        ],
        "expected_profit": {
            "gross_pct": opportunity["gross_profit_pct"],
            "net_pct": opportunity["net_profit_pct"]
        }
    }

    return plan
