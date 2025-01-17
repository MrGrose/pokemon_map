from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name="Имя покемона", max_length=200)
    title_en = models.CharField(verbose_name="Имя покемона на английском", max_length=200)
    title_jp = models.CharField(verbose_name="Имя покемона на японском", max_length=200)
    picture = models.ImageField(verbose_name="Картинка", null=True, blank=True)
    previous_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="previous_evolutions",
        verbose_name="Предыдущая эволюция"
    )
    next_evolution = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="next_evolutions",
        blank=True,
        verbose_name="Следующая эволюция",
    )

    def __str__(self):
        return f'{self.title} (EN: {self.title_en}, JP: {self.title_jp})'


class PokemonEntity(models.Model):
    lon = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name="pokemon", verbose_name="Покемон")
    appeared_at = models.DateTimeField(verbose_name="Время появления", null=True, blank=True)
    disappeared_at = models.DateTimeField(verbose_name="Время исчезновения", null=True, blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    level = models.IntegerField(verbose_name="Уровень", null=True, blank=True)
    health = models.IntegerField(verbose_name="Здоровье", null=True, blank=True)
    attack = models.IntegerField(verbose_name="Атака", null=True, blank=True)
    defence = models.IntegerField(verbose_name="Защита", null=True, blank=True)
    stamina = models.IntegerField(verbose_name="Выносливость", null=True, blank=True)

    def __str__(self):
        return f'{self.pokemon.title} ({self.lat}, {self.lon})'
