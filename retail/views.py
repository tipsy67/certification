from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from retail.filters import MemberFilter
from django.db.models import Prefetch
from retail.models import Contact, Member, Product
from retail.permissions import IsActive
from retail.serializer import (ContactSerializer, MemberSerializer,
                               ProductSerializer)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsActive, IsAuthenticated)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (IsActive, IsAuthenticated)


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = (IsActive, IsAuthenticated)

    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = MemberFilter


    def list(self, request, *args, **kwargs):
        contacts_qs = Contact.objects.all()
        country = request.query_params.get('country')
        if country:
            contacts_qs = contacts_qs.filter(country=country)
            queryset = Member.objects.prefetch_related(Prefetch('contacts',contacts_qs)).exclude(contacts=None)
        else:
            queryset = Member.objects.prefetch_related(Prefetch('contacts',contacts_qs))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
