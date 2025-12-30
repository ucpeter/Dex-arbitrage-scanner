from dataclasses import dataclass
from typing import List
from datetime import datetime
from app.models.price import PriceSnapshot


@dataclass(frozen=True)
class ArbitrageOpportunity:
    chain: str
    token_in: str
    token_out: str
    buy_dex: str
    sell_dex: str
    buy_price: float
    sell_price: float
    gross_profit_pct: float
    net_profit_pct: float
    liquidity_usd: float
    timestamp: datetime


def find_cross_dex_arbitrage(
    prices: List[PriceSnapshot],
    *,
    min_profit_pct: float,
    trading_fee_pct: float,
) -> List[ArbitrageOpportunity]:

    markets = {}
    for p in prices:
        key = (p.chain, p.token_in.symbol, p.token_out.symbol)
        markets.setdefault(key, []).append(p)

    results = []

    for (chain, token_in, token_out), snaps in markets.items():
        if len(snaps) < 2:
            continue

        for buy in snaps:
            for sell in snaps:
                if buy.dex == sell.dex:
                    continue
                if buy.price >= sell.price:
                    continue

                gross = ((sell.price - buy.price) / buy.price) * 100
                net = gross - (trading_fee_pct * 2)

                if net < min_profit_pct:
                    continue

                results.append(
                    ArbitrageOpportunity(
                        chain=chain,
                        token_in=token_in,
                        token_out=token_out,
                        buy_dex=buy.dex,
                        sell_dex=sell.dex,
                        buy_price=buy.price,
                        sell_price=sell.price,
                        gross_profit_pct=round(gross, 4),
                        net_profit_pct=round(net, 4),
                        liquidity_usd=min(buy.liquidity_usd, sell.liquidity_usd),
                        timestamp=min(buy.timestamp, sell.timestamp),
                    )
                )

    return sorted(results, key=lambda x: x.net_profit_pct, reverse=True)
