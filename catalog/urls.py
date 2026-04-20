# catalog/urls.py
from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),                          # Главная
    path("products/", views.product_list, name="product_list"), # Список товаров
    path("products/<int:pk>/", views.products_detail, name="products_detail"),  # Детали товара
    path("contacts/", views.contacts, name="contacts"),         # Контакты
]
