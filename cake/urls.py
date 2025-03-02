from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

<<<<<<< HEAD
from cake_models.views import index, RegistrationUserView, ProfileListView, UserLogoutView, LoginUserView
=======
from cake_models.views import index, RegistrationUserView, ProfileListView, UserLogoutView, create_payment, success, payment_webhook
>>>>>>> f5c544c (Add payment)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('registration/', RegistrationUserView.as_view(), name='register'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
<<<<<<< HEAD
    path('login/', LoginUserView.as_view(), name='login'),
=======
    path('create-payment/', create_payment, name='create_payment'),
    path('payment/success/', success, name='payment_success'),
    path('payment/webhook/', payment_webhook, name='payment_webhook')
>>>>>>> f5c544c (Add payment)

]
