from django.contrib.auth import logout, login, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from .forms import RegistrationUserForm
from .models import User, Profile, Sizes, Forms, Toppings, Berries, Decors


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


class ProfileListView(DetailView):
    model = Profile
    template_name = 'lk-order.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        print(f"Авторизованный пользователь: {self.request.user},{self.request.user.is_authenticated}")
        if not self.request.user.is_authenticated:
            raise Http404("Пользователь не авторизован.")
        return get_object_or_404(Profile, user=self.request.user)


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("index")
