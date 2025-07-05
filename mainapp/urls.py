from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    BaseView,
    ProductDetailView,
    CategoryListView,
    CategoriesListView,
    OrderView,
    AccountAuthenticationView,
    RegistrationView,
    AddReviewToProduct,
    AboutUsView,
    ReviewPageView,
    LikeView,
    DislikeView
)


urlpatterns = [
    path("", BaseView.as_view(), name="base"),
    path("products/<str:slug>/", ProductDetailView.as_view(), name="product_detail"),
    path("category/<str:slug>/", CategoryListView.as_view(), name="category_detail"),
    path("categories/", CategoriesListView.as_view(), name="categories"),
    path("order/", OrderView.as_view(), name="make_order"),
    path("about/", AboutUsView.as_view(), name="about"),
    path("review/<str:slug>/", AddReviewToProduct.as_view(), name="add_review"),
    path("reviews/", ReviewPageView.as_view(), name="reviews"),
    path("login/", AccountAuthenticationView.as_view(), name="login"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("logout/", LogoutView.as_view(next_page="/"), name="logout"),
    path("like/<int:id>", LikeView.as_view(), name="like"),
    path("dislike/<int:id>", DislikeView.as_view(), name="dislike"),
]
