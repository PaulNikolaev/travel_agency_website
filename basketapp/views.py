from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from basketapp.models import Basket
from mainapp.models import Accommodation


@login_required
def basket(request):
    title = 'корзина'
    basket_items = Basket.objects.filter(user=request.user).order_by('accommodation__country')

    total_nights = sum(item.nights for item in basket_items)
    total_cost = sum(item.accommodation_cost for item in basket_items)

    content = {
        'title': title,
        'basket_items': basket_items,
        'total_nights': total_nights,
        'total_cost': total_cost,
    }
    return render(request, 'basketapp/basket.html', content)


@login_required
def basket_add(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('acc:accommodations', args=[pk]))

    accommodation = get_object_or_404(Accommodation, pk=pk)
    basket = Basket.objects.filter(user=request.user, accommodation=accommodation).first()

    if not basket:
        basket = Basket(user=request.user, accommodation=accommodation)

    basket.nights += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required
def basket_edit(request, pk, nights):
    basket = get_object_or_404(Basket, pk=pk, user=request.user)

    try:
        nights = int(nights)
        if nights > 0:
            basket.nights = nights
            basket.save()
    except ValueError:
        pass  # можно также вернуть ошибку, если нужно

    # 👇 ВСТАВЬ ЗДЕСЬ — после сохранения корзины
    basket_items = Basket.get_items(request.user)
    total_nights = sum(item.nights for item in basket_items)
    total_cost = sum(item.accommodation_cost for item in basket_items)

    result_html = render_to_string('basketapp/includes/inc_basket_list.html', {
        'basket_items': basket_items,
        'total_nights': total_nights,
        'total_cost': total_cost,
    }, request=request)

    return JsonResponse({'result': result_html})
