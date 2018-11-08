from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "base_app"

urlpatterns = [
    path('', views.base, name="base"),
    path('restaurant/<int:pk>', views.restaurant, name="restaurant"),
    path('all_comments', views.all_comments, name="all_comments"),
    path('restaurant/<int:pk>/write_comment', views.write_comment, name="write_comment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
