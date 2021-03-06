# Generated by Django 2.1 on 2018-10-01 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='dish_category',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='dish_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='menu',
            old_name='dish_price',
            new_name='price',
        ),
        migrations.AddField(
            model_name='restaurant',
            name='latitude',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='restaurant',
            name='longitude',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='is_delivery_possible',
            field=models.TextField(blank=True, choices=[('가능', '가능'), ('불가능', '불가능')], verbose_name='배달 가능 여부'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='is_eating_lonely_possible',
            field=models.TextField(blank=True, choices=[('가능', '가능'), ('불가능', '불가능')], verbose_name='혼밥 가능 여부'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='is_package_possible',
            field=models.TextField(blank=True, choices=[('가능', '가능'), ('불가능', '불가능')], verbose_name='포장 가능 여부'),
        ),
    ]
