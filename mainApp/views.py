from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.urls import reverse
from .models import Product, categoryProduct, pedidos, insumos
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
    """Muestra el detalle del producto y permite crear un nuevo pedido."""
    
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
        initial_data = {'producto_ref': producto}
        form = SolicitudPedidoForm(initial=initial_data)

    context = {
        'producto': producto,
        'form': form,
        'titulo': f'Detalle: {producto.nombre}',
    }
    
    return render(request, 'detalle_producto.html', context)



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