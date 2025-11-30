from django.contrib import admin
from django.utils.html import format_html
from .models import Product, categoryProduct, insumos, pedidos, Exhibicion, CalificacionPedido
from django.db.models import Avg
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = ('nombre','category','precio_base','display_thumbnail',)
    

    list_filter = ('category',)
    
    search_fields = ('nombre','description',)
    

    def display_thumbnail(self, obj):
        """Muestra una miniatura de la primera imagen del producto."""

        if obj.imagen1:

            return format_html('<img src="{}" style="height: 50px; width: auto; border-radius: 4px;" />', obj.imagen1.url)
        return "No Image"
    

    display_thumbnail.short_description = 'Imagen'

@admin.register(pedidos)
class PedidosAdmin(admin.ModelAdmin):

    list_display = (
        'nombre_cliente',
        'fecha_creacion',
        'fecha_entrega',
        'plataforma',
        'estados', 
        'estado_pago',
        'token_Trakeo',
        'crear_exhibicion_url',
    )
    

    list_filter = (
        'estados',       
        'estado_pago',  
        'plataforma',    
        'fecha_creacion',
    )
    
    search_fields = (
        'nombre_cliente',
        'contacto',
        'descripcion',
        'token_Trakeo',
    )
    
    readonly_fields = ('fecha_creacion', 'token_Trakeo')

    def crear_exhibicion_url(self, obj):
            if hasattr(obj, 'exhibicion'):
                url = reverse('admin:mainApp_exhibicion_change', args=[obj.exhibicion.id])
                return format_html('<a style="color: green; font-weight: bold;" href="{}">✅ En Galería</a>', url)

            if obj.estados in ('finalizada', 'entregada'):
                url = reverse('admin:mainApp_exhibicion_add') + f'?pedido_referencia={obj.id}'
                return format_html('<a class="button" href="{}">🖼️ Promocionar</a>', url)
            
            return "Pendiente"
        
    crear_exhibicion_url.short_description = 'Galería'
    crear_exhibicion_url.allow_tags = True

@admin.register(insumos)
class InsumosAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'tipo',
        'cantidad_disponible',
        'unidad',
        'marca',
        'color',
    )
    
    list_filter = ('tipo','marca','color',)
    
    search_fields = ('name','tipo','marca',)

@admin.register(categoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)
    list_display = ('nombre',)

#nueva funcion

@admin.register(CalificacionPedido)
class CalificacionPedidoAdmin(admin.ModelAdmin):
    list_display = ('exhibicion', 'puntuacion', 'fecha_creacion')
    list_filter = ('puntuacion',)
    readonly_fields = ('fecha_creacion',)


@admin.register(Exhibicion)
class ExhibicionAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_thumbnail', 'pedido_referencia', 'mostrar_publicamente', 'display_puntuacion_promedio')
    list_filter = ('mostrar_publicamente', 'fecha_publicacion',)
    search_fields = ('pedido_referencia__nombre_cliente', 'descripcion_publica',)
    readonly_fields = ('fecha_publicacion', 'display_puntuacion_promedio',)
    
    def display_thumbnail(self, obj):
        if obj.imagen_final:
            return format_html('<img src="{}" style="height: 50px; width: auto; border-radius: 4px;" />', obj.imagen_final.url)
        return "No Image"
    display_thumbnail.short_description = 'Muestra'

    def display_puntuacion_promedio(self, obj):
        promedio = obj.puntuacion_promedio()
        if promedio:
            return f"{promedio} / 5.0"
        return "Sin Calificar"
    display_puntuacion_promedio.short_description = 'Punt. Promedio'

