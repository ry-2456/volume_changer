from django.urls import path
from . import views

app_name = 'vca'

urlpatterns = [
    path('', views.index, name='index'),            
]
