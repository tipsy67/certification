from django.urls import include, path
from rest_framework import routers

from retail.apps import RetailConfig
from retail.views import (CityViewSet, ContactViewSet, CountryViewSet,
                          MemberViewSet, ProductViewSet)

app_name = RetailConfig.name

router_member = routers.DefaultRouter()
router_member.register(r'member', MemberViewSet, basename="member")

router_contact = routers.DefaultRouter()
router_contact.register(r'contact', ContactViewSet, basename="contact")

router_country = routers.DefaultRouter()
router_country.register(r'country', CountryViewSet, basename="country")

router_city = routers.DefaultRouter()
router_city.register(r'city', CityViewSet, basename="city")

router_product = routers.DefaultRouter()
router_product.register(r'product', ProductViewSet, basename="product")

urlpatterns = (
    []
    + router_member.urls
    + router_contact.urls
    + router_country.urls
    + router_city.urls
    + router_product.urls
)
