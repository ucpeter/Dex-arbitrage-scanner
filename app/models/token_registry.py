from typing import Dict, List
from app.models.token import Token

TOKENS_BY_CHAIN: Dict[str, List[Token]] = {
    "ethereum": [
        Token("USDC", "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", 6, "ethereum"),
        Token("USDT", "0xdAC17F958D2ee523a2206206994597C13D831ec7", 6, "ethereum"),
        Token("WETH", "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", 18, "ethereum"),
        Token("DAI", "0x6B175474E89094C44Da98b954EedeAC495271d0F", 18, "ethereum"),
    ],
    "polygon": [
        Token("USDC", "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", 6, "polygon"),
        Token("USDT", "0xc2132D05D31c914a87C6611C10748AaCBf1EFA90", 6, "polygon"),
        Token("WETH", "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619", 18, "polygon"),
    ],
    "bsc": [
        Token("USDT", "0x55d398326f99059fF775485246999027B3197955", 18, "bsc"),
        Token("WBNB", "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c", 18, "bsc"),
    ],
    "arbitrum": [
        Token("USDC", "0xaf88d065e77c8cC2239327C5EDb3A432268e5831", 6, "arbitrum"),
        Token("WETH", "0x82af49447d8a07e3bd95bd0d56f35241523fbab1", 18, "arbitrum"),
    ],
}
