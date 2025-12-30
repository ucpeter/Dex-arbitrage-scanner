from dataclasses import dataclass
from datetime import datetime
from app.models.token import Token


@dataclass(frozen=True)
class PriceSnapshot:
    chain: str
    dex: str
    token_in: Token
    token_out: Token
    price: float
    liquidity_usd: float
    timestamp: datetime
