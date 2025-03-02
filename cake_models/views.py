import datetime
from django.contrib.auth import logout, login, get_user
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView
from django.utils.text import slugify

from .forms import RegistrationUserForm, LoginUserForm, ProfileUserForm
from .models import User, Profile, Sizes, Forms, Toppings, Berries, Decors, Order

import uuid
from yookassa import Configuration, Payment
from django.conf import settings
from environs import Env

from .forms import RegistrationUserForm
from .models import User, Profile, Sizes, Forms, Toppings, Berries, Decors



env = Env()
env.read_env()

def create_payment(request):

    Configuration.account_id = env.int('YOOKASSA_SHOP_ID')
    Configuration.secret_key = env.str('YOOKASSA_SECRET_KEY')
    
    payment = Payment.create({
        "amount": {
            "value": "100.00",  
            "currency": "RUB"
        },
        "capture_mode": "AUTOMATIC",  
        "confirmation": {
            "type": "redirect",
            "return_url": "https://thumbs.dreamstime.com/z/%D1%83%D1%81%D0%BF%D0%B5%D1%85-%D0%BE%D0%B4%D0%BE%D0%B1%D1%80%D0%B8%D0%BB-%D0%BF%D0%BE%D0%B4%D1%82%D0%B2%D0%B5%D1%80%D0%B6%D0%B4%D0%B5%D0%BD%D0%BD%D0%BE%D0%B5-%D1%83%D0%B2%D0%B5%D0%B4%D0%BE%D0%BC%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5-%D0%BA%D0%BE%D0%BD%D1%82%D1%80%D0%BE%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9-%D0%BF%D0%BE%D0%BC%D0%B5%D1%82%D0%BA%D0%B8-%D0%BE-206638829.jpg"
        },
        "description": "Описание платежа"
    })
    
    return redirect(payment.confirmation.confirmation_url)

def success(request):
    return render(request, 'success.html')

def payment_webhook(request):
    if request.method == "POST":
        data = request.json()
        payment_id = data['object']['id']
        status = data['object']['status']

        if status == "succeeded":
            # Логика добавления заказа
            pass
        else:
            # Если заказ не добавлен выводим какое-то сообщение
            pass

        return JsonResponse({"status": "ok"})

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


def create_order(request, id=None):
    email = request.GET.get('EMAIL')
    address = request.GET.get('ADDRESS')
    date = request.GET.get('DATE')
    time = request.GET.get('TIME')
    comment = request.GET.get('DELIVCOMMENTS')
    customer_name = request.GET.get('NAME')
    cake_name = request.GET.get('COMMENTS')
    phone = request.GET.get('PHONE')
    inscription=request.GET.get('WORDS')
    levels = request.GET.get('LEVELS')
    form = request.GET.get('FORM')
    topping = request.GET.get('TOPPING')
    berries = request.GET.get('BERRIES')
    decor = request.GET.get('DECOR')
    cake_id = request.GET.get('CAKE')
    total_cost = 0
    cake_berries_obj = None
    cake_decor_obj = None
    if berries:
        cake_berries = Berries.objects.get(id=berries)
        total_cost += cake_berries.price
    if decor:
        cake_decor = Decors.objects.get(id=decor)
        total_cost += cake_decor.price
    if inscription:
        total_cost = total_cost + 500

    cake_form = Forms.objects.get(id=form)
    cake_levels = Sizes.objects.get(id=levels)
    cake_topping = Toppings.objects.get(id=topping)
    total_cost += int(cake_form.price + cake_levels.price + cake_topping.price)
    if date:
        order_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        min_date = datetime.datetime.now() + datetime.timedelta(days=1)
        if order_date < min_date:
            total_cost = int(total_cost) * 1.2
    user, created = User.objects.get_or_create(
        phone=phone,
        defaults={"username": slugify(phone)}
    )
    order = Order.objects.create(
        user=user,
        client_name=customer_name,
        email=email,
        comment=cake_name,
        address=address,
        delivery_datetime=f'{date} {time}',
        delivery_comment=f'{comment}',
        size=cake_levels,
        form=cake_form,
        topping=cake_topping,
        berry=cake_berries,
        decor=cake_decor,
        inscription=inscription,
        total_cost=total_cost
    )


def index(request):
    phone = request.GET.get('PHONE')
    if phone:
        create_order(request)
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