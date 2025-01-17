# Generated by Django 3.1.14 on 2025-01-17 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Имя покемона')),
                ('title_en', models.CharField(max_length=200, verbose_name='Имя покемона на английском')),
                ('title_jp', models.CharField(max_length=200, verbose_name='Имя покемона на японском')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Картинка')),
                ('next_evolution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolutions', to='pokemon_entities.pokemon', verbose_name='Следующая эволюция')),
                ('previous_evolution', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_evolutions', to='pokemon_entities.pokemon', verbose_name='Предыдущая эволюция')),
            ],
        ),
        migrations.CreateModel(
            name='PokemonEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lon', models.FloatField(verbose_name='Долгота')),
                ('lat', models.FloatField(verbose_name='Широта')),
                ('appeared_at', models.DateTimeField(blank=True, null=True, verbose_name='Время появления')),
                ('disappeared_at', models.DateTimeField(blank=True, null=True, verbose_name='Время исчезновения')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('level', models.IntegerField(blank=True, null=True, verbose_name='Уровень')),
                ('health', models.IntegerField(blank=True, null=True, verbose_name='Здоровье')),
                ('attack', models.IntegerField(blank=True, null=True, verbose_name='Атака')),
                ('defence', models.IntegerField(blank=True, null=True, verbose_name='Защита')),
                ('stamina', models.IntegerField(blank=True, null=True, verbose_name='Выносливость')),
                ('pokemon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pokemon', to='pokemon_entities.pokemon', verbose_name='Покемон')),
            ],
        ),
    ]
