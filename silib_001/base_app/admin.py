from django.contrib import admin
from .models import Category, Menu, Restaurant, Comment

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', ]

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'price']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'menu', 'open_to_close', 'is_package_possible', 'is_delivery_possible', 'is_card_possible', 'detail', 'latitude', 'longitude', 'register']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'price_star', 'taste_star', 'clean_star', 'dish_eaten', 'content', 'try_again', ]
