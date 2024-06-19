from django.urls import path
from . import views
urlpatterns = [
     path('create_business/', views.CreateBusinessView.as_view(), name='create_business'),
]