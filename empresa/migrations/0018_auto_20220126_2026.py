# Generated by Django 3.1.2 on 2022-01-26 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0017_auto_20220124_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoria',
            name='foto',
            field=models.ImageField(upload_to='img_categorias/', verbose_name='Foto'),
        ),
    ]
