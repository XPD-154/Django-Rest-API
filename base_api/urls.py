from django.urls import path
from . import views
urlpatterns = [
    path('', views.getRoutes),
    path('clients/', views.getClients),
    path('client/<str:pk>', views.getClient),
    path('create_client/', views.addClient),
    path('update_client/<str:pk>', views.updateClient),
    path('delete_client/<str:pk>', views.deleteClient),
]
