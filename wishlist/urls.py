from django.urls import path
from .views import (
    WishesView,
    AddProductToWishesAuthenticatedUserView,
    AddProductToWishesNotAuthenticatedUserView,
    DeleteProductFromWishesAuthenticatedUserView,
    DeleteProductFromWishesNotAuthenticatedUserView,
    DeleteAllProductsFromWishesAuthenticatedUserView,
    DeleteAllProductsFromWishesNotAuthenticatedUserView,

)

app_name = "wishlist"

urlpatterns = [
    path("", WishesView.as_view(), name="wishlist"),
    path(
        "<int:id>/add-authenticated/",
        AddProductToWishesAuthenticatedUserView.as_view(),
        name="wishlist-add-authenticated",
    ),
    path(
        "<int:id>/add-not-authenticated/",
        AddProductToWishesNotAuthenticatedUserView.as_view(),
        name="wishlist-add-not-authenticated",
    ),
    path(
        "<int:id>/remove-authenticated/",
        DeleteProductFromWishesAuthenticatedUserView.as_view(),
        name="wishlist-remove-authenticated",
    ),
    path(
        "<int:id>/remove-not-authenticated/",
        DeleteProductFromWishesNotAuthenticatedUserView.as_view(),
        name="wishlist-remove-not-authenticated",
    ),
    path(
        "delete-authenticated/",
        DeleteAllProductsFromWishesAuthenticatedUserView.as_view(),
        name="wishlist-delete-all-authenticated",
    ),
    path(
        "delete-not-authenticated/",
        DeleteAllProductsFromWishesNotAuthenticatedUserView.as_view(),
        name="wishlist-delete-all-not-authenticated",
    ),
]
