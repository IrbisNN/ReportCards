# Generated by Django 5.1.1 on 2025-03-20 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0008_studentclasse_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='slug',
            field=models.SlugField(max_length=250, null=True, unique=True),
        ),
    ]
