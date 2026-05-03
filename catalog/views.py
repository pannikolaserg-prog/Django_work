from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ContactForm, ProductForm
from .models import Product


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


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm  # Используем форму с валидацией вместо fields
    template_name = "products/product_form.html"
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно создан!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме")
        return super().form_invalid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm  # Используем форму с валидацией
    template_name = "products/product_form.html"
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        messages.success(self.request, "Продукт успешно обновлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Исправьте ошибки в форме")
        return super().form_invalid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "products/product_confirm_delete.html"
    success_url = reverse_lazy('catalog:product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Продукт успешно удален!")
        return super().delete(request, *args, **kwargs)
