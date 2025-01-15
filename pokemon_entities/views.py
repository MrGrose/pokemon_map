import json

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
        )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons_on_page = {}

    for pokemon_entity in active_pokemons_entities:
        pokemon = pokemon_entity.pokemon
        if pokemon.picture:
            image_url = request.build_absolute_uri(
                settings.MEDIA_URL + pokemon.picture.name)
        else:
            image_url = ''
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            image_url
        )

    all_pokemons_entities = PokemonEntity.objects.all()
    for pokemon_entity in all_pokemons_entities:
        pokemon = pokemon_entity.pokemon
        if pokemon.id not in pokemons_on_page:
            pokemons_on_page[pokemon.id] = {
                'pokemon_id': pokemon.id,
                'img_url': request.build_absolute_uri(
                    pokemon.picture.url
                    ) if pokemon.picture else None,
                'title_ru': pokemon.title,
            }

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': list(pokemons_on_page.values()),
    })


def show_pokemon(request, pokemon_id):
    pokemons = PokemonEntity.objects.filter(pokemon__id=pokemon_id)
    if not pokemons.exists():
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_data = {
        'img_url': None,
        'title_ru': None,
        'title_en': None,
        'title_jp': None,
        'entities': [],
        'evolved_from': None
    }
    for pokemon_entity in pokemons:
        pokemon = pokemon_entity.pokemon
        if pokemon.picture:
            pokemon_data['img_url'] = request.build_absolute_uri(
                settings.MEDIA_URL + pokemon.picture.name
            )
        else:
            pokemon_data['img_url'] = ''
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
        pokemon_data['entities'].append({
            'lat': pokemon_entity.lat,
            'lon': pokemon_entity.lon,
            'level': pokemon_entity.level,
            'health': pokemon_entity.health,
            'attack': pokemon_entity.attack,
            'defence': pokemon_entity.defence,
            'stamina': pokemon_entity.stamina,
        })
        if pokemon.evolved_from:
            evolved_from_pokemon = pokemon.evolved_from
            pokemon_data['evolved_from'] = {
                'id': evolved_from_pokemon.id,
                'title_ru': evolved_from_pokemon.title,
                'img_url': request.build_absolute_uri(settings.MEDIA_URL + evolved_from_pokemon.picture.name) if evolved_from_pokemon.picture else ''
            }

        if pokemon.evolutions.exists():
            next_evolution_pokemon = pokemon.evolutions.first()
            pokemon_data['next_evolution'] = {
                'pokemon_id': next_evolution_pokemon.id,
                'title_ru': next_evolution_pokemon.title,
                'img_url': request.build_absolute_uri(settings.MEDIA_URL + next_evolution_pokemon.picture.name) if next_evolution_pokemon.picture else ''
            }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })
