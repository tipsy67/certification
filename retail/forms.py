from django import forms
from django.core.exceptions import ValidationError

from retail.models import Member
from retail.src.field_validators import are_fields_valid


class MemberForm(forms.ModelForm):
    model = Member
    fields = ('pk', 'member_type', 'supplier')

    def clean(self, *args, **kwargs):
        cleaned_data = super().clean()
        pk = self.instance.pk
        valid, context = are_fields_valid(cleaned_data, pk)
        if not valid:
            raise ValidationError(context)

        return cleaned_data
