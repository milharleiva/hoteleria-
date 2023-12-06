from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('iniciar_sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('registro/', views.registro, name='registro'),
    path('inicio/', views.pagina_inicio, name='inicio'),
    path('habitaciones/', views.lista_habitaciones, name='lista_habitaciones'),
    path('habitaciones/<int:habitacion_id>/', views.detalle_habitacion, name='detalle_habitacion'),
    path('reservar/<int:habitacion_id>/', views.reservar_habitacion, name='reservar_habitacion'),
    path('confirmacion_reserva/', views.confirmacion_reserva, name='confirmacion_reserva'),
    path('gestionar_habitaciones/', views.gestionar_habitaciones, name='gestionar_habitaciones'),
    path('crear_habitacion/', views.crear_habitacion, name='crear_habitacion'),
    path('editar_habitacion/<int:habitacion_id>/', views.editar_habitacion, name='editar_habitacion'),
    path('eliminar_habitacion/<int:habitacion_id>/', views.eliminar_habitacion, name='eliminar_habitacion'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    # Añade aquí cualquier otra URL que necesites
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)