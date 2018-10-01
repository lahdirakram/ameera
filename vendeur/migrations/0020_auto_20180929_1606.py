# Generated by Django 2.1.1 on 2018-09-29 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendeur', '0019_vendeur_vend_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='prod_test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('qte', models.IntegerField(default=1)),
                ('prod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendeur.Product')),
            ],
        ),
        migrations.DeleteModel(
            name='test',
        ),
    ]
