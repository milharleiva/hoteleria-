from django.contrib import admin
from django.urls import path, include  # Asegúrate de importar include
from hotelapp import views as hotelapp_views  # Este alias es opcional pero ayuda a la claridad
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hotelapp_views.pagina_inicio, name='inicio'),  # Ruta raíz que redirige a la página de inicio
    path('accounts/login/', LoginView.as_view(), name='login'),  # Ruta para el login, si utilizas la vista genérica de Django
    path('hotelapp/', include('hotelapp.urls')),  # Incluye las URLs de la aplicación hotelapp
    # Añade aquí cualquier otra URL que necesites
]
