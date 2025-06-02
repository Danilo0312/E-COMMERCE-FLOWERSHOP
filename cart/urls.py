from django.urls import path
from .views import (
    CartView, AddProductToCartAuthenticatedUserView,
    AddProductToCartNotAuthenticatedUserView,
    DeleteProductFromCartAuthenticatedUserView,
    DeleteProductFromCartNotAuthenticatedUserView,
    DeleteOneProductFromCartNotAuthenticatedUserView,
    DeleteAllProductsFromCartAuthenticatedUserView,
    DeleteAllProductsFromCartNotAuthenticatedUserView
)

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path(
        "<int:id>/add-authenticated/",
        AddProductToCartAuthenticatedUserView.as_view(),
        name="cart-add-authenticated",
    ),
    path(
        "<int:id>/add-not-authenticated/",
        AddProductToCartNotAuthenticatedUserView.as_view(),
        name="cart-add-not-authenticated",
    ),
    path(
        "<int:id>/remove-authenticated/",
        DeleteProductFromCartAuthenticatedUserView.as_view(),
        name="cart-remove-authenticated",
    ),
    path(
        "<int:id>/remove-not-authenticated/",
        DeleteProductFromCartNotAuthenticatedUserView.as_view(),
        name="cart-remove-not-authenticated",
    ),
    path(
        "<int:id>/remove-one-not-authenticated/",
        DeleteOneProductFromCartNotAuthenticatedUserView.as_view(),
        name="remove-one-not-authenticated",
    ),
    path(
        "delete-authenticated/",
        DeleteAllProductsFromCartAuthenticatedUserView.as_view(),
        name="cart-delete-all-authenticated",
    ),
    path(
        "delete-not-authenticated/",
        DeleteAllProductsFromCartNotAuthenticatedUserView.as_view(),
        name="cart-delete-all-not-authenticated",
    ),
]
