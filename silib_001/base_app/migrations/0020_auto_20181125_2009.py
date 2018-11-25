# Generated by Django 2.1 on 2018-11-25 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base_app', '0019_auto_20181109_2344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base_app.Comment', verbose_name='해당 후기')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='유저')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='like_user_set',
            field=models.ManyToManyField(blank=True, related_name='like_user_set', through='base_app.Like', to=settings.AUTH_USER_MODEL),
        ),
    ]