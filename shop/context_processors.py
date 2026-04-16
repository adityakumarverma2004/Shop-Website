from .utils.metal_prices import get_live_metal_prices

def live_metal_prices_processor(request):
    """
    Exposes the 10g Gold (24k, 22k, 18k) and 1kg Silver live prices
    to all templates globally context variable `metal_prices`.
    """
    prices = get_live_metal_prices()
    return {
        'metal_prices': prices
    }
