
from django import forms
from .models import pedidos, Product

class SolicitudPedidoForm(forms.ModelForm):
    imagen = forms.ImageField(
        label="Sube una imagen de referencia", 
        required=False 
    ) 

    nombre_cliente = forms.CharField(label="Tu Nombre")
    contacto = forms.CharField(label="Email, Teléfono y/o Red Social")
    descripcion = forms.CharField(
        label="Descripción de lo solicitado", 
        widget=forms.Textarea
    )
    
    producto_ref = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = pedidos
        fields = [
            'nombre_cliente', 
            'contacto', 
            'producto_ref', 
            'descripcion', 
            'imagen', 
            'fecha_entrega',
        ]
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
        }