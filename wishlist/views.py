from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View

from mainapp.models import Product, Order
from mainapp.services import replace_to_dot
from .models import OrderItem


class WishesView(TemplateView):

    template_name = "wishlist.html"


class AddProductToWishesNotAuthenticatedUserView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            price = float(replace_to_dot(request.POST.get("price")))
            data = {
                "id": request.POST.get("id"),
                "title": request.POST.get("title"),
                "qty": 1,
                "price": price,
                "total_price_cart": price,
            }
            if not request.session.get("wishlist"):
                request.session["wishlist"] = list()
                if data not in request.session['wishlist']:
                    request.session['wishlist'].append(data)
                    request.session.modified = True
            else:
                request.session["wishlist"] = list(request.session["wishlist"])
        return redirect(request.POST.get("url_from"))


class AddProductToWishesAuthenticatedUserView(View):
    def post(self, request, id, *args, **kwargs):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            order_item, created = OrderItem.objects.get_or_create(
                product=product, user=request.user
            )
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if not order.products_wishlist.filter(product__id=product.id).exists():
                    order.products_wishlist.add(order_item)
                    order_item.quantity = 1
                    return redirect(request.POST.get("url_from"))
                else:
                    messages.add_message(request, messages.INFO, "Уже есть в желаниях")
            else:
                order = Order.objects.create(user=request.user)
                order.products_wishlist.add(order_item)
                return redirect(request.POST.get("url_from"))
        return redirect(request.POST.get("url_from"))


class DeleteProductFromWishesNotAuthenticatedUserView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            for item in request.session["wishlist"]:
                if str(item["id"]) == str(request.POST.get("id")):
                    item.clear()

            while {} in request.session["wishlist"]:
                request.session["wishlist"].remove({})

            if not request.session["wishlist"]:
                del request.session["wishlist"]

            request.session.modified = True
        return redirect(request.POST.get("url_from"))
        

class DeleteProductFromWishesAuthenticatedUserView(View):
    def post(self, request, id, *args, **kwargs):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products_wishlist.filter(product__id=product.id).exists():
                    order_item = OrderItem.objects.filter(
                        product=product, user=request.user
                    )[0]
                    order.products_wishlist.remove(order_item)
                    order_item.delete()
                    messages.add_message(request, messages.INFO, "This item quantity was updated.")
                    return redirect("/")
                else:
                    messages.add_message(request, messages.ERROR, "This item was not in your cart")
                    return redirect("/", id=id)
        return redirect(request.POST.get("url_from"))


class DeleteAllProductsFromWishesNotAuthenticatedUserView(View):
    def post(self, request, *args, **kwargs):
        if request.session.get("wishlist") and not request.user.is_authenticated:
            del request.session["wishlist"]
        return redirect(request.POST.get("url_from"))


class DeleteAllProductsFromWishesAuthenticatedUserView(View):
    def post(self, request, id, *args, **kwargs):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products_wishlist.filter(product__id=product.id).exists():
                    order_item = OrderItem.objects.filter(
                        product=product, user=request.user
                    )[0]
                    order.products_wishlist.remove(order_item)
                    order_item.delete()
                    return redirect("/")
                else:
                    return redirect("/", id=id)
            else:
                return redirect("/", id=id)
        return redirect(request.POST.get("url_from"))
