from copy import copy

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from retail.forms import MemberForm
from retail.models import Contact, Member, Product


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'country',
        'city',
        'created_at',
        'updated_at',
        'member',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ('copy_product',)
    search_fields = ('name',)

    @admin.action(description="скопировать выделенные продукты")
    def copy_product(self, request, queryset):
        count = 0
        for instance in queryset:
            new_instance = copy(instance)
            new_instance.pk = None
            new_instance.save()
            count += 1

        self.message_user(request, f"Скопировано {count} записи(ей).")


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    form = MemberForm
    list_display = (
        'pk',
        'name',
        'city',
        'display_member_type',
        'member_level',
        'accounts_payable',
        'updated_at',
        'supplier_link',
    )
    list_display_links = ('name',)
    actions = ('clear_accounts_payable',)

    search_fields = ('name', 'contacts__city')
    list_filter = ('name', 'contacts__city')

    @admin.action(description="очистить задолженность перед поставщиком")
    def clear_accounts_payable(self, request, queryset):
        count = queryset.update(accounts_payable=0)
        self.message_user(request, f"Изменено {count} записи(ей).")

    @admin.display(description='поставщик')
    def supplier_link(self, instance):
        if instance.supplier is not None:
            url = reverse('admin:retail_member_change', args=[instance.supplier.pk])
            return format_html('<a href="{}">{}</a>', url, instance.supplier.name)
        return "нет поставщика"

    @admin.display(description='город')
    def city(self, instance):
        contact = instance.contacts.all().first()
        if contact is not None:
            url = reverse('admin:retail_contact_change', args=[contact.pk])
            return format_html('<a href="{}">{}</a>', url, contact.city)
        return "нет контактов"
