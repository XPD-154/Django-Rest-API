from django.urls import path
from . import views
urlpatterns = [
    path('', views.getRoutes),
    path('clients/', views.getClients),
    path('client/<str:pk>/', views.getClient),
]
