from django.shortcuts import render, redirect, get_object_or_404
from .models import Restaurant


# Create your views here.
def base(request):
    restaurants = Restaurant.objects.all()
    ctx = {
        'restaurants': restaurants,
    }
    return render(request, 'base_app/base.html', ctx)
