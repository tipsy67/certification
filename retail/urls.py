from django.urls import include, path
from rest_framework import routers

from retail.apps import RetailConfig
from retail.views import ContactViewSet, MemberViewSet

app_name = RetailConfig.name

router_member = routers.DefaultRouter()
router_member.register(r'member', MemberViewSet, basename="Member")

router_contact = routers.DefaultRouter()
router_contact.register(r'contact', ContactViewSet, basename="contact")

urlpatterns = [] + router_member.urls + router_contact.urls
