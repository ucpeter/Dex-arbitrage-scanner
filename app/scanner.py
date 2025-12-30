from web3 import Web3
from app.config import RPC_ENDPOINTS, DEX_CONFIGS, SCAN_MIN_PROFIT_PCT, DEX_TRADING_FEE_PCT
from app.dex.uniswap_v2 import UniswapV2Dex
from app.models.token_registry import TOKENS_BY_CHAIN
from app.models.arbitrage import find_cross_dex_arbitrage


def run_scan():
    for chain, rpc in RPC_ENDPOINTS.items():
        web3 = Web3(Web3.HTTPProvider(rpc))
        if not web3.is_connected():
            continue

        tokens = TOKENS_BY_CHAIN.get(chain, [])
        dexes = [
            UniswapV2Dex(web3, chain, d["name"], d["factory"])
            for d in DEX_CONFIGS
            if d["chain"] == chain
        ]

        prices = []
        for dex in dexes:
            for a in tokens:
                for b in tokens:
                    if a.symbol == b.symbol:
                        continue
                    snap = dex.get_price_snapshot(a, b)
                    if snap:
                        prices.append(snap)

        arbs = find_cross_dex_arbitrage(
            prices,
            min_profit_pct=SCAN_MIN_PROFIT_PCT,
            trading_fee_pct=DEX_TRADING_FEE_PCT,
        )

        for a in arbs:
            print(
                f"[{chain}] {a.token_in}/{a.token_out} "
                f"BUY {a.buy_dex} SELL {a.sell_dex} "
                f"NET {a.net_profit_pct:.2f}%"
            )


if __name__ == "__main__":
    run_scan()
