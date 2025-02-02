# Generated by Django 3.1.14 on 2025-01-15 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_auto_20250115_2203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemonentity',
            name='next_evolution',
        ),
        migrations.RemoveField(
            model_name='pokemonentity',
            name='previous_evolution',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='evolved_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='evolutions', to='pokemon_entities.pokemon'),
        ),
    ]
