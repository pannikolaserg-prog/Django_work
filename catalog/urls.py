from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', cache_page(60)(views.ProductDetailView.as_view()), name='product_detail'),
    path('products/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),
    path('products/<int:pk>/publish-toggle/', views.ProductPublishToggleView.as_view(), name='product_publish_toggle'),
]