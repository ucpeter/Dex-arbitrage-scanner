from web3 import Web3
from app.dex.base import DexBase
from app.models.token import Token

FACTORY_ABI = [
    {
        "name": "getPair",
        "outputs": [{"type": "address", "name": "pair"}],
        "inputs": [
            {"type": "address", "name": "tokenA"},
            {"type": "address", "name": "tokenB"},
        ],
        "stateMutability": "view",
        "type": "function",
    }
]

PAIR_ABI = [
    {
        "name": "getReserves",
        "outputs": [
            {"type": "uint112", "name": "reserve0"},
            {"type": "uint112", "name": "reserve1"},
            {"type": "uint32", "name": "blockTimestampLast"},
        ],
        "inputs": [],
        "stateMutability": "view",
        "type": "function",
    },
    {"name": "token0", "outputs": [{"type": "address"}], "inputs": [], "stateMutability": "view", "type": "function"},
    {"name": "token1", "outputs": [{"type": "address"}], "inputs": [], "stateMutability": "view", "type": "function"},
]


class UniswapV2Dex(DexBase):

    def __init__(self, web3, chain, dex_name, factory_address):
        super().__init__(web3, chain)
        self._name = dex_name
        self.factory = web3.eth.contract(
            address=Web3.to_checksum_address(factory_address),
            abi=FACTORY_ABI,
        )

    def dex_name(self):
        return self._name

    def get_pair_address(self, token_a: Token, token_b: Token):
        pair = self.factory.functions.getPair(token_a.address, token_b.address).call()
        if int(pair, 16) == 0:
            return None
        return Web3.to_checksum_address(pair)

    def get_reserves(self, pair_address):
        pair = self.web3.eth.contract(address=pair_address, abi=PAIR_ABI)
        r0, r1, _ = pair.functions.getReserves().call()
        return {
            "r0": r0,
            "r1": r1,
            "t0": pair.functions.token0().call(),
            "t1": pair.functions.token1().call(),
        }

    def compute_price(self, token_in, token_out, r):
        if token_in.address == r["t0"]:
            return r["r1"] / r["r0"]
        return r["r0"] / r["r1"]

    def estimate_liquidity_usd(self, token_in, token_out, r):
        return min(r["r0"], r["r1"])
