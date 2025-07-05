from django import template
from django.shortcuts import get_object_or_404
from django.db.models import Count, QuerySet

from mainapp.models import Like, Dislike, Product

register = template.Library()


@register.filter
def count_likes(id: int) -> QuerySet[Like]:
    """
    Count likes in templates

    :param int id: Through this id we get current product
    :return: Counted likes
    :rtype: QuerySet[Like]
    """
    product = get_object_or_404(Product, id=id)
    result = (
        Like.objects.filter(products=product)
        .aggregate(count_likes=Count("products"))
        .get("count_likes", 0)
    )
    return result


@register.filter
def count_dislikes(id: int) -> QuerySet[Dislike]:
    """
    Count dislikes in templates

    :param int id: Through this id we get current product
    :return: Counted dislikes
    :rtype: QuerySet[Dislike]
    """
    product = get_object_or_404(Product, id=id)
    result = (
        Dislike.objects.filter(products=product)
        .aggregate(count_dislikes=Count("products"))
        .get("result", 0)
    )
    return result