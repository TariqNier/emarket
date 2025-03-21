# Generated by Django 5.1 on 2024-08-25 13:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('desc', models.TextField(default='', max_length=100, verbose_name='Description')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('brand', models.CharField(default='', max_length=200)),
                ('category', models.CharField(choices=[('computers', 'Computers'), ('food', 'Food'), ('kids', 'Kids'), ('utilites', 'Utilites'), ('Home', 'Home')], max_length=200)),
                ('rating', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('stock', models.IntegerField(default=0)),
                ('createAt', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
