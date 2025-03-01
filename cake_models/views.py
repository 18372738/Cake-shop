from django.contrib.auth import logout, login, get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from .forms import RegistrationUserForm
from .models import User, Profile, Sizes, Forms, Toppings, Berries, Decors


def get_cake_elements():
    elements = {
        'sizes': Sizes.objects.all(),
        'forms': Forms.objects.all(),
        'toppings': Toppings.objects.all(),
        'berries': Berries.objects.all(),
        'decors': Decors.objects.all(),
    }
    return elements

def index(request: HttpRequest) -> HttpResponse:

    context = {
        'form': RegistrationUserForm(),
        'elements': get_cake_elements(),
    }
    return render(request, "index.html", context)

class RegistrationUserView(CreateView):
    model = User
    form_class = RegistrationUserForm
    template_name = 'index.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        print(f"Создан пользователь: {user}, ID: {user.id}, Phone: {user.phone}, Username: {user.username}", )
        login(self.request, user)
        self.request.session.save()

        print(f"Авторизованный пользователь: {self.request.user.is_authenticated}")
        return super().form_valid(form)

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