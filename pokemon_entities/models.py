from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    title_en = models.TextField()
    title_jp = models.TextField()
    picture = models.ImageField(null=True, blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evolutions'
    )
    next_evolution = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        related_name='previous_evolutions',
        blank=True
    )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    lon = models.FloatField()
    lat = models.FloatField()
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    attack = models.IntegerField(null=True, blank=True)
    defence = models.IntegerField(null=True, blank=True)
    stamina = models.IntegerField(null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.pokemon.title
