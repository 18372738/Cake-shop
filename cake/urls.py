from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cake_models.views import index, RegistrationUserView, ProfileListView, UserLogoutView, LoginUserView
from cake_models.views import index, RegistrationUserView, ProfileListView, UserLogoutView, create_payment, success


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('registration/', RegistrationUserView.as_view(), name='register'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('create-payment/', create_payment, name='create_payment'),
    path('payment/success/', success, name='payment_success'),
]
