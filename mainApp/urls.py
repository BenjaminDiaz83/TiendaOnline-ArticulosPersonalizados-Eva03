
from django.urls import path, include
from . import views
from . import api_views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'insumos', api_views.InsumoViewSet, basename='insumos')
router.register(r'pedidos', api_views.PedidoCreateUpdateViewSet, basename='pedidos')

urlpatterns = [
    
    path('', views.lista_productos, name='home'), 
    path('producto/<int:pk>/', views.detalle_producto, name='detalle_producto'), 
    path('rastreo/', views.rastreo_pedido_form, name='rastreo_form'), 
    path('rastreo/<uuid:token>/', views.detalle_rastreo, name='detalle_rastreo'), 
    path('insumos/', views.lista_insumos, name='lista_insumos'),
    path('solicitar_producto/<int:pk>/', views.solicitar_producto_form, name='solicitar_producto'),
    path('galeria/', views.galeria_destacados, name='galeria_destacados'),
    path('reportes/', views.reporte_pedidos, name='reporte_pedidos'),
    #ruta para el filtro
    path('api/pedidos/filtrar/', api_views.filtrar_pedidos, name='filtrar_pedidos'),
    #rutas API
    path('api/', include(router.urls)),
]