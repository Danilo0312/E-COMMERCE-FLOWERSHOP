from typing import Any
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models import QuerySet
from django.contrib.postgres.search import (
    SearchQuery,
    SearchVector,
    SearchRank,
    SearchHeadline,
    TrigramSimilarity,
)

from .models import Product, Category


def send_message_order(
        request,
        f_name: str,
        l_name: str,
        email: str,
        phone_number: int,
        buying_type: str,
        address: str,
        comment: str
) -> Any:
    """
    Send email with order info to user email.


    :param request: HttpRequest of Django
    :param str f_name: First name of user
    :param str l_name: Last name of user
    :param str email: Email of user
    :param int phone_number: First name of user
    :param str buying_type: First name of user
    :param str address: First name of user
    :param str comment: First name of user
    :return: Method of EmailMultiAlternatives which send email
    :rtype: Any
    """
    subject, from_email, to = (
        "Venesia Flower Shop | Заказ №",
        "acperow.ram@yandex.ru",
        f"{email}",
    )
    text_content = ""
    data = {
        "f_name": f_name,
        "l_name": l_name,
        "email": email,
        "phone_number": phone_number,
        "buying_type": buying_type,
        "address": address,
        "comment": comment,
        "products": request.POST.get("product"),
    }
    html_content = render_to_string("html_email.html", data)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def searched_products(q: str, category: Category) -> QuerySet[Product]:
    """
    Search product with filter and string search.

    :param str q: Query parameter from url
    :param QuerySet[Category] category: Searched product in category

    :return: Searched product
    :rtype: QuerySet[Product]
    """
    vector = SearchVector("title")
    query = SearchQuery(q)
    search_headline = SearchHeadline("description", query)

    products_search = (
        Product.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline).annotate(
            similarity=TrigramSimilarity("title", q),
        ).filter(similarity__gt=0.1, category=category).order_by("-rank")
    )
    if q is None:
        products_search = Product.objects.filter(category=category)

    return products_search


def replace_to_dot(price: str) -> float:
    """
    Get price in str with comma from request.POST.get('price') and convert to float with dot.

    :param str price: Price from request.POST.get('price')
    :rtype: float
    """
    for i in price.replace(',', '.').split():
        price = i
    return float(price)