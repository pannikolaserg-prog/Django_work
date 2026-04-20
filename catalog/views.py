from itertools import product

from django.contrib import messages
from django.shortcuts import render, get_object_or_404

from .forms import ContactForm
from .models import Product


def home(request):
    return render(request, "home.html")


def contacts(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Данные успешно получены
            name = form.cleaned_data["name"]
            messages.success(request, f"{name}, ваше сообщение отправлено!")
            form = ContactForm()  # Очищаем форму
    else:
        form = ContactForm()

    return render(request, "contacts.html", {"form": form})


def product_list(request):
    products = Product.objects.all()
    context = {"products": products}

    return render(request, "products_list.html", context)

def products_detail(request, pk):
    product =get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, "products_detail.html", context)
