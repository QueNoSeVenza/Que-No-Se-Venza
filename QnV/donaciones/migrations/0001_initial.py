# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-06-14 14:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.CharField(max_length=60)),
                ('fecha_vencimiento', models.DateField()),
                ('stock', models.CharField(default='En Espera', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60)),
                ('concentracion_gramos', models.CharField(max_length=60)),
                ('laboratorio', models.CharField(max_length=60)),
                ('droga', models.CharField(max_length=60)),
                ('funcion', models.CharField(choices=[('Analgesico', 'Analgesico'), ('Androgenos', 'Androgenos')], default='Null', max_length=60)),
                ('prescripcion', models.BooleanField(default=False)),
                ('tipo', models.CharField(choices=[('Pastillas', 'Pastillas'), ('Jarabe', 'Jarabe'), ('Gotas', 'Gotas')], default=0, max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Pedir',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donaciones.Medicamento')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='donacion',
            name='medicamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donaciones.Medicamento'),
        ),
        migrations.AddField(
            model_name='donacion',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]