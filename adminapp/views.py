from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from django.template.defaultfilters import title
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.decorators import method_decorator
from mainapp.models import Accommodation, ListOfCountries
from authapp.models import TravelUser
from authapp.forms import TravelUserRegisterForm, TravelUserEditForm
from adminapp.forms import TravelUserAdminEditForm, AccommodationEditForm


# админка - список пользователей
class TravelUserListView(ListView):
    model = TravelUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


# админка - создание пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    title = 'пользователи/создание'

    if request.method == 'POST':
        user_form = TravelUserRegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin:users'))
    else:
        user_form = TravelUserRegisterForm()

    content = {
        'title': title,
        'update_form': user_form,
    }
    return render(request, 'adminapp/user_update.html', content)


# админка - редактирование пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'пользователи/редактирование'

    edit_user = get_object_or_404(TravelUser, pk=pk)

    if request.method == 'POST':
        edit_form = TravelUserAdminEditForm(request.POST,
                                            request.FILES,
                                            instance=edit_user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin:user_update',
                                                args=[edit_user.pk]))
    else:
        edit_form = TravelUserAdminEditForm(instance=edit_user)

    content = {
        'title': title,
        'update_form': edit_form,
    }

    return render(request, 'adminapp/user_update.html', content)


# админка - удаление пользователя
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'пользователи/удаление'

    user = get_object_or_404(TravelUser, pk=pk)
    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('admin:users'))

    content = {
        'title': title,
        'user_to_delete': user,
    }
    return render(request, 'adminapp/user_delete.html', content)
