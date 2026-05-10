from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


class ProductListView(ListView):  # Общедоступный
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, DetailView):  # Только для авторизованных
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"
    login_url = 'users:login'


class ProductCreateView(LoginRequiredMixin, CreateView):  # Только для авторизованных
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'


class ProductUpdateView(LoginRequiredMixin, UpdateView):  # Только для авторизованных
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'


class ProductDeleteView(LoginRequiredMixin, DeleteView):  # Только для авторизованных
    model = Product
    template_name = "catalog/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'
