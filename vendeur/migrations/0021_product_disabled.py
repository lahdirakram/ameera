# Generated by Django 2.1 on 2018-10-02 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendeur', '0020_auto_20180929_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='disabled',
            field=models.IntegerField(default=0),
        ),
    ]
