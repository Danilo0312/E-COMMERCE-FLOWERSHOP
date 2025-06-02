from django.db import models
from django.conf import settings


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE, related_name="user_for_cart")
    product = models.ForeignKey('mainapp.Product', on_delete=models.CASCADE, verbose_name="Товар", related_name="product_for_cart")
    quantity = models.IntegerField(default=1, verbose_name="Кол-во")

    class Meta:
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.quantity} {self.product.title} {self.user.username}"