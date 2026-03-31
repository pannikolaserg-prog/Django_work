from django.contrib import messages
from django.shortcuts import render

from .forms import ContactForm


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
