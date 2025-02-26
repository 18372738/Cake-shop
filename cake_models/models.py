from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    phone = PhoneNumberField(
        unique=True,
        verbose_name="Номер телефона",
        region='RU'
    )
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Profile(models.Model):
    name = models.CharField('Имя', max_length=100, blank=True)
    email = models.EmailField('Email', max_length=100, unique=True, blank=True)
    phone_number = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

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
