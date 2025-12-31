"""
Global configuration for the DEX arbitrage scanner.
"""

import os

# =========================
# RPC endpoints
# =========================

RPC_ENDPOINTS = {
    "ethereum": os.getenv("ETH_RPC_URL", "https://eth.llamarpc.com"),
    "polygon": os.getenv("POLYGON_RPC_URL", "https://polygon.llamarpc.com"),
    "bsc": os.getenv("BSC_RPC_URL", "https://bsc.llamarpc.com"),
    "arbitrum": os.getenv("ARBITRUM_RPC_URL", "https://arbitrum.llamarpc.com"),
}

# =========================
# DEX configurations
# =========================

DEX_CONFIGS = [
    # Ethereum
    {
        "chain": "ethereum",
        "name": "UniswapV2",
        "factory": "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f",
    },
    {
        "chain": "ethereum",
        "name": "SushiSwap",
        "factory": "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac",
    },

    # Polygon
    {
        "chain": "polygon",
        "name": "QuickSwap",
        "factory": "0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32",
    },

    # BSC
    {
        "chain": "bsc",
        "name": "PancakeSwap",
        "factory": "0xCA143Ce32Fe78f1f7019d7d551a6402fC5350c73",
    },

    # Arbitrum
    {
        "chain": "arbitrum",
        "name": "SushiSwap",
        "factory": "0xc35DADB65012eC5796536bD9864eD8773aBc74C4",
    },
]

# =========================
# Scanner parameters
# =========================

# ✅ REQUIRED by scanner.py
SCAN_INTERVAL = int(os.getenv("SCAN_INTERVAL", "30"))

# Alias to avoid import mismatch
MIN_PROFIT_PCT = float(os.getenv("MIN_PROFIT_PCT", "0.3"))

# Existing values (kept)
SCAN_MIN_PROFIT_PCT = MIN_PROFIT_PCT
DEX_TRADING_FEE_PCT = float(os.getenv("DEX_TRADING_FEE_PCT", "0.30"))
