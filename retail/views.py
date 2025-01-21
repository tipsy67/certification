from django.shortcuts import render
from django.urls import path, include
from rest_framework import viewsets

from retail.models import Member, Contact
from retail.serializer import MemberSerializer, ContactSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer



