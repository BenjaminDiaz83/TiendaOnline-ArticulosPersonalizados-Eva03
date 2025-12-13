from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg, Count, F
from django.contrib.auth.decorators import login_required   
from django.urls import reverse
from .models import pedidos, Product, categoryProduct, insumos, Exhibicion, CalificacionPedido
from datetime import datetime, timedelta
from .forms import SolicitudPedidoForm
from django.contrib import messages

def lista_productos(request):
    """Muestra el listado de productos con filtros, buscador y destacados."""
    
    categorias = categoryProduct.objects.all()
    productos = Product.objects.all()
    destacados = Product.objects.filter(destacado=True)
    
    
    categoria_seleccionada_id = request.GET.get('categoria')
    if categoria_seleccionada_id:
        productos = productos.filter(category__id=categoria_seleccionada_id)
    
    
    query = request.GET.get('q') 
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | 
            Q(description__icontains=query)
        ).distinct()
        
    
    context = {
        'productos': productos,
        'destacados': destacados,
        'categorias': categorias,
        'categoria_seleccionada_id': categoria_seleccionada_id,
        'query': query,
        'titulo': 'Catálogo de Productos',
    }
    
    return render(request, 'lista_productos.html', context)


def detalle_producto(request, pk):
    """Muestra solo el detalle del producto, con un botón para la solicitud."""
    
    producto = get_object_or_404(Product, pk=pk)
    
    context = {
        'producto': producto,
        'titulo': f'Detalle: {producto.nombre}',
    }
    
    
    return render(request, 'detalle_producto.html', context)

def solicitar_producto_form(request, pk):
    """Nueva vista dedicada a manejar el formulario de solicitud de pedido."""
    
    producto = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = SolicitudPedidoForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo_pedido = form.save(commit=False)
            
            
            nuevo_pedido.producto_ref = producto
            nuevo_pedido.plataforma = 'website'
            nuevo_pedido.estados = 'solicitado' 
            nuevo_pedido.estado_pago = 'pendiente' 
            
            nuevo_pedido.save()
            
            messages.success(request, f'¡Pedido creado con éxito! Tu código de rastreo es: {nuevo_pedido.token_Trakeo}')
            
            
            return redirect('detalle_rastreo', token=nuevo_pedido.token_Trakeo)
    else:
        
        initial_data = {
            'producto_ref': producto,
            
            'descripcion': f'Solicitud basada en el producto: {producto.nombre}',
        }
        form = SolicitudPedidoForm(initial=initial_data)

    context = {
        'producto': producto,
        'form': form,
        'titulo': f'Solicitar: {producto.nombre}',
    }
    
    
    return render(request, 'solicitar_producto_form.html', context)

def rastreo_pedido_form(request):
    """Muestra el formulario para ingresar el token de rastreo."""
    if request.method == 'POST':
        token = request.POST.get('token_rastreo')
        if token:
            try:
                pedido = pedidos.objects.get(token_Trakeo=token)
                return redirect('detalle_rastreo', token=token)
            except pedidos.DoesNotExist:
                messages.error(request, 'Código de rastreo no encontrado. Verifica el token.')
                
    context = {
        'titulo': 'Rastreo de Pedido',
    }
    
    return render(request, 'rastreo_form.html', context)


def detalle_rastreo(request, token):
    """Muestra el estado de un pedido usando el token de Trakeo (UUID)."""
    
    
    pedido = get_object_or_404(pedidos, token_Trakeo=token) 
    

    tracking_url = request.build_absolute_uri(reverse('detalle_rastreo', args=[pedido.token_Trakeo]))
    
    context = {
        'pedido': pedido,
        'tracking_url': tracking_url,
        'titulo': f'Rastreo del Pedido #{pedido.id}',
    }
    
    return render(request, 'detalle_rastreo.html', context)


def lista_insumos(request):
    """Lista todos los insumos disponibles."""
    
    insumos_list = insumos.objects.all().order_by('name')
    
    context = {
        'insumos_list': insumos_list,
        'titulo': 'Inventario de Insumos',
    }
    
    return render(request, 'lista_insumos.html', context)

def galeria_destacados(request):
    Exhibiciones = Exhibicion.objects.filter(mostrar_publicamente=True).annotate(promedio_calificacion=Avg('calificaciones__puntuacion')).order_by(
        '-promedio_calificacion', '-fecha_publicacion'

    )
    context = {
        'exhibiciones': Exhibiciones,
        'titulo': 'Galeria de Trabajos Realizados',
        'subtitulo': 'Muestra de productos realizados, junto a la satisfacción de los clientes',
    }
    return render(request, 'galeria_destacados.html', context)

#eva 4 hacia abajo

@login_required 
def reporte_pedidos(request):

    fecha_inicio_str = request.GET.get('fecha_inicio')
    fecha_fin_str = request.GET.get('fecha_fin')
    plataforma_seleccionada = request.GET.get('plataforma')

    platform_choices = pedidos.PLATAFORMAS
    hoy = datetime.now().date()
    inicio_default = hoy - timedelta(days=30)

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date() if fecha_inicio_str else inicio_default
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date() if fecha_fin_str else hoy
    except ValueError:
        fecha_inicio = inicio_default
        fecha_fin = hoy

    qs_filtrado = pedidos.objects.filter(
        fecha_creacion__date__gte=fecha_inicio,
        fecha_creacion__date__lte=fecha_fin
    )
    if plataforma_seleccionada:
        qs_filtrado = qs_filtrado.filter(plataforma=plataforma_seleccionada)

    reporte_estados = qs_filtrado.values('estados').annotate(
        cantidad=Count('estados')
    ).order_by('-cantidad')
    estado_labels = dict(pedidos.ESTADOS)
    for item in reporte_estados:
        item['estados'] = estado_labels.get(item['estados'],'Desconocido')
    pedidos_detallados = qs_filtrado.select_related('producto_ref').order_by('-fecha_creacion')
    reporte_plataformas = qs_filtrado.values('plataforma').annotate(
        cantidad=Count('plataforma')
    ).order_by('-cantidad')

    plataforma_labels = dict(pedidos.PLATAFORMAS)
    for item in reporte_plataformas:
        item['plataforma'] = plataforma_labels.get(item['plataforma'],'Desconocida')
    
    context = {
        'reporte_estados': reporte_estados,
        'reporte_plataformas': reporte_plataformas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'plataforma_seleccionada': plataforma_seleccionada,
        'platform_choices': platform_choices,
        'pedidos_detallados': pedidos_detallados,
        'title': 'Reporte de Pedidos'
    }
    return render(request, 'reporte_pedidos.html', context)

