from django.db import models

MEMBER_TYPE = (
    ('PLNT', 'plant'),
    ('INDV', 'individual'),
    ('RTL', 'retail')
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
        ordering = ['-created_at']

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
    member_type = models.CharField(max_length=4, choices=MEMBER_TYPE, verbose_name='тип звена')
    accounts_payable = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='кредиторка')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    updated_at = models.DateField(auto_now=True, verbose_name='дата изменения')
    supplier = models.OneToOneField(to='Member', on_delete=models.PROTECT, verbose_name='поставщик')

    class Meta:
        verbose_name = 'элемент сети'
        verbose_name_plural = 'элементы сети'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} {self.member_type}"
