from django.urls import path
from . import views
from django.contrib import admin  

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),  
    path('buscar/', views.search_pokemon, name='buscar_pokemon'),
]
