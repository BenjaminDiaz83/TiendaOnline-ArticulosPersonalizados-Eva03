import os
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction


USERNAME = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
EMAIL = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
PASSWORD = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass') 


User = get_user_model()


@transaction.atomic
def create_superuser_if_not_exists():
    if not User.objects.filter(username=USERNAME).exists():
        print(f"Creando superusuario {USERNAME}...")
        try:
            
            User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
            print("¡Superusuario creado con éxito!")
        except IntegrityError:
            
            print("El superusuario ya fue creado por otro proceso.")
        except Exception as e:
            
            print(f"Error fatal al crear el superusuario: {e}")
    else:
        print(f"El superusuario {USERNAME} ya existe. Saltando creación.")

# Ejecutar la función
create_superuser_if_not_exists()