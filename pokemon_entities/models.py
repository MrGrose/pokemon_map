from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField("Имя покемона", max_length=200)
    title_en = models.TextField("Имя покемона на английском")
    title_jp = models.TextField("Имя покемона на японском")
    picture = models.ImageField("Картинка", null=True, blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="evolutions",
        verbose_name="Предыдущая эволюция"
    )
    next_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="previous_evolutions",
        blank=True,
        verbose_name="Следующая эволюция",
    )

    def __str__(self):
        return f'{self.title} (EN: {self.title_en}, JP: {self.title_jp})'


class PokemonEntity(models.Model):
    lon = models.FloatField("Долгота")
    lat = models.FloatField("Широта")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    appeared_at = models.DateTimeField("Время появления", null=True, blank=True)
    disappeared_at = models.DateTimeField("Время исчезновения", null=True, blank=True)
    description = models.TextField("Описание", blank=True)

    def __str__(self):
        return f'{self.pokemon.title} at ({self.lat}, {self.lon})'
