from django.db import models

# Create your models here.
class Pokemon(models.Model):
    # Campo para el nombre del Pokémon
    nombre = models.CharField(max_length=255, unique=True)

    # Campo para el número de la Pokédex
    numero_pokedex = models.IntegerField(unique=True, primary_key=True)

    # Campo para el tipo de Pokémon (Agua, Fuego, Planta, etc.)
    tipo = models.CharField(max_length=255)

    # Campo para la generación a la que pertenece (Primera, Segunda, etc.)
    generacion = models.IntegerField()

    # Campo para la imagen del Pokémon (URL o ruta local)
    imagen = models.URLField(max_length=255, blank=True)
    

    # Método para mostrar el nombre del Pokémon
    def __str__(self):
        return self.nombre
