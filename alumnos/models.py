from django.db import models
from django.contrib.auth.models import User  # ← Cambiar esta línea

class Alumno(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('egresado', 'Egresado'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  # ← User directamente
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    edad = models.IntegerField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    estado = models.CharField(max_length=10, choices=ESTADOS, default='activo')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        ordering = ['-fecha_creacion']