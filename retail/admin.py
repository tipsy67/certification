from django.contrib import admin

from retail.models import Contact, Product, Member


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    pass

