from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import insumos, pedidos
from .serializers import InsumoSerializer, PedidoSerializer
from datetime import datetime

class InsumoViewSet(viewsets.ModelViewSet): #Permite Crear, Listar, Ver detalle, Modificar y Eliminar insumos.
    queryset = insumos.objects.all()
    serializer_class = InsumoSerializer
    #Ruta: /api/insumos/

class PedidoCreateUpdateViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet): #Permite Crear y Modificar pedidos. NO permite listar ni eliminar.
    queryset = pedidos.objects.all()
    serializer_class = PedidoSerializer
    #Ruta: /api/pedidos/


@api_view(['GET'])
def filtrar_pedidos(request):
    """
    Filtra pedidos por rango de fechas, estado y cantidad máxima.
    
    Parámetros (Query Params):
    - fecha_inicio (YYYY-MM-DD)
    - fecha_fin (YYYY-MM-DD)
    - estado (ej: 'solicitado', 'aprobado', etc.)
    - limite (int)
    """
    queryset = pedidos.objects.all()
    #Ruta: /api/pedidos/filtrar/
    #Filtro por Rango de Fechas
    fecha_inicio = request.query_params.get('fecha_inicio')
    fecha_fin = request.query_params.get('fecha_fin')

    if fecha_inicio and fecha_fin:
        try:
            queryset = queryset.filter(
                fecha_creacion__date__range=[fecha_inicio, fecha_fin]
            )
        except ValueError:
            return Response(
                {"error": "Formato de fecha inválido. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

    # 2. Filtro por Estado
    estado = request.query_params.get('estado')
    if estado:
        queryset = queryset.filter(estados=estado)

    # 3. Cantidad máxima de resultados
    limite = request.query_params.get('limite')
    if limite:
        try:
            limite = int(limite)
            queryset = queryset[:limite]
        except ValueError:
            pass # Si no es un número válido, ignoramos el límite

    serializer = PedidoSerializer(queryset, many=True)
    return Response(serializer.data)