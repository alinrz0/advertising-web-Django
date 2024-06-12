from django.urls import path
from . import views
urlpatterns = [
     path('', views.about_us_view, name="about_us"),
]