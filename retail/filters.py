import django_filters

from retail.models import Member


class MemberFilter(django_filters.FilterSet):
    country = django_filters.CharFilter(
        field_name='contacts__country', lookup_expr='icontains'
    )

    class Meta:
        model = Member
        fields = ['country']

    @property
    def qs(self):
        parent = super().qs
        # author = getattr(self.request, 'user', None)

        return parent
