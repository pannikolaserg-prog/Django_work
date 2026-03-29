from django.urls import path, include
from newapp.apps import NewappConfig
app_name = NewappConfig.name

urlpatterns = [
    path('',)
]
