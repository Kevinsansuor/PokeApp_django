from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .forms import FormularioPokeApp, RegistroUsuarioForm
import requests
from .models import Pokemon, Usuario

def signup(request):
    if request.method == 'POST':
        form_reg = RegistroUsuarioForm(request.POST)
        if form_reg.is_valid():
            nombre_completo = form_reg.cleaned_data['nombre_completo']
            celular = form_reg.cleaned_data['celular']
            email = form_reg.cleaned_data['email']
            contrasena = form_reg.cleaned_data['contrasena']
            usuario = Usuario(nombre_completo=nombre_completo, celular=celular, email=email, contrasena=contrasena)
            usuario.save()
            return redirect('index')  # Redireccionar a la página principal después del registro
    return render(request, 'registro.html', {'form_reg': RegistroUsuarioForm()})

def index(request):
    
    pet_lang = requests.get("https://pokeapi.co/api/v2/language/7/")
    lang_es = pet_lang.json()


    #Funcion index hace una petición
    pokemon_info = None
    #variable pokemon info vacia
    evolutions = []
    #Array de evoluciones
    form = FormularioPokeApp()
    
    usuario_nombre = None
    
    
    if request.method == 'POST':
        #Si dentro del index se hace una petición de Post
        form = FormularioPokeApp(request.POST)
        
        #1
        #Se valida el formulario
        if form.is_valid():
            #Desde la variable search_term se almacena el formulario con el contenido limpio
            search_term = form.cleaned_data['search_term']
            #La función cleaned_dat convierte strings en objetos, además de contener librerias para validaciones de formularios
            try:
                
                #Busqueda en la base de daos
                
                Pokemon_model = Pokemon.objects.get(nombre__iexact=search_term)
                
                pokemon_info= {
                    'name': Pokemon_model.nombre,
                    'id': Pokemon_model.numero_pokedex,
                    'types': Pokemon_model.tipo,
                    'image_url': Pokemon_model.imagen,
                    'attribute': Pokemon_model.mejor_atributo,
                    'description': Pokemon_model.descripcion_poke,
                    'species': Pokemon_model.especie_poke,
                    'habilities': Pokemon_model.habilidades_poke
                } 
                
            except Pokemon.DoesNotExist:
                
                try:    
                    
                    pokemon_id = int(search_term)
                    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
                except ValueError:
                    # Buscar por nombre
                    url = f'https://pokeapi.co/api/v2/pokemon/{search_term.lower()}/'
            
            response = requests.get(url)
            
            if response.status_code == 200:
                pokemon_data = response.json()
                
                """ for name_entry in bulbasaur_data['names']:
                    if name_entry['language']['name'] == 'es':
                        print(f"Bulbasaur in Spanish is: {name_entry['name']}") """
                        
                pokemon_data = response.json()
                species_url = pokemon_data['species']['url']
                species_response = requests.get(species_url)
                if species_response.status_code == 200:
                    species_data = species_response.json()
                    pokemon_info = {
                            'name': pokemon_data['name'].capitalize(),
                            'id': pokemon_data['id'],
                            'types': ', '.join([t['type']['name'].capitalize() for t in pokemon_data['types']]),
                            'image_url': pokemon_data['sprites']['front_default'],
                            'attribute': 'N/A',  
                            'description': species_data['flavor_text_entries'][0]['flavor_text'],
                            'species': species_data['genera'][0]['genus'],
                            'habilities': ', '.join([a['ability']['name'].capitalize() for a in pokemon_data['abilities']])
                    }
                
                """ Si hay Ok, guardar en la base de datos"""
                
                Pokemon_instance = Pokemon(
                    nombre = pokemon_info['name'],
                    numero_pokedex = pokemon_info['id'],
                    tipo = pokemon_info['types'],
                    generacion = 1,
                    imagen = pokemon_info['image_url'],
                    region="Kanto",
                    mejor_atributo=pokemon_info['attribute'],
                    descripcion_poke=pokemon_info['description'],
                    especie_poke=pokemon_info['species'],
                    habilidades_poke=pokemon_info['habilities'],
                )
                
                Pokemon_instance.save()
                
                
            
                evolution_chain_url = pokemon_data['species']['url']
                evolution_chain_response = requests.get(evolution_chain_url)
                #Si la respuesta es exitosa
                if evolution_chain_response.status_code == 200:
                    #Aca se obtienen los datos de la evolucion del pokemon
                    evolution_chain_data = evolution_chain_response.json()
                    evolution_chain_id = evolution_chain_data['evolution_chain']['url'].split('/')[-2]
                    evolution_chain_detail_url = f'https://pokeapi.co/api/v2/evolution-chain/{evolution_chain_id}/'
                    evolution_chain_detail_response = requests.get(evolution_chain_detail_url)
                    #Si la respuesta es exitosa
                    if evolution_chain_detail_response.status_code == 200:
                        #Se obtienen los datos detallados de la evolucion del pokemon
                        evolution_chain_detail_data = evolution_chain_detail_response.json()
                        chain = evolution_chain_detail_data['chain']
                        
                def get_pokemon_image(pokemon_name):
                            pokemon_url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/'
                            pokemon_response = requests.get(pokemon_url)
                            if pokemon_response.status_code == 200:
                                pokemon_data = pokemon_response.json()
                                return pokemon_data['sprites']['front_default']
                            return None
                        
                def extract_evolution_info(evolution, pokemon_name):
                            evolution_name = evolution['species']['name'].capitalize()
                            if evolution_name != pokemon_name:  # Verificamos si la evolución es diferente al Pokémon actual
                                evolutions.append({'name': evolution_name, 'image_url': get_pokemon_image(evolution_name)})
                            if 'evolves_to' in evolution:
                                for sub_evolution in evolution['evolves_to']:
                                    extract_evolution_info(sub_evolution, pokemon_name)
                        
                        #Aca se extrae la informacion de la evolucion del pokemon
                extract_evolution_info(chain, pokemon_info['name'])  # Pasamos el nombre del Pokémon actual
    
    return render(request, 'index.html', {'form': form, 'pokemon_info': pokemon_info, 'evolutions': evolutions})
    



    # Si no se envió el formulario o hubo un error en la búsqueda, mostramos la página de inicio con el formulario
    return render(request, 'search_pokemon.html', {'form': form})

