from django.db.models import QuerySet

from .models import Category, Product


def products(request) -> dict[str, QuerySet[Product]]:
    """
    Context processor for templates which return Product qs.

    :return: Product queryset
    :rtype: dict[str, QuerySet[Product]]
    """
    return {"products": Product.objects.all()}


def categories(request) -> dict[str, QuerySet[Category]]:
    """
    Context processor for templates which return Category qs.

    :return: Category queryset
    :rtype: dict[str, QuerySet[Category]]
    """
    return {"categories": Category.objects.all()}