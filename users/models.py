from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = [
        ('estudiante', 'Estudiante'),
        ('profesor', 'Profesor'),
        ('bibliotecario', 'Bibliotecario'),
        ('admin', 'Administrador'),
    ]

    documento = models.CharField(max_length=20, unique=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')
    telefono = models.CharField(max_length=20, blank=True, default='')

    USERNAME_FIELD = 'documento'
    REQUIRED_FIELDS = ['username', 'email', 'rol']
    
