from django.contrib import messages
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import ContactForm
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


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price']
    template_name = "products/product_form.html"
    success_url = reverse_lazy('catalog:product_list" ')
