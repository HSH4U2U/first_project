# Generated by Django 2.1 on 2018-11-09 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0018_auto_20181109_2338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='is_eating_lonely_possible',
            new_name='is_card_possible',
        ),
    ]
