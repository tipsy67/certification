from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response

from retail.models import Member, Contact, Product
from retail.permissions import IsActive
from retail.serializer import MemberSerializer, ContactSerializer, ProductSerializer


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

    def list(self, request, *args, **kwargs):
        queryset = Member.objects.prefetch_related('contacts')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



