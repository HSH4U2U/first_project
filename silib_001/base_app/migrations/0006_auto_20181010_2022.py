# Generated by Django 2.1 on 2018-10-10 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0005_category_category_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base_app.Category', verbose_name='카테고리'),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base_app.Menu', verbose_name='음식점 메뉴'),
        ),
    ]
