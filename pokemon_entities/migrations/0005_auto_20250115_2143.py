# Generated by Django 3.1.14 on 2025-01-15 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0004_auto_20250115_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='pokemon',
            name='title_en',
            field=models.TextField(default='default title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokemon',
            name='title_jp',
            field=models.TextField(default='default title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pokemonentity',
            name='description',
            field=models.TextField(default='default title'),
            preserve_default=False,
        ),
    ]
