from django.contrib import admin
from django.urls import path
from barcodereader import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.detect, name="index"),
    path("camera_feed/", views.camera_feed, name="camera_feed"),
]
