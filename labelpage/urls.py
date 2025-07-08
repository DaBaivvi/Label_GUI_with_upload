from django.urls import path
from . import views
from homepage import views as homepage_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage_views.introduction, name = 'introduction'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name = 'login'),
    path('register/', homepage_views.register_view, name = 'register'),
    path('label/', views.label_redirect_view, name='label_redirect'),
    path('label/<int:csv_id>/', views.label_view, name='label'),
    path('go_to_last_labeled/', views.go_to_last_labeled_view, name='go_to_last_labeled'),
    path('load_resource_csvs/', views.load_resource_csvs, name='load_resource_csvs'),
]
