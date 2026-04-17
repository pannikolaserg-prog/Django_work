from django.urls import path

from . import views
from catalog.views import product_list

app_name = "catalog"

urlpatterns = [
    # path("", views.home, name="home"),
    # path("contacts/", views.contacts, name="contacts"),
    path("", product_list)
]
