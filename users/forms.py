from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Verification


class RegistroComEmailForm(UserCreationForm):
    """formulário de cadastro que exige o e-mail do usuário"""

    email = forms.EmailField(
        required=True, help_text="Obrigatório para enviarmos suas boas-vindas."
    )

    class Meta:
        model = User
        fields = ("username", "email")

