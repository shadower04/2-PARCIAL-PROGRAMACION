from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_alumnos, name='lista_alumnos'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('enviar-pdf/<int:alumno_id>/', views.enviar_pdf, name='enviar_pdf'),
]