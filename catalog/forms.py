from django import forms
from django.forms import ModelForm

from catalog.models import Product


class ContactForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(label="Сообщение", widget=forms.Textarea)


from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Запрещенные слова
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Простая стилизация
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(f'Название содержит запрещенное слово: {word}')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        desc_lower = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in desc_lower:
                raise ValidationError(f'Описание содержит запрещенное слово: {word}')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Проверка размера (5 МБ)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Файл не должен превышать 5 МБ')

            # Проверка расширения
            ext = image.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                raise ValidationError('Можно загружать только JPG, JPEG или PNG')
        return image
