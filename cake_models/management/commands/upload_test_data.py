import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from cake_models.models import Sizes, Forms, Toppings, Berries, Decors, User, Profile, Order


class Command(BaseCommand):
    help = "Заполнить базу данных тестовыми данными"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # Создание клиентов
            # user_1 = User.objects.create(
            #     phone="+79004217012",
            #     username="Иван"
            # )
            # user_2 = User.objects.create(
            #     phone="+79004216012",
            #     username="Любовь"
            # )
            # user_3 = User.objects.create(
            #     phone="+79004215012",
            #     username="Пётр"
            # )
            # if not Profile.objects.filter(phone_number=user_1).exists():
            #     profile_1 = Profile.objects.create(
            #         name=user_1.username,
            #         email="iv@mail.ru",
            #         phone_number=user_1
            #     )
            # if not Profile.objects.filter(phone_number=user_2).exists():
            #     profile_2 = Profile.objects.create(
            #         name=user_2.username,
            #         email="love@mail.ru",
            #         phone_number=user_2
            #     )
            # if not Profile.objects.filter(phone_number=user_3).exists():
            #     profile_3 = Profile.objects.create(
            #         name=user_3.username,
            #         email="pet@mail.ru",
            #         phone_number=user_3
            #     )

            size_1 = Sizes.objects.create(
                title="1",
                price="400"
            )
            size_2 = Sizes.objects.create(
                title="2",
                price="750"
            )
            size_3 = Sizes.objects.create(
                title="3",
                price="1100"
            )

            form_1 = Forms.objects.create(
                title="Квадрат",
                price="600"
            )
            form_2 = Forms.objects.create(
                title="Круг",
                price="400"
            )
            form_3 = Forms.objects.create(
                title="Прямоугольник",
                price="1000"
            )

            topping_1 = Toppings.objects.create(
                title="Без",
                price="0"
            )
            topping_2 = Toppings.objects.create(
                title="Белый соус",
                price="200"
            )
            topping_3 = Toppings.objects.create(
                title="Карамельный сироп",
                price="180"
            )
            topping_4 = Toppings.objects.create(
                title="Кленовый сироп",
                price="2000"
            )
            topping_5 = Toppings.objects.create(
                title="Клубничный сироп",
                price="300"
            )
            topping_6 = Toppings.objects.create(
                title="Черничный сироп",
                price="350"
            )
            topping_7 = Toppings.objects.create(
                title="Молочный шоколад",
                price="200"
            )

            berries_1 = Berries.objects.create(
                title="Ежевика",
                price="400"
            )
            berries_2 = Berries.objects.create(
                title="Малина",
                price="300"
            )
            berries_3 = Berries.objects.create(
                title="Голубика",
                price="450"
            )
            berries_4 = Berries.objects.create(
                title="Клубника",
                price="500"
            )

            decor_1 = Decors.objects.create(
                title="Фисташки",
                price="300"
            )
            decor_2 = Decors.objects.create(
                title="Безе",
                price="400"
            )
            decor_3 = Decors.objects.create(
                title="Фундук",
                price="350"
            )
            decor_4 = Decors.objects.create(
                title="Пекан",
                price="300"
            )
            decor_5 = Decors.objects.create(
                title="Маршмеллоу",
                price="200"
            )
            decor_5 = Decors.objects.create(
                title="Марципан",
                price="280"
            )

            # order_1 = Order.objects.create(
            #     size=size_1,
            #     form=form_1,
            #     topping=topping_1,
            #     berry=berries_1,
            #     decor=decor_1,
            #     inscription="С днём рождения",
            #     client_name="Иван",
            #     phonenumber="+79004217012",
            #     email="iv@mail.ru",
            #     address="Ленина 1",
            #     delivery_datetime=timezone.make_aware(
            #         datetime.datetime(2025, 3, 2, 8, 0)
            #     ),
            #     total_cost="1500",
            # )
            # order_2 = Order.objects.create(
            #     size=size_2,
            #     form=form_2,
            #     topping=topping_2,
            #     berry=berries_2,
            #     decor=decor_2,
            #     inscription="С днём рождения",
            #     client_name="Любовь",
            #     phonenumber="+79004216012",
            #     email="love@mail.ru",
            #     address="Ленина 2",
            #     delivery_datetime=timezone.make_aware(
            #         datetime.datetime(2025, 3, 1, 8, 0)
            #     ),
            #     total_cost="2000",
            # )
            # order_3 = Order.objects.create(
            #     size=size_3,
            #     form=form_3,
            #     topping=topping_3,
            #     berry=berries_3,
            #     decor=decor_3,
            #     inscription="С днём рождения",
            #     client_name="Пётр",
            #     phonenumber="+79004215012",
            #     email="pet@mail.ru",
            #     address="Ленина 3",
            #     delivery_datetime=timezone.make_aware(
            #         datetime.datetime(2025, 2, 28, 8, 0)
            #     ),
            #     total_cost="2500",
            # )

            self.stdout.write(
                self.style.SUCCESS(f"Тестовые данные успешно загружены в бд")
            )
