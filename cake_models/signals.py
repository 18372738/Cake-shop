import telegram
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Profile, Order
from cake.settings import TG_BOT_TOKEN, TG_CHAT_ID


bot = telegram.Bot(token=TG_BOT_TOKEN)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Order)
def notify_telegram(sender, instance, created, **kwargs):
    if created:
        message = (f"Новый заказ!\n"
            f"Клиент: {instance.user.phone}\n"
            f"Дата: {instance.dates}\n"
            f"Время: {instance.time}\n"
            f"Адрес: {instance.address}\n"
            f"Комментарий: {instance.delivcomments or 'Нет'}"
        )
        bot.send_message(chat_id=TG_CHAT_ID, text=message, reply_markup=reply_markup)
