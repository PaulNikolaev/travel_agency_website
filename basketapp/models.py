from django.db import models
from django.conf import settings
from mainapp.models import Accommodation


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    nights = models.PositiveIntegerField(verbose_name='количество ночей', default=0)
    add_datetime = models.DateTimeField(verbose_name='время', auto_now_add=True)

    # Стоимость одного предложения
    @property
    def accommodation_cost(self):
        return self.accommodation.price * self.nights

    # Общее количество ночей по всем заказам
    @property
    def total_nights(self):
        return sum(item.nights for item in Basket.objects.filter(user=self.user))

    # Общая стоимость всех предложений в корзине
    @property
    def total_cost(self):
        return sum(item.accommodation_cost for item in Basket.objects.filter(user=self.user))

    # количество заказов пользователя в корзине
    @staticmethod
    def get_items(user):
        return user.basket.select_related().order_by('accommodation__country')
