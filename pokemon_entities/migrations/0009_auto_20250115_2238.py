# Generated by Django 3.1.14 on 2025-01-15 19:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0008_pokemon_next_evolutions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='evolved_from',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolution', to='pokemon_entities.pokemon'),
        ),
        migrations.RemoveField(
            model_name='pokemon',
            name='next_evolutions',
        ),
        migrations.AddField(
            model_name='pokemon',
            name='next_evolutions',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous_evolution', to='pokemon_entities.pokemon'),
        ),
    ]
