from django.shortcuts import render
from django.urls import path, include
from rest_framework import viewsets
from rest_framework.response import Response

from retail.models import Member, Contact
from retail.serializer import MemberSerializer, ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def list(self, request, *args, **kwargs):
        queryset = Member.objects.prefetch_related('contacts')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



