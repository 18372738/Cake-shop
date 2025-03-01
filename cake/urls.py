from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from cake_models.views import index, RegistrationUserView, ProfileListView, UserLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('registration/', RegistrationUserView.as_view(), name='register'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout')

]
