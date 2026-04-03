from django.shortcuts import render, redirect
from django.contrib.auth import login , logout
from django.core.mail import send_mail
from django.conf import settings
import random
from .forms import RegistroComEmailForm
from .models import Verification
from django.contrib.auth.models import User  # Precisamos importar o modelo User!


def register(request):
    """Cadastra um novo usuário no sistema inativo e envia e-mail com código."""
    if request.method != "POST":
        form = RegistroComEmailForm()
    else:
        form = RegistroComEmailForm(data=request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            
            new_user.is_active = False  
            
            new_user.save()

            code = str(random.randint(100000, 999999))
            Verification.objects.create(user=new_user, verify_code=code)

            assunto = "Código para entrar no Apollo Notebooks! 🚀"
            mensagem = f"Olá {new_user.username}.\n\nPara começar a criar seus cadernos, use este código de acesso: {code}"
            remetente = settings.EMAIL_HOST_USER
            destinatario = [new_user.email]

            send_mail(assunto, mensagem, remetente, destinatario, fail_silently=False)

            request.session["id_usuario_pendente"] = new_user.id
            return redirect("users:verificar_codigo")

    context = {"form": form}
    return render(request, "users/register.html", context)

def deslogar_usuario(request):
    """Importa do django o método de deslogar"""
    logout(request)
    return redirect('appliance:index')


def verificar_codigo(request):
    """Função fantasma (view de verificação do codigo do email)"""
    usuario_id = request.session.get("id_usuario_pendente")

    if not usuario_id:
        return redirect("users:register")  

    if request.method == "POST":
        user_code = request.POST.get("codigo")  

        try:
            
            code_db = Verification.objects.get(user_id=usuario_id)

            if user_code == code_db.verify_code:
                usuario = User.objects.get(id=usuario_id)

                usuario.is_active = True
                
                usuario.save()

                code_db.delete()
                del request.session["id_usuario_pendente"]

                login(request, usuario)

                return redirect("appliance:books")
            else:
            
                return render(request,"users/verificar_codigo.html", {"erro": "Código incorreto. Tente novamente."},)

        except Verification.DoesNotExist:
            return redirect("users:register")

    return render(request, "users/verificar_codigo.html")
