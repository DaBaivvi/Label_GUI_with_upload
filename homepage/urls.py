from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
from labelpage import views as labelpage_views
from . import views

urlpatterns = [
    path('', views.introduction, name='introduction'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('labelpage/', include('labelpage.urls')),
]