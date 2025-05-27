from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from mainapp.models import Accommodation, ListOfCountries
from authapp.models import TravelUser
from authapp.forms import TravelUserRegisterForm
from adminapp.forms import TravelUserAdminEditForm, AccommodationEditForm


# админка - список пользователей
class TravelUserListView(ListView):
    model = TravelUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



