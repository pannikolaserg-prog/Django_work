from django.urls import path, include
from catalog.apps import NewappConfig
from catalog.views import home

app_name = NewappConfig.name

urlpatterns = [
    path('', home, name='home')
]
