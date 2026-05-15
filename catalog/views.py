from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin  # Добавьте для авторизации
from .forms import ContactForm, ProductForm
from .models import Product
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class HomeView(TemplateView):
    template_name = "products/home.html"


class ContactView(FormView):
    template_name = "products/contacts.html"
    form_class = ContactForm
    success_url = reverse_lazy("catalog:contacts")

    def form_valid(self, form):
        messages.success(self.request, f"{form.cleaned_data['name']}, ваше сообщение отправлено!")
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, DetailView):  # 🔥 Добавлен LoginRequiredMixin
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
    login_url = 'users:login'  # 🔥 Добавлено для редиректа


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.is_published = False
        messages.success(self.request, "Продукт создан и отправлен на модерацию!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме")
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):  # 🔥 Добавлен LoginRequiredMixin
    model = Product
    form_class = ProductForm
    template_name = "products/product_form.html"
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'  # 🔥 Добавлено для редиректа

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме")
        return super().form_invalid(form)

    def test_func(self):
        product = self.get_object()
        is_owner = product.owner == self.request.user
        is_moderator = self.request.user.has_perm('catalog.can_unpublish_product')
        return is_owner or is_moderator

    def handle_no_permission(self):
        messages.error(self.request, "У вас нет прав на удаление этого продукта!")
        return redirect('catalog:product_list')

class ProductDeleteView(LoginRequiredMixin, DeleteView):  # 🔥 Добавлен LoginRequiredMixin
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:product_list')
    login_url = 'users:login'  # 🔥 Добавлено для редиректа

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Продукт успешно удален!")
        return super().delete(request, *args, **kwargs)

class ProductPublishToggleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    fields = []
    template_name = "catalog/product_confirm_publish.html"
    login_url = 'users:login'

    def test_func(self):
        return self.request.user.has_perm('catalog.can_unpublish_product')

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        product.is_published = not product.is_published
        product.save()
        status = "опубликован" if product.is_published else "снят с публикации"
        messages.success(request, f"Продукт '{product.name}' {status}!")
        return redirect('catalog:product_list')
