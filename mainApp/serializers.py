from rest_framework import serializers
from .models import insumos, pedidos

class InsumoSerializer(serializers.ModelSerializer):
    class Meta:
        model = insumos
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = pedidos
        fields = '__all__'

        read_only_fields = ['token_Trakeo', 'fecha_creacion']