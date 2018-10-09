from django.urls import path
from . import views

app_name = "base_app"

urlpatterns = [
    path('', views.base, name="base"),
#     path('product<int:pk>', views.product, name="product"),
#     path('category', views.category_main, name="category_main"),
    path('restaurant/<int:pk>', views.restaurant, name="restaurant"),
]

