from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    picture = models.ImageField(null=True, default='default_pokemon.png')

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True)
    health = models.IntegerField(null=True)
    attack = models.IntegerField(null=True)
    defence = models.IntegerField(null=True)
    stamina = models.IntegerField(null=True)

    def __str__(self):
        return f'Pokemon at ({self.lat}, {self.lon}) - {self.pokemon.title}'
