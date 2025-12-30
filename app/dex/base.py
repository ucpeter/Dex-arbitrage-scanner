from abc import ABC, abstractmethod
from web3 import Web3
from app.models.token import Token
from app.models.price import PriceSnapshot
from datetime import datetime


class DexBase(ABC):

    def __init__(self, web3: Web3, chain: str):
        self.web3 = web3
        self.chain = chain

    @abstractmethod
    def dex_name(self) -> str:
        pass

    @abstractmethod
    def get_pair_address(self, token_a: Token, token_b: Token):
        pass

    @abstractmethod
    def get_reserves(self, pair_address: str):
        pass

    @abstractmethod
    def compute_price(self, token_in: Token, token_out: Token, reserves):
        pass

    @abstractmethod
    def estimate_liquidity_usd(self, token_in: Token, token_out: Token, reserves):
        pass

    def get_price_snapshot(self, token_in: Token, token_out: Token):
        pair = self.get_pair_address(token_in, token_out)
        if not pair:
            return None

        reserves = self.get_reserves(pair)
        price = self.compute_price(token_in, token_out, reserves)
        if price <= 0:
            return None

        liquidity = self.estimate_liquidity_usd(token_in, token_out, reserves)

        return PriceSnapshot(
            chain=self.chain,
            dex=self.dex_name(),
            token_in=token_in,
            token_out=token_out,
            price=price,
            liquidity_usd=liquidity,
            timestamp=datetime.utcnow(),
        )
