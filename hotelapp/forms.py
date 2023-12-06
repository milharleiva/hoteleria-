from django import forms
from .models import Reservacion, Habitacion
from django.apps import AppConfig
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = ['fecha_check_in', 'fecha_check_out']
        widgets = {
            'fecha_check_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class HotelappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotelapp'

    def ready(self):
        
        Group.objects.get_or_create(name='Cliente')
        Group.objects.get_or_create(name='Administrador')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise forms.ValidationError("El nombre de usuario debe tener al menos 5 caracteres.")
        return username

class HabitacionForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero', 'tipo', 'precio', 'descripcion', 'disponible', 'imagen']
        widgets = {
            'numero': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_numero'}),
            'tipo': forms.Select(attrs={'class': 'form-select', 'id': 'id_tipo'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'id': 'id_precio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'id': 'id_descripcion'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_disponible'}),
            # No se define un widget para 'imagen' ya que se manejará directamente como un input file en HTML
        }

    imagen = forms.ImageField(
        required=False, 
        widget=forms.FileInput(attrs={'class': 'form-control', 'id': 'id_imagen', 'accept': 'image/*'})
     )