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
        _accommodation = Basket.objects.filter(user=self.user)
        _total_nights = sum(list(map(lambda x: x.nights, _accommodation)))
        return _total_nights

    # Общая стоимость всех предложений в корзине
    @property
    def total_coast(self):
        _accommodation = Basket.objects.filter(user=self.user)
        _total_coast = sum(list(map(lambda x: x.accommodation_cost, _accommodation)))
        return _total_coast

    # количество заказов пользователя в корзине
    @staticmethod
    def get_items(user):
        return user.basket.select_related().order_by('accommodation__country')
