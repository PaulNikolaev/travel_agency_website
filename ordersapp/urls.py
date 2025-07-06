import ordersapp.views as ordersapp
from django.urls import path

app_name = "ordersapp"

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='orders_list'),
    path('create/', ordersapp.OrderItemsCreate.as_view(), name='order_create'),
]
