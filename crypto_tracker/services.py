import requests
from typing import Dict, List, Optional
import json

class CryptoService:
    BASE_URL = "https://api.coingecko.com/api/v3"

    @classmethod
    def get_coin_price(cls, coin_id: str) -> Optional[Dict]:
        try:
            response = requests.get(
                f"{cls.BASE_URL}/simple/price",
                params={
                    "ids": coin_id,
                    "vs_currencies": "usd",
                    "include_24hr_change": "true"
                }
            )
            response.raise_for_status()
            data = response.json()
            print(f"CoinGecko price API response for {coin_id}: {data}")
            if coin_id in data:
                return {
                    "usd": data[coin_id]["usd"],
                    "usd_24h_change": data[coin_id].get("usd_24h_change", 0)
                }
            return None
        except requests.RequestException as e:
            print(f"Error fetching price data for {coin_id}: {e}")
            return None

    @classmethod
    def get_trending_coins(cls) -> List[Dict]:
        try:
            response = requests.get(f"{cls.BASE_URL}/search/trending")
            response.raise_for_status()
            data = response.json()
            print(f"CoinGecko trending API response: {data}")
            return data.get("coins", [])
        except requests.RequestException as e:
            print(f"Error fetching trending coins: {e}")
            return []

    @classmethod
    def get_coin_history(cls, coin_id: str, days: int = 7) -> Optional[Dict]:
        try:
            response = requests.get(
                f"{cls.BASE_URL}/coins/{coin_id}/market_chart",
                params={
                    "vs_currency": "usd",
                    "days": days
                }
            )
            response.raise_for_status()
            data = response.json()
            print(f"CoinGecko history API response for {coin_id} (last {days} days): {data}")
            return {
                "prices": data.get("prices", []),
                "market_caps": data.get("market_caps", []),
                "total_volumes": data.get("total_volumes", [])
            }
        except requests.RequestException as e:
            print(f"Error fetching history data for {coin_id}: {e}")
            return None 