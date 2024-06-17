from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify_code/', views.VerifyCodeView.as_view(), name='verify_code'),
    path('logout/', views.logout_view, name='logout'),
]