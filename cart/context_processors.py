from decimal import Decimal

from django.db.models import QuerySet

from cart.models import OrderItem
from django.db.models.aggregates import Sum


def cart_session(request) -> dict[str, dict]:
    """
    Get cart session.

    :return: Cart session
    :rtype: dict[str, dict]
    """
    return {"cart_session": request.session.get("cart")}


def get_cart_price_not_auth(request) -> dict[str, Decimal | int]:
    """
    Get the total price of items in the cart if the user has not authenticated.

    :return: Total price of items in the cart
    :rtype: dict[str, Decimal | int]
    """
    try:
        total_pr = sum(
            Decimal(item["price"]) * item["qty"] for item in request.session.get("cart")
        )
    except TypeError:
        total_pr = 0
    return {"get_cart_price_not_auth": total_pr}


def get_cart_qty_not_auth(request) -> dict[str, int]:
    """
    Get the total quantity of items in the cart if the user has not authenticated.

    :return: Total quantity of items in the cart
    :rtype: dict[str, int]
    """
    try:
        total_qty = sum(item["qty"] for item in request.session.get("cart"))
    except TypeError:
        total_qty = 0
    return {"get_cart_qty_not_auth": total_qty}


def order_items_cart(request) -> dict[str, QuerySet[OrderItem]]:
    """
    Get order items of user.

    :return: Order items of user
    :rtype: dict[str, QuerySet[OrderItem]]
    """
    return {"order_items_cart": OrderItem.objects.filter(user__username=request.user)}


def get_cart_qty_auth(request) -> dict[str, QuerySet[OrderItem]]:
    """
    Get the quantity of products in cart of authenticated user.

    :return: Quantity of products in cart
    :rtype: dict[str, QuerySet[OrderItem]]
    """
    get_cart_qty = (
        OrderItem.objects.filter(user__username=request.user)
        .aggregate(get_cart_qty_auth=Sum("quantity"))
        .get("get_cart_qty_auth", 0)
    )
    return {"get_cart_qty": get_cart_qty}


def get_cart_total_auth(request) -> dict[str, QuerySet[OrderItem]]:
    """
     Get the total price of products in cart of authenticated user.

    :return: Total price of products in cart
    :rtype: dict[str, QuerySet[OrderItem]]
    """
    get_cart_total = (
        OrderItem.objects.filter(user__username=request.user)
        .aggregate(get_cart_total_auth=Sum("product__price") * Sum("quantity"))
        .get("get_cart_total_auth", 0)
    )
    return {"get_cart_total": get_cart_total}
