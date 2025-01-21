
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api-retail/", include("retail.urls", namespace="retail")),
]
