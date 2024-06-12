from django.urls import path
from . import views
urlpatterns = [
<<<<<<< HEAD
     path("ads/",views.AdListView.as_view() , name='ads_list'),
     path('ads/<slug>/<pk>/', views.AdDetailView.as_view(), name='ad_detail'),
     path('' , views.empty_url)
=======
     path("",views.AdListView.as_view()),
     path('<pk>/', views.AdDetailView.as_view(), name='ad_detail'),
>>>>>>> 25138200c661c10e0f2ad703afa3b5e2c53041a1
]