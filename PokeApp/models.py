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
    
    # Campo region del Pokemon
    region = models.CharField(max_length=100)
    
    #Camppo atributo principal Pokemon
    mejor_atributo = models.CharField(max_length=100)
    
    #Campo atributo descripcion Pokemon
    descripcion_poke = models.CharField(max_length=100)
    
    #Campo especie Pokemon
    especie_poke = models.CharField(max_length=100)
    
    #Campo habilidades Pokemon
    habilidades_poke = models.CharField(max_length=100)

    # Método para mostrar el nombre del Pokémon
    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre_completo = models.CharField(max_length=255)
    
    celular = models.CharField(max_length=20, unique=True)
    
    email = models.EmailField(unique=True, null="False")
    
    contrasena = models.CharField(max_length=128)
    
    def __str__(self):
        return self.nombre_completo
