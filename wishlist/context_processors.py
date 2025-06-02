from django.db.models import QuerySet
from django.db.models.aggregates import Sum
from wishlist.models import OrderItem


def wishes_session(request) -> dict[str, dict]:
    """
    Get wishlist session.

    :return: Wishlist session
    :rtype: dict
    """
    return {'wishes_session': request.session.get("wishlist")}


def get_wishlist_qty_not_auth(request) -> dict[str, int]:
    """
    Get the quantity of products in wishlist of not authenticated user.

    :return: Total quantity
    :raises TypeError, ValueError: Get an error if total_qty was being wrong
    :rtype: dict[str, int]
    """
    try:
        total_qty = sum(item["qty"] for item in request.session.get("wishlist"))
    except (TypeError, ValueError):
        total_qty = 0
    return {"get_wishlist_qty_not_auth": total_qty}


def wishlist_items(request) -> dict[str, QuerySet[OrderItem]]:
    """
    Get wishlist items of user.

    :return: User wishlist items
    :rtype: dict[str, QuerySet[OrderItem]]
    """
    return {"wishlist_items": OrderItem.objects.filter(user__username=request.user)}


def get_wishlist_qty_auth(request) -> dict[str, QuerySet[OrderItem]]:
    """
    Get the quantity of products in wishlist of authenticated user.

    :return: Total quantity
    :rtype: dict[str, QuerySet[OrderItem]]
    """
    get_wishlist_qty = OrderItem.objects.filter(user__username=request.user).aggregate(
        get_wishlist_qty_auth=Sum("quantity")).get("get_wishlist_qty_auth", 0)
    return {"get_wishlist_qty": get_wishlist_qty}
