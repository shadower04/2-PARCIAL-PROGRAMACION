from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Alumno
from .forms import AlumnoForm
from .utils import generar_pdf_alumno, enviar_pdf_email

@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.filter(usuario=request.user)
    return render(request, 'alumnos/lista_alumnos.html', {'alumnos': alumnos})

@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.usuario = request.user
            alumno.save()
            messages.success(request, 'Alumno creado exitosamente!')
            return redirect('lista_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/crear_alumno.html', {'form': form})

@login_required
def enviar_pdf(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id, usuario=request.user)
    
    try:
        # Generar PDF
        pdf_path = generar_pdf_alumno(alumno)
        
        # Enviar por email
        enviar_pdf_email(request.user.email, pdf_path, alumno)
        
        messages.success(request, f'PDF enviado exitosamente para {alumno.nombre}')
    except Exception as e:
        messages.error(request, f'Error al enviar PDF: {str(e)}')
    
    return redirect('lista_alumnos')