from django.contrib import admin
from .models import Bitlink, Sizes, Forms, Toppings, Berries, Decors


@admin.register(Bitlink)
class BitlinkAdmin(admin.ModelAdmin):
    list_display = ('original_url', 'bitlink', 'clicks')


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
