from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View

from mainapp.models import Order, Product
from .models import OrderItem
from mainapp.services import replace_to_dot


class CartView(TemplateView):

    template_name = "order.html"


class AddProductToCartNotAuthenticatedUserView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            price = float(replace_to_dot(request.POST.get("price")))
            data = {
                "id": int(request.POST.get("id")),
                "title": request.POST.get("title"),
                "qty": 1,
                "price": price,
                "total_price_cart": price,
            }
            if not request.session.get("cart"):
                request.session["cart"] = list()
                if data not in request.session['cart']:
                    request.session['cart'].append(data)
                    request.session.modified = True
                else:
                    for item in request.session.get("cart"):
                        if item["id"] == request.POST.get("id"):
                            item['qty'] += 1
                            item['total_price_cart'] += item['price']
                            request.session.modified = True
            else:
                request.session["cart"] = list(request.session["cart"])
        return redirect(request.POST.get("url_from"))

        
class AddProductToCartAuthenticatedUserView(View):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            order_item, created = OrderItem.objects.get_or_create(
                product=product, user=request.user
            )
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products_cart.filter(product__id=product.id).exists():
                    order_item.quantity += 1
                    order_item.save()
                    return redirect(request.POST.get("url_from"))
                else:
                    order.products_cart.add(order_item)
                    return redirect(request.POST.get("url_from"))
            else:
                order = Order.objects.create(user=request.user)
                order.products_cart.add(order_item)
                return redirect(request.POST.get("url_from"))
        return redirect(request.POST.get("url_from"))


class DeleteProductFromCartNotAuthenticatedUserView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            for item in request.session["cart"]:
                if item["id"] == request.POST.get("id"):
                    item.clear()

            while {} in request.session["cart"]:
                request.session["cart"].remove({})

            if not request.session["cart"]:
                del request.session["cart"]

            request.session.modified = True
        return redirect(request.POST.get("url_from"))


class DeleteOneProductFromCartNotAuthenticatedUserView(View):
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            for item in request.session["cart"]:
                if item["id"] == request.POST.get("id") and item["qty"] > 1:
                    item["qty"] -= 1
                elif item["id"] == request.POST.get("id") and item["qty"] == 1:
                    item.clear()

            while {} in request.session["cart"]:
                request.session["cart"].remove({})

            if not request.session["cart"]:
                del request.session["cart"]

            request.session.modified = True
        return redirect(request.POST.get("url_from"))


class DeleteProductFromCartAuthenticatedUserView(View):
    def post(self, request, id, *args, **kwargs):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products_cart.filter(product__id=product.id).exists():
                    order_item = OrderItem.objects.filter(
                        product=product, user=request.user
                    )[0]
                    if order_item.quantity > 1:
                        order_item.quantity -= 1
                        order_item.save()
                    else:
                        order.products_cart.remove(order_item)
                        order_item.delete()
                    return redirect(request.POST.get("url_from"))
                else:
                    return redirect(request.POST.get("url_from"), id=id)
        return redirect(request.POST.get("url_from"))


class DeleteAllProductsFromCartNotAuthenticatedUserView(View):
    def post(self, request, *args, **kwargs):
        if request.session.get("cart") and not request.user.is_authenticated:
            del request.session["cart"]
            request.session.modified = True
        return redirect(request.POST.get("url_from"))


class DeleteAllProductsFromCartAuthenticatedUserView(View):
    def post(self, request, id, *args, **kwargs):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, id=id)
            order_qs = Order.objects.filter(user=request.user)
            if order_qs.exists():
                order = order_qs[0]
                # check if the order item is in the order
                if order.products_cart.filter(product__id=product.id).exists():
                    order_item = OrderItem.objects.filter(
                        product=product, user=request.user
                    )[0]
                    order.products_cart.remove(order_item)
                    order_item.delete()
                    messages.add_message(request, messages.INFO, "This item quantity was updated.")
                    return redirect("/")
                else:
                    return redirect("/", id=id)
            else:
                return redirect("/", id=id)
        return redirect(request.POST.get("url_from"))
