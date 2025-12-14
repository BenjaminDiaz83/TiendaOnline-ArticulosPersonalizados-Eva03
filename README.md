Tienda articulos personalizados
Una app para realizar pedidos e internamente gestionar insumos y los estados de los pedidos

Funcionalidades clave = crud pedidos e insumos
Framework: Django

Primeros pasos:
1) preparacion de entorno
   python -m venv venv
(win) .\venv\Scripts\activate
(mac) venv/bin/activate

2) Instalacion de requerimientos
   pip install -r requirements.txt

3) Correr el servidor
   python manage.py runserver


Despliegue del Render (Todo ejecutado en el start command de render)

1.- Preparacion de la base de datos
   python manage.py migrate

2.- Creacion de administrador
   python manage.py shell -c "exec(open('create_admin.py').read())"

3.- Inicio del servidor web
   gunicorn DemoTiendaOnline.wsgi
