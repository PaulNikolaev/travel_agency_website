import adminapp.views as adminapp
from django.urls import path

app_name = 'adminapp'

urlpatterns = [
    path('users/read/', adminapp.TravelUserListView.as_view(), name='users'),
]