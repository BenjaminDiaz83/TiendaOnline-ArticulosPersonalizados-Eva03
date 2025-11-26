
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.lista_productos, name='home'), 
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'), 
    path('rastreo/', views.rastreo_pedido_form, name='rastreo_form'), 
    path('rastreo/<uuid:token>/', views.detalle_rastreo, name='detalle_rastreo'), 
    path('insumos/', views.lista_insumos, name='lista_insumos'),
    path('solicitar_producto/<int:pk>/', views.solicitar_producto_form, name='solicitar_producto'),
    
]