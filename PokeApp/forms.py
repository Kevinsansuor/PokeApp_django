# forms.py

from django import forms

class FormularioPokeApp(forms.Form):
    search_term = forms.CharField(label='Buscar Pokémon por nombre o ID', max_length=100, widget=forms.TextInput(attrs={'class': 'busquedaPokemon'}))
