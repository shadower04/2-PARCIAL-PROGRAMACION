from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import RegistroForm

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Enviar correo de bienvenida
            try:
                send_mail(
                    '¡Bienvenido al Sistema de Alumnos!',
                    f'Hola {user.username},\n\nGracias por registrarte en nuestro sistema.',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
            except:
                pass  # Si falla el email, continuar igual
            
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'usuarios/dashboard.html')