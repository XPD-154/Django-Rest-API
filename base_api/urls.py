from django.urls import path
from . import views
urlpatterns = [
    path('', views.getRoutes),
    path('clients/', views.getClients),
    path('client/<str:pk>', views.getClient),
    path('specific_client/', views.getSpClient),
    path('check_client_xl/', views.checkClientXl),
    path('check_client_js/', views.checkClientJs),
    path('create_client/', views.addClient),
    path('update_client/<str:pk>', views.updateClient),
    path('delete_client/<str:pk>', views.deleteClient),
    path('login_test/', views.login_test),
    path('api_key/<str:cid>', views.createClientApiKey),
]
