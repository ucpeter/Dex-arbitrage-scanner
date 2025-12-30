from dataclasses import dataclass


@dataclass(frozen=True)
class Token:
    symbol: str
    address: str
    decimals: int
    chain: str
