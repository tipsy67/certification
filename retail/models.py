from django.db import models
from config.settings import NULLABLE


GRAND_LEVEL = 'PLNT'
GRAND_NAME = 'Завод'
MEMBER_TYPE = (
    (GRAND_LEVEL, GRAND_NAME),
    ('INDV', 'Индивидуальный предприниматель'),
    ('RTL', 'Розничная сеть')
)

class Contact(models.Model):
    email = models.EmailField(verbose_name='эл.почта')
    country = models.CharField(max_length=100, verbose_name='страна')
    city = models.CharField(max_length=100, verbose_name='город')
    street = models.CharField(max_length=100, verbose_name='улица')
    building = models.CharField(max_length=100, verbose_name='строение')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='дата изменения')
    member = models.ForeignKey(to='Member', on_delete=models.CASCADE, related_name='contacts', verbose_name='')

    class Meta:
        verbose_name = 'контакт'
        verbose_name_plural = 'контакты'
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.email}"


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    product_model = models.CharField(max_length=100, verbose_name='модель')
    launch_date = models.DateField(verbose_name='дата выхода на рынок')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='дата изменения')
    member = models.ForeignKey(to='Member', on_delete=models.CASCADE, related_name='products', verbose_name='')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} {self.product_model}"

class Member(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    member_type = models.CharField(max_length=4, choices=MEMBER_TYPE, default=GRAND_LEVEL, verbose_name='тип звена')
    member_level = models.PositiveSmallIntegerField(editable=False, default=0, verbose_name='уровень')
    accounts_payable = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='кредиторка')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='дата изменения')
    supplier = models.ForeignKey(to='Member', on_delete=models.PROTECT, **NULLABLE, default= None, related_name='buyers', verbose_name='поставщик')
    need_recalc = models.BooleanField(editable=False, default=False, verbose_name='уровень')


    class Meta:
        verbose_name = 'элемент сети'
        verbose_name_plural = 'элементы сети'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.display_member_type})"

    @property
    def display_member_type(self):
        return dict(MEMBER_TYPE).get(f"{self.member_type}", "ошибка")








