from django import forms
from .models import pedidos

class PedidoForm(forms.ModelForm):
    imagenes_referencia = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        required=False,
        label="Imágenes de referencia"
    )

    class Meta:
        model = pedidos
        fields = ['nombre_cliente', 'contacto', 'producto_ref', 'descripcion', 'fecha_entrega', 'imagenes_referencia']
        widgets = {
            'fecha_entrega': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_imagenes_referencia(self):
        files = self.files.getlist('imagenes_referencia')
        if len(files) > 3:
            raise forms.ValidationError("Solo puedes subir hasta 3 imágenes.")
        return files
