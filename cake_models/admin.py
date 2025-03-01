from django.contrib import admin
from .models import Bitlink, Sizes, Forms, Toppings, Berries, Decors, User, Profile, Order
from cake_models.shortlink import count_clicks, shorten_link
from environs import Env

env = Env()
env.read_env()
vk_token = env.str('VK_TOKEN')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk','name', 'email', 'user')


@admin.register(Bitlink)
class BitlinkAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'bitlink', 'clicks')
    ordering = ['clicks']
    actions = ['count_clicks', 'shorten_link']

    @admin.action(description="Узнать количество переходов")
    def count_clicks(self, request, queryset):
        for obj in queryset:
            if obj.bitlink:
                obj.clicks = count_clicks(vk_token, obj.bitlink)
                obj.save()

    @admin.action(description="Сократить ссылки")
    def shorten_link(self, request, queryset):
        for obj in queryset:
            obj.bitlink = shorten_link(vk_token, obj.original_url)
            obj.save()


@admin.register(Sizes)
class SizesAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)


@admin.register(Forms)
class FormsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)


@admin.register(Toppings)
class ToppingsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)


@admin.register(Berries)
class BerriesAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)


@admin.register(Decors)
class DecorsAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)


@admin.register(Order)
class DecorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name',)

