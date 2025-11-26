from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # ← Importar User por defecto

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User  # ← Usar User por defecto, no Usuario
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email ya está registrado.")
        return email