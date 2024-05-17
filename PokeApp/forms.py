# forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class FormularioPokeApp(forms.Form):
    search_term = forms.CharField(label='Buscar Pokémon por nombre o ID', max_length=100, widget=forms.TextInput(attrs={'class': 'busquedaPokemon'}))

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1'] 
