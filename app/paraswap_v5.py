import requests

PARASWAP_API = "https://apiv5.paraswap.io/prices"

def get_paraswap_price(network, src, dest):
    """
    Minimal Paraswap v5 price query
    """
    params = {
        "srcToken": src,
        "destToken": dest,
        "amount": 10**18,
        "network": network,
    }
    try:
        r = requests.get(PARASWAP_API, params=params, timeout=10)
        data = r.json()
        return float(data["priceRoute"]["destAmount"]) / 1e18
    except Exception:
        return None
