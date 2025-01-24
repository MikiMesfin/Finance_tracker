import requests
from django.core.cache import cache
from decimal import Decimal

def get_exchange_rate(from_currency, to_currency):
    cache_key = f'rate_{from_currency}_{to_currency}'
    rate = cache.get(cache_key)
    
    if not rate:
        # Using a free currency API (you'll need to sign up for an API key)
        response = requests.get(
            f'https://api.exchangerate-api.com/v4/latest/{from_currency}'
        )
        data = response.json()
        rate = Decimal(str(data['rates'][to_currency]))
        cache.set(cache_key, rate, 3600)  # Cache for 1 hour
    
    return rate
