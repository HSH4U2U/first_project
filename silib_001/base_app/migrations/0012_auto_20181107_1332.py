# Generated by Django 2.1 on 2018-11-07 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0011_auto_20181023_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=160, verbose_name='150자평'),
        ),
    ]