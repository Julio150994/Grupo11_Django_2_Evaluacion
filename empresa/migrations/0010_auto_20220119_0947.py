# Generated by Django 3.1.2 on 2022-01-19 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0009_auto_20220118_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='foto',
            field=models.ImageField(upload_to='static/assets/imagenes/', verbose_name='Foto'),
        ),
    ]