from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile, Order
# from .bot import send_order_bot

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# @receiver(post_save, sender=Order)
# def send_order(sender, instance, created, **kwargs):
#     if created:
#         message = 'Заказ создан. Сообщение сделано в качестве примера'
#         send_order_bot(message)
