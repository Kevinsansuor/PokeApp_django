# forms.py

from django import forms
from .models import Usuario

class FormularioPokeApp(forms.Form):
    search_term = forms.CharField(label='Buscar Pokémon por nombre o ID', max_length=100, widget=forms.TextInput(attrs={'type': 'search', 'name': 'search', 'placeholder': 'Nombre o Id', 'class': 'busquedaPokemon'}))

class RegistroUsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'celular', 'email', 'contrasena']
