# Generated by Django 2.1 on 2018-10-23 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0010_auto_20181023_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
