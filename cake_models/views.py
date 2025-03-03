from django.contrib.auth import logout, login, get_user
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.utils.text import slugify

import uuid
from yookassa import Configuration, Payment
from django.conf import settings

from .forms import RegistrationUserForm, LoginUserForm, ProfileUserForm
from .models import User, Profile, Sizes, Forms, Toppings, Berries, Decors, Order



def create_payment(request):
    data = request.GET
    print(data)
    total_cost = request.GET.get("total_cost")
    create_order(data)

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    payment = Payment.create({
        "amount": {
            "value": str(total_cost),
            "currency": "RUB"
        },
        "capture_mode": "AUTOMATIC",
        "confirmation": {
            "type": "redirect",
            "return_url": "http://127.0.0.1:8000/"
        },
        "description": f"Оплата заказа на сумму {total_cost} руб."
    })

    request.session['payment_id'] = payment.id

    return redirect(payment.confirmation.confirmation_url)


def success(request):
    return render(request, 'success.html')


def create_order(data):
    email = data['email']
    address = data['address']
    date = data['date']
    time = data['time']
    comment = data['comment']
    customer_name = data['customer_name']
    phone = data['phone']
    inscription = data['inscription']
    levels = data['levels']
    form = data['form']
    topping = data['topping']
    berries = data['berries']
    decor = data['decor']
    total_cost = data['total_cost']
    delivcomment = data['deliv_comments']

    if berries != '0':
        cake_berries = Berries.objects.get(id=berries)
    else:
        cake_berries = None
    if decor != '0':
        cake_decor = Decors.objects.get(id=decor)
    else:
        cake_decor = None
    cake_form = Forms.objects.get(id=form)
    cake_levels = Sizes.objects.get(id=levels)
    cake_topping = Toppings.objects.get(id=topping)

    user, created = User.objects.get_or_create(
        phone=phone,
        defaults={"username": slugify(phone)}
    )

    order = Order.objects.create(
        user=user,
        client_name=customer_name,
        email=email,
        comment=f'{comment}',
        address=address,
        delivery_datetime=f'{date} {time}',
        delivery_comment=f'{delivcomment}',
        size=cake_levels,
        form=cake_form,
        topping=cake_topping,
        berry=cake_berries,
        decor=cake_decor,
        inscription=inscription,
        total_cost=total_cost
    )


def get_cake_element():
    cake_elements = {
        'forms': Forms.objects.all(),
        'toppings': Toppings.objects.all(),
        'berries': Berries.objects.all(),
        'decors': Decors.objects.all(),
        'sizes': Sizes.objects.all()
    }
    cake_elements_json = {
        'size_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['sizes']},
        'size_prices': {0: 0} | {item.id: int(item.price) for item in cake_elements['sizes']},
        'form_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['forms']},
        'form_prices': {0: 0} | {item.id: int(item.price) for item in cake_elements['forms']},
        'topping_titles': {0: 'не выбрано'} | {item.id: item.title for item in cake_elements['toppings']},
        'topping_prices': {0: 0} | {item.id: int(item.price) for item in cake_elements['toppings']},
        'berry_titles': {0: 'нет'} | {item.id: item.title for item in cake_elements['berries']},
        'berry_prices': {0: 0} | {item.id: int(item.price) for item in cake_elements['berries']},
        'decor_titles': {0: 'нет'} | {item.id: item.title for item in cake_elements['decors']},
        'decor_prices': {0: 0} | {item.id: int(item.price) for item in cake_elements['decors']},
    }

    return cake_elements, cake_elements_json



def index(request):
    cake_elements, cake_elements_json = get_cake_element()
    return render(
        request,
        template_name='index.html',
        context={
            'form': RegistrationUserForm(),
            'form_login': LoginUserForm(),
            'cake_elements': cake_elements,
            'cake_elements_json': cake_elements_json,
        }
    )


class RegistrationUserView(CreateView):
    model = User
    form_class = RegistrationUserForm
    template_name = 'index.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        print(f"Создан пользователь: {user}, ID: {user.id}, Phone: {user.phone}, Username: {user.username}", )

        return super().form_valid(form)

    def get_success_url(self):
        user = self.object
        login(self.request, user)
        print(f"Авторизованный пользователь: {self.request.user.is_authenticated}")
        return super().get_success_url()

class LoginUserView(LoginView):
    form_class = AuthenticationForm
    template_name = 'index.html'

    def get_success_url(self):
        return reverse_lazy('profile')

class ProfileListView(DetailView):
    model = Profile
    template_name = 'lk-order.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        print(f"Авторизованный пользователь: {self.request.user},{self.request.user.is_authenticated}")
        if not self.request.user.is_authenticated:
            raise Http404("Пользователь не авторизован.")
        return get_object_or_404(Profile, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        orders = Order.objects.filter(user=self.request.user)
        context['orders'] = orders
        context['phone'] = self.request.user.phone
        context['form'] = ProfileUserForm(instance=profile)
        return context

    def post(self,request, *args, **kwargs):
        profile = self.get_object()
        form = ProfileUserForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")
