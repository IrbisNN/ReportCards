# Generated by Django 5.1.1 on 2025-03-18 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_student_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentclasse',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cards.school'),
        ),
    ]
