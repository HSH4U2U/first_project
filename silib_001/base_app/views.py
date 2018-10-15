from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Category, Comment
import json
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.
def base(request):
    restaurants = Restaurant.objects.all()
    categorys = Category.objects.all()

    # 카테고리 별 restaurants 추출
    category_restaurants = {}
    for category in categorys:
        category_restaurants[category] = Restaurant.objects.filter(category=category)

    ctx = {
        'restaurants': restaurants,
        'categorys': categorys,
        'category_restaurants': category_restaurants,
    }
    return render(request, 'base_app/base.html', ctx)

# def category(request, pk):
#     category = Category.objects.filter(pk=pk)
#     restaurants = Restaurant.objects.filter(category__pk=pk)
#     ctx = {
#         'restaurants': restaurants,
#         'category': category,
#     }
#     return render(request, 'base_app/category.html', ctx)


def restaurant(request, pk):
    restaurants = Restaurant.objects.all()
    selected_restaurant = Restaurant.objects.filter(pk=pk)
    comments = Comment.objects.filter(restaurant__pk=pk)
    ctx = {
        'restaurants': restaurants,
        'selected_restaurant': selected_restaurant,
        'comments': comments,
    }
    return render(request, 'base_app/restaurant.html', ctx)
