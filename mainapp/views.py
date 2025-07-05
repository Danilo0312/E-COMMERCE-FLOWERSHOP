from django.contrib.auth import authenticate, login
from django.db.models import QuerySet
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http.response import BadHeaderError, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, View, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .services import send_message_order, searched_products
from .models import Category, Dislike, Like, Order, Product
from cart.models import OrderItem
from .forms import (
    ReviewForm,
    RegistrationForm,
    AccountAuthenticationForm,
    OrderForm,
)


class AboutUsView(TemplateView):

    template_name = "about.html"


class ReviewPageView(TemplateView):

    template_name = "reviews.html"


class BaseView(ListView):

    paginate_by = 10
    model = Product
    context_object_name = "products"
    template_name = "base.html"


class ProductDetailView(DetailView):

    model = Product
    context_object_name = "product"
    template_name = "product_detail.html"
    slug_url_kwarg = "slug"


class CategoryListView(ListView):
    model = Product
    template_name = 'category_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        context['products_of_category'] = Product.objects.filter(category=category)
        context['category'] = category
        context['products_search'] = searched_products(self.request.GET.get('q'), category)
        return context

    def get_queryset(self) -> QuerySet[Product]:
        q = self.request.GET.get("q")
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return searched_products(q, category)


class CategoriesListView(ListView):

    model = Category
    context_object_name = "categories"
    template_name = "categories_detail.html"


class OrderView(View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {"form": form}
        return render(request, "order.html", context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        if form.is_valid():
            f_name = form.cleaned_data.get("f_name")
            l_name = form.cleaned_data.get("l_name")
            email = form.cleaned_data.get("email")
            phone_number = form.cleaned_data.get("phone_number")
            buying_type = form.cleaned_data.get("buying_type")
            address = form.cleaned_data.get("address")
            comment = form.cleaned_data.get("comment")
            try:
                send_message_order(request, f_name, l_name, email, phone_number, buying_type, address, comment)
                if not request.user.is_authenticated:
                    del request.session["cart"]
                    request.session.modified = True
                order_qs = Order.objects.filter(user=request.user)
                if order_qs.exists():
                    order = order_qs[0]
                    if order.products_cart.filter(user=request.user).exists():
                        order_item = OrderItem.objects.filter(user=request.user)
                        order.delete()
                        order_item.delete()
            except BadHeaderError:
                return HttpResponse("Плохое соединение")
            messages.success(request, "Спасибо за заказ!")
            return redirect("/")
        context = {"form": form}
        return render(request, "order.html", context)


class AccountAuthenticationView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        form = AccountAuthenticationForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, "login.html", context)

    def post(self, request, *args, **kwargs):
        form = AccountAuthenticationForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                if request.session.get("cart"):
                    del request.session["cart"]
                    request.session.modified = True
                login(request, user)
                messages.success(request, "Вы авторизированны!")
                return redirect("/")
            else:
                messages.error(request, "Пожалуйста исправьте ошибки!")
        context = {
            "form": form,
        }
        return render(request, "login.html", context)


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        form = RegistrationForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, "registration.html", context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            if request.session.get("cart"):
                del request.session["cart"]
                request.session.modified = True
            account = authenticate(email=email, password=password)
            login(request, account)
            messages.success(request, "Регистрация прошла успешно!")
            return redirect("/")
        else:
            messages.error(request, "Пожалуйста исправьте ошибки!")
        context = {
            "form": form,
        }
        return render(request, "registration.html", context)


class AddReviewToProduct(View):
    """Отзывы"""

    def post(self, request, slug, *args, **kwargs):
        form = ReviewForm(request.POST)
        product = Product.objects.get(slug=slug)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.product = product
            form.save()
        return HttpResponseRedirect(product.get_absolute_url())


class LikeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        like = Like.objects.filter(user=request.user, products=product)
        dislike = Dislike.objects.filter(user=request.user, products=product)
        if not like.exists():
            if not dislike.exists():
                Like.objects.create(user=request.user, products=product)
                return redirect(request.POST.get("url_from"))
            else:
                Dislike.objects.get(user=request.user, products=product).delete()
                Like.objects.create(user=request.user, products=product)
        else:
            Like.objects.get(user=request.user, products=product).delete()
        return redirect(request.POST.get("url_from"))


class DislikeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, id, *args, **kwargs):
        product = get_object_or_404(Product, id=id)
        like = Like.objects.filter(user=request.user, products=product)
        dislike = Dislike.objects.filter(user=request.user, products=product)
        if not dislike.exists():
            if not like.exists():
                Dislike.objects.create(user=request.user, products=product)
                return redirect(request.POST.get("url_from"))
            else:
                Like.objects.get(user=request.user, products=product).delete()
                Dislike.objects.create(user=request.user, products=product)
        else:
            Dislike.objects.get(user=request.user, products=product).delete()
        return redirect(request.POST.get("url_from"))
