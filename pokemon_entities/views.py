import folium
from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils import timezone
from pokemon_entities.models import PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    active_pokemons_entities = PokemonEntity.objects.filter(
        appeared_at__lte=timezone.localtime(),
        disappeared_at__gte=timezone.localtime()
        ).select_related('pokemon')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_on_page = {}

    for pokemon_entity in active_pokemons_entities:
        image_url = request.build_absolute_uri(
            settings.MEDIA_URL + pokemon_entity.pokemon.picture.name
            ) if pokemon_entity.pokemon.picture else ''
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )
        if pokemon_entity.pokemon.id not in pokemons_on_page:
            pokemons_on_page[pokemon_entity.pokemon.id] = {
                'pokemon_id': pokemon_entity.pokemon.id,
                'img_url': image_url,
                'title_ru': pokemon_entity.pokemon.title,
            }

    all_pokemons_entities = PokemonEntity.objects.all().select_related('pokemon')
    for pokemon_entity in all_pokemons_entities:
        if pokemon_entity.pokemon.id not in pokemons_on_page:
            pokemons_on_page[pokemon_entity.pokemon.id] = {
                'pokemon_id': pokemon_entity.pokemon.id,
                'img_url': request.build_absolute_uri(
                    pokemon_entity.pokemon.picture.url)
                if pokemon_entity.pokemon.picture else None,
                'title_ru': pokemon_entity.pokemon.title,
            }

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': list(pokemons_on_page.values()),
    })


def show_pokemon(request, pokemon_id):
    pokemons = PokemonEntity.objects.filter(
        pokemon__id=pokemon_id).select_related(
            'pokemon',
            'pokemon__previous_evolution',
            'pokemon__next_evolution'
        )
    if not pokemons.exists():
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_data = {
        'img_url': None,
        'title_ru': None,
        'title_en': None,
        'title_jp': None,
        'previous_evolution': None,
        'next_evolution': None
    }
    media_url = settings.MEDIA_URL
    for pokemon_entity in pokemons:
        pokemon = pokemon_entity.pokemon
        pokemon_data['img_url'] = request.build_absolute_uri(
            media_url + pokemon.picture.name) if pokemon.picture else ''
        pokemon_data['title_ru'] = pokemon.title
        pokemon_data['title_en'] = pokemon.title_en
        pokemon_data['title_jp'] = pokemon.title_jp
        pokemon_data['description'] = pokemon_entity.description

        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_data['img_url']
        )

        if pokemon.previous_evolution:
            evolved_from_pokemon = pokemon.previous_evolution
            pokemon_data['previous_evolution'] = {
                'pokemon_id': evolved_from_pokemon.id,
                'title_ru': evolved_from_pokemon.title,
                'img_url': request.build_absolute_uri(
                    media_url + evolved_from_pokemon.picture.name)
                if evolved_from_pokemon.picture else ''
            }

        if pokemon.next_evolution:
            next_evolution_pokemon = pokemon.next_evolution
            pokemon_data['next_evolution'] = {
                'pokemon_id': next_evolution_pokemon.id,
                'title_ru': next_evolution_pokemon.title,
                'img_url': request.build_absolute_uri(
                    media_url + next_evolution_pokemon.picture.name)
                if next_evolution_pokemon.picture else ''
            }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })
