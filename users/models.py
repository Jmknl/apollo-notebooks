from django.db import models
from django.conf import settings  


class Verification(models.Model):
    """Tabela para receber o código de vericação do usuário, enviado pelo email"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    verify_code = models.CharField(max_length=6)

    def __str__(self):
        return f"Código {self.verify_code} do usuário ({self.user.email})"
