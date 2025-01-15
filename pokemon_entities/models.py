from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    picture = models.ImageField(null=True, upload_to='media')

    def __str__(self):
        return f'{self.title}'


class PokemonEntity(models.Model):
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return f'{self.longitude} {self.latitude}'