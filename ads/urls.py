from django.urls import path
from . import views
urlpatterns = [
     path("",views.AdListView.as_view()),
     path('<pk>/', views.AdDetailView.as_view(), name='ad_detail'),
]