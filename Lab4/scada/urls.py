from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('increment_scores/', views.increment_scores, name='increment_scores'),
]