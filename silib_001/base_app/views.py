from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant, Category


# Create your views here.
def base(request):
    restaurants = Restaurant.objects.all()
    categorys = Category.objects.all()
    ctx = {
        'restaurants': restaurants,
        'categorys': categorys,
    }
    return render(request, 'base_app/base.html', ctx)

def category(request, pk):
    category = Category.objects.filter(pk=pk)
    restaurants = Restaurant.objects.filter(category__pk=pk)
    ctx = {
        'restaurants': restaurants,
        'category': category,
    }
    return render(request, 'base_app/category.html', ctx)
