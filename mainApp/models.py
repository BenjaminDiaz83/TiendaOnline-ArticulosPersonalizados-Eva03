import uuid
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Product(models.Model):
    nombre = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey('categoryProduct', on_delete=models.CASCADE)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    imagen1 = models.ImageField(upload_to='imagenes_productos/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='imagenes_productos/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='imagenes_productos/', blank=True, null=True)
    destacado = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre

class categoryProduct(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class insumos(models.Model):
    name = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    cantidad_disponible = models.PositiveIntegerField()
    unidad = models.CharField(max_length=20, blank=True)
    marca = models.CharField(max_length=50)
    color = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class pedidos(models.Model):
    ESTADOS = [
    ('solicitado', 'Solicitado'),
    ('aprobado', 'Aprobado'),
    ('en_proceso', 'En proceso'),
    ('realizada', 'Realizada'),
    ('entregada', 'Entregada'),
    ('finalizada', 'Finalizada'),
    ('cancelada', 'Cancelada'),
    ]
    PAGOS = [
    ('pendiente', 'Pendiente'),
    ('parcial', 'Parcial'),
    ('pagado', 'Pagado'),
    ]
    PLATAFORMAS = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('whatsapp', 'WhatsApp'),
        ('tiktok', 'Tiktok'), #pagina extra pedida en la prueba
        ('presencial', 'Presencial'),
        ('website', 'Website'),
    ]
    #Datos primoridales del cliente 
    nombre_cliente = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    #Datos de los productos (Si aplica por que recuerden que puede ser personalizado)
    producto_ref = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    descripcion = models.TextField()

    imagen = models.ImageField(upload_to='imagenes_pedidos/', blank=True, null=True)

    imagen_ref1 = models.ImageField(upload_to='imagenes_pedidos/', blank=True, null=True, verbose_name="Imagen de referencia 1")
    imagen_ref2 = models.ImageField(upload_to='imagenes_pedidos/', blank=True, null=True, verbose_name="Imagen de referencia 2")
    imagen_ref3 = models.ImageField(upload_to='imagenes_pedidos/', blank=True, null=True, verbose_name="Imagen de referencia 3")
    imagenes_referencia = models.JSONField(default=list, blank=True, null=True)  # Para múltiples imágenes de referencia

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateField(blank=True, null=True)
    plataforma = models.CharField(max_length=50, choices=PLATAFORMAS, default='website')

    estados = models.CharField(max_length=20, choices=ESTADOS, default='solicitado')
    estado_pago = models.CharField(max_length=20, choices=PAGOS, default='pendiente')

    token_Trakeo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #VITAL para el seguimiento posterior del pedido

    def clean(self):
        super().clean()
        if self.estado_pago != 'pagado' and self.estados == 'finalizada':
            raise ValidationError("No se puede finalizar un pedido con pago pendiente o parcial.")
    def __str__(self):
        return f"Pedido de {self.nombre_cliente} - {self.producto_ref.nombre if self.producto_ref else 'Personalizado'}"
