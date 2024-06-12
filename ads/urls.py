from django.urls import path
from . import views
urlpatterns = [
     path("ads/",views.AdListView.as_view() , name='ads_list'),
     path('ads/<slug>/<pk>/', views.AdDetailView.as_view(), name='ad_detail'),
     path('' , views.empty_url)
]