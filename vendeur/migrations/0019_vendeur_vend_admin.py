# Generated by Django 2.1 on 2018-09-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendeur', '0018_remove_vendeur_vend_coockie_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendeur',
            name='vend_admin',
            field=models.IntegerField(default=0),
        ),
    ]
