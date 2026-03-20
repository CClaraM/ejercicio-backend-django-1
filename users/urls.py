from django.urls import path
from .views import LoginView, MiPerfilView


urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('usuarios/me/',MiPerfilView.as_view(), name='mi_perfil'),
]