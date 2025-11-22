from django.contrib import admin
from django.utils.html import format_html
from .models import Product, categoryProduct, insumos, pedidos

# admin de productos


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


#admin de pedidos


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


#admin de insumos
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


#categoria
@admin.register(categoryProduct)
class CategoryProductAdmin(admin.ModelAdmin):

    search_fields = ('nombre',)
    list_display = ('nombre',)