from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from django.shortcuts import render, redirect
from .models import Habitacion, Reservacion, Cliente, Administrador
from .forms import ReservacionForm
from django import forms
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import HabitacionForm  
import re 
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            return render(request, 'login.html', {'error_message': 'Credenciales incorrectas'})
    return render(request, 'registration/login.html')

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

       
        if password == password2:
            
            if User.objects.filter(username=username).exists():
                
                return render(request, 'registro.html', {'error': 'El nombre de usuario ya existe'})
            else:
              
                user = User.objects.create(username=username, password=make_password(password))
                Cliente.objects.create(usuario=user, nombre=username)
                login(request, user)
                return redirect('iniciar_sesion')
        else:
           
            return render(request, 'registro.html', {'error': 'Las contraseñas no coinciden'})

    return render(request, 'registro.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

@login_required
def pagina_inicio(request):
    return render(request, 'inicio.html')

def lista_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    for habitacion in habitaciones:
        if not habitacion.imagen:
            habitacion.imagen_url = 'path_to_default_image.jpg'
        else:
            habitacion.imagen_url = habitacion.imagen.url

    return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

def detalle_habitacion(request, habitacion_id):
    try:
        habitacion = Habitacion.objects.get(pk=habitacion_id)
    except Habitacion.DoesNotExist:
        raise Http404("Habitación no encontrada")
    return render(request, 'detalle_habitacion.html', {'habitacion': habitacion})

@login_required
def reservar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)

    if request.method == 'POST':
        form = ReservacionForm(request.POST)
        if form.is_valid():
            
            if request.user.is_authenticated:
               
                reserva = form.save(commit=False)
                reserva.cliente = request.user.cliente  
                reserva.habitacion = habitacion
                reserva.save()

                
                habitacion.disponible = False
                habitacion.save()

                
                return redirect('confirmacion_reserva')
    else:
        form = ReservacionForm()

    return render(request, 'reserva.html', {'habitacion': habitacion, 'form': form, 'mensaje': 'Esta habitación no está disponible para reservas'})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='inicio')
def gestionar_habitaciones(request):
    habitaciones = Habitacion.objects.all()
    return render(request, 'gestionar_habitaciones.html', {'habitaciones': habitaciones})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='inicio')
def crear_habitacion(request):
    if request.method == 'POST':
        # Aquí se procesan los campos del formulario manualmente
        numero = request.POST.get('numero')
        tipo = request.POST.get('tipo')
        precio = request.POST.get('precio')
        descripcion = request.POST.get('descripcion')
        disponible = request.POST.get('disponible') == 'on'
        imagen = request.FILES.get('imagen')

        # Manejo de la imagen
        imagen_url = None
        if imagen:
            fs = FileSystemStorage(location=os.path.join(settings.STATIC_ROOT, 'image_habitacion'))
            filename = fs.save(imagen.name, imagen)
            imagen_url = fs.url(filename)

        # Crear y guardar el objeto Habitacion
        habitacion = Habitacion(
            numero=numero,
            tipo=tipo,
            precio=precio,
            descripcion=descripcion,
            disponible=disponible,
            # Suponiendo que el modelo Habitacion tiene un campo para la URL de la imagen
            imagen=imagen_url  
        )
        habitacion.save()
        
        return redirect('gestionar_habitaciones')
    else:
        return render(request, 'crear_habitacion.html')
@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='inicio')
def editar_habitacion(request, habitacion_id):
    habitacion = get_object_or_404(Habitacion, pk=habitacion_id)
    if request.method == 'POST':
        form = HabitacionForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect('gestionar_habitaciones')
    else:
        form = HabitacionForm(instance=habitacion)
    return render(request, 'editar_habitacion.html', {'form': form, 'habitacion': habitacion})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='inicio')
def eliminar_habitacion(request, habitacion_id):
    try:
        habitacion = Habitacion.objects.get(pk=habitacion_id)
    except Habitacion.DoesNotExist:
       
        return redirect('gestionar_habitaciones')
    
    if request.method == 'POST':
       
        habitacion.delete()
        return redirect('gestionar_habitaciones')
    
    return render(request, 'eliminar_habitacion.html', {'habitacion': habitacion})
    

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='inicio')
def gestionar_reservaciones(request):
    reservaciones = Reservacion.objects.all()
    return render(request, 'gestionar_reservaciones.html', {'reservaciones': reservaciones})

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='inicio')
def confirmar_reservacion(request, reservacion_id):
  
    return redirect('gestionar_reservaciones')

@login_required
@user_passes_test(lambda u: u.is_superuser, login_url='inicio')
def cancelar_reservacion(request, reservacion_id):
    
    return redirect('gestionar_reservaciones')

@login_required
def confirmacion_reserva(request):
    
    return render(request, 'confirmacion_reserva.html')

@login_required
@user_passes_test(lambda u: u.is_superuser)
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        is_admin = request.POST.get('is_admin') == 'on'

        # Validaciones regex
        regex_username = r'^\w+$'  # Ejemplo: solo caracteres alfanuméricos y guiones bajos
        regex_password = r'[A-Za-z0-9@#$%^&+=]{8,}'  # Ejemplo: al menos 8 caracteres y caracteres especiales permitidos
        
        if not re.match(regex_username, username):
            # Manejar nombre de usuario inválido
            return render(request, 'crear_usuario.html', {'error': 'Nombre de usuario inválido'})

        if not re.match(regex_password, password):
            # Manejar contraseña inválida
            return render(request, 'crear_usuario.html', {'error': 'Contraseña inválida'})

        # Creación del usuario
        user = User.objects.create(
            username=username,
            password=make_password(password),
            first_name=nombre,
            is_superuser=is_admin,
            is_staff=is_admin  
        )

        if is_admin:
            Administrador.objects.create(usuario=user, nombre=nombre)

        return redirect('inicio')
    else:
        return render(request, 'crear_usuario.html')
