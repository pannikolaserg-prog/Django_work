from django.core.cache import cache
from django.conf import settings

CACHE_ENABLED = getattr(settings, 'CACHE_ENABLED', True)


def get_products_from_cache(user):
    """Возвращает список всех продуктов с кэшированием"""
    from .models import Product

    if not CACHE_ENABLED:
        return _get_all_products(user)

    is_moderator = user.is_authenticated and user.has_perm('catalog.can_unpublish_product')
    user_type = "moderator" if is_moderator else "user"
    key = f"all_products_{user_type}"

    products = cache.get(key)
    if products is not None:
        return products

    products = _get_all_products(user)
    cache.set(key, products, 300)
    return products


def _get_all_products(user):
    """Внутренняя функция для получения продуктов из БД"""
    from .models import Product

    products = Product.objects.all()

    is_moderator = user.is_authenticated and user.has_perm('catalog.can_unpublish_product')
    if not is_moderator:
        products = products.filter(is_published=True)

    return products.order_by('name')


def get_products_by_category(category_id, user):
    """Возвращает список продуктов в указанной категории"""
    from .models import Product

    products = Product.objects.filter(category_id=category_id)

    is_moderator = user.is_authenticated and user.has_perm('catalog.can_unpublish_product')
    if not is_moderator:
        products = products.filter(is_published=True)

    return products.order_by('name')


def get_category_by_id(category_id):
    """Возвращает категорию по ID"""
    from .models import Category
    try:
        return Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return None


def get_all_categories():
    """Возвращает список всех категорий"""
    from .models import Category
    return Category.objects.all()
