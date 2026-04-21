from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('get_logs/', views.get_logs, name='get_logs'),
    path('view_db/', views.view_db, name="view_db"),
    path('statistics/', views.statistics, name="statistics"),
    path('get_error_stats/', views.get_error_stats, name="get_error_stats"),
    path('get_color_stats/', views.get_color_stats, name="get_color_stats"),
    path('get_prod_stats/', views.get_prod_stats, name="get_prod_stats"),
]