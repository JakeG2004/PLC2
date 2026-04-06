from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('get_logs/', views.get_logs, name='get_logs'),
    path('view_db/', views.view_db, name="view_db"),
]