from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED

def get_products_from_cache():
    """Получает данные о продуктах из кэша, если кэш пуст, получает данные из бд."""
    if not CACHE_ENABLED:
        return Product.objects.all
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.object.all()
    cache.set(key, products)
    return products

