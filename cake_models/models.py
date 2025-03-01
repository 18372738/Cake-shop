from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField


ORDER_STATUSES = (
    ('ADOPTED', 'Принят'),
    ("courier", "передан курьеру"),
    ("delivered", "доставлено")
)


class User(AbstractUser):
    phone = PhoneNumberField(
        unique=True,
        verbose_name="Номер телефона",
        region='RU',
    )
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = slugify(self.phone)
        super().save(*args, **kwargs)


class Profile(models.Model):
    name = models.CharField('Имя', max_length=100, blank=True)
    email = models.EmailField('Email', max_length=100, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Личный кабинет'
        verbose_name_plural = 'Личные кабинеты'


class Bitlink(models.Model):
    original_url = models.URLField(verbose_name="Url-Адрес")
    bitlink = models.URLField(verbose_name="Сокращенная ссылка", blank=True, null=True)
    clicks = models.IntegerField(verbose_name="Количество переходов", default=0)

    class Meta():
        verbose_name = 'Битлинк'
        verbose_name_plural = 'Битлинки'

    def __str__(self):
        return self.bitlink or self.original_url


class Sizes(models.Model):
    title = models.CharField(
        'Количество уровней',
        max_length=100
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=7,
        decimal_places=2,
    )

    class Meta():
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'

    def __str__(self):
        return self.title


class Forms(models.Model):
    title = models.CharField(
        'Форма',
        max_length=100
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
    )

    class Meta():
        verbose_name = 'Форма'
        verbose_name_plural = 'Формы'

    def __str__(self):
        return self.title


class Toppings(models.Model):
    title = models.CharField(
        'Топпинг',
        max_length=100
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
    )

    class Meta():
        verbose_name = 'Топпинг'
        verbose_name_plural = 'Топпинги'

    def __str__(self):
        return self.title


class Berries(models.Model):
    title = models.CharField(
        'Ягода',
        max_length=100
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
    )

    class Meta():
        verbose_name = 'Ягода'
        verbose_name_plural = 'Ягоды'

    def __str__(self):
        return self.title


class Decors(models.Model):
    title = models.CharField(
        'Декор',
        max_length=100
    )
    price = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
    )

    class Meta():
        verbose_name = 'Декор'
        verbose_name_plural = 'Декоры'

    def __str__(self):
        return self.title


class Order(models.Model):
    status = models.CharField(
        verbose_name="Статус",
        choices=ORDER_STATUSES,
        max_length=30,
        default="true",
    )

    size = models.ForeignKey(
        Sizes,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Количество уровней торта',
        null=True,
        blank=True,
    )

    form = models.ForeignKey(
        Forms,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Форма торта',
        null=True,
        blank=True,
    )

    topping = models.ForeignKey(
        Toppings,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Топпинг',
        null=True,
        blank=True,
    )

    berry = models.ForeignKey(
        Berries,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Ягоды',
        null=True,
        blank=True,
    )

    decor = models.ForeignKey(
        Decors,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Декор',
        null=True,
        blank=True,
    )

    inscription = models.TextField(
        'надпись на торт',
        blank=True,
    )

    comment = models.TextField(
        'комментарий к заказу',
        blank=True
    )

    client_name = models.CharField(
        'имя клиента',
        max_length=100
    )

    phonenumber = PhoneNumberField(
        verbose_name='номер телефона',
        region='RU',
        unique=True
    )

    email = models.EmailField(
        verbose_name='почта клиента'
    )

    address = models.CharField(
        'адрес доставки',
        max_length=250,
        blank=True
    )

    delivery_datetime = models.DateTimeField(
        'дата и время доставки',
        db_index=True,
        null=True,
        blank=True,
    )

    delivery_comment = models.TextField(
        'комментарий курьеру',
        blank=True
    )

    created_at = models.DateTimeField(
        'заказ зарегестрирован',
        default=timezone.now,
        db_index=True
    )

    total_cost = models.IntegerField(
        'Стоимость заказа',
        null=True,
        blank=True
    )

    class Meta():
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'Заказ № {self.id}. {self.client_name}, телефон - {self.phonenumber}'

