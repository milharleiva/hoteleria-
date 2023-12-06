from django.contrib.auth.models import User, Group
from django.db import models

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Administrador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Habitacion(models.Model):
    TIPOS_HABITACION = [
        ('sencilla', 'Sencilla'),
        ('doble', 'Doble'),
        ('suite', 'Suite'),
    ]

    numero = models.IntegerField(unique=True)
    tipo = models.CharField(max_length=50, choices=TIPOS_HABITACION)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    disponible = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='image_habitacion/', blank=True, null=True)

    def __str__(self):
        return f"Habitación {self.numero} - {self.get_tipo_display()}"


class Reservacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)
    fecha_check_in = models.DateField()
    fecha_check_out = models.DateField()
    estado = models.CharField(
        max_length=20,
        choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
        default='pendiente'
    )

    def __str__(self):
        return f"Reservación de {self.cliente} para {self.habitacion}"
