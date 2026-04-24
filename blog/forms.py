from django import forms
from .models import MyBlog

class MyBlogForm(forms.ModelForm):
    class Meta:
        model = MyBlog
        fields = ['name', 'description', 'preview', 'is_published']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите заголовок'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Введите содержание'}),
            'preview': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
