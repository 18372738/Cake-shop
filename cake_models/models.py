from django.db import models


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
