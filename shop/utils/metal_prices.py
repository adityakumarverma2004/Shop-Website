import requests
import logging
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

def get_live_metal_prices():
    # Try to get from cache first
    cached_prices = cache.get('live_metal_prices')
    if cached_prices:
        return cached_prices

    api_key = getattr(settings, 'METALS_DEV_API_KEY', None)
    if not api_key:
        logger.warning("METALS_DEV_API_KEY is not set in settings.")
        return _get_fallback_prices()

    # The API returns 1 gram of gold/silver in INR when currency=INR and unit=g
    url = f"https://api.metals.dev/v1/latest?api_key={api_key}&currency=INR&unit=g"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('status') == 'success':
            metals = data.get('metals', {})
            
            # Gold price per gram
            gold_per_gram = metals.get('ibja_gold', metals.get('gold', 0))
            
            # Silver price per gram
            silver_per_gram = metals.get('mcx_silver', metals.get('silver', 0))

            if gold_per_gram and silver_per_gram:
                prices = {
                    'gold_24k_10g': round(gold_per_gram * 10),
                    # 22k is approx 91.6% purity
                    'gold_22k_10g': round(gold_per_gram * 10 * 0.916),
                    # 18k is approx 75% purity
                    'gold_18k_10g': round(gold_per_gram * 10 * 0.750),
                    # Silver is usually sold per 1kg volume in India
                    'silver_1kg': round(silver_per_gram * 1000)
                }
                
                # Cache for 8 hours (28800 seconds) 
                # This ensures we don't hit the 100 requests/month free limit (max ~90 requests/month if requested exactly every 8 hrs)
                cache.set('live_metal_prices', prices, 28800)
                return prices
    except Exception as e:
        logger.error(f"Failed to fetch live metal prices: {e}")

    return _get_fallback_prices()

def _get_fallback_prices():
    # Fallback to realistic data in case the API is fully depleted or fails
    return {
        'gold_24k_10g': 75000,
        'gold_22k_10g': 68700,
        'gold_18k_10g': 56250,
        'silver_1kg': 92000
    }
