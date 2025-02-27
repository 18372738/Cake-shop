from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from .forms import RegistrationUserForm
from .models import User, Profile


def index(request: HttpRequest) -> HttpResponse:
    context = {
        'form': RegistrationUserForm()
    }
    return render(request, "index.html", context)

class RegistrationUserView(CreateView):
    model = User
    form_class = RegistrationUserForm
    template_name = 'index.html'
    success_url = reverse_lazy('lk-order')

class ProfileListView(ListView):
    model = Profile
    template_name = 'lk-order.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user